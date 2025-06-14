from clickhouse_driver import Client
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from PIL import Image
import torch
import torchvision.transforms as transforms
from transformers import CLIPModel, CLIPProcessor
from sklearn.preprocessing import normalize
import logging
from typing import List, Dict, Tuple, Optional
from clickhouse_driver import Client
from datetime import datetime
import os

def save_to_clickhouse_basic(config: dict, data: dict):
    client = Client(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

    start_dt = datetime.fromisoformat(data['metadata']['startDateTime'])
    end_dt = datetime.fromisoformat(data['metadata']['endDateTime'])

    client.execute(f'''
        INSERT INTO {config['table_crop_detection']} 
        (crop, alternate_names, color, confidence, startDateTime, endDateTime, duration)
        VALUES
    ''', [(data['crop'], data['alternate_names'], data['color'], data['confidence'],
           start_dt, end_dt, data['metadata']['duration'])])


def save_to_clickhouse_detailed(config: dict, data: dict, image_path: str = None):
    client = Client(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

    start_dt = datetime.fromisoformat(data['metadata']['startDateTime'])
    end_dt = datetime.fromisoformat(data['metadata']['endDateTime'])

    client.execute(f'''
        INSERT INTO {config['table_crop_analysis']} (
            crop, alternate_names, color, confidence, overall_description,

            growth_stage, estimated_age_months, growth_description,

            overall_health, vigor_score, disease_indicators, pest_indicators, stress_indicators, health_description,

            planting_pattern, plant_density, field_size_estimate, crop_uniformity, weed_presence, field_description,

            setting, terrain, surrounding_vegetation, infrastructure_visible, weather_conditions, environment_description,

            moisture_level, soil_visibility, irrigation_evidence, season_indication, conditions_description,

            farming_type, management_quality, harvest_readiness, estimated_months_to_harvest, management_description,

            people_present, people_count, people_description, activities_observed, people_confidence_score,

            equipment_present, equipment_count, equipment_types, equipment_description, equipment_condition, equipment_usage, equipment_confidence_score,

            animals_present, total_animal_count, cattle_count, poultry_count, goats_count, sheep_count, pigs_count, horses_count, other_livestock_count, wild_animals_count, animal_types_identified, animal_description, animal_activity, animal_health_indicators, integration_with_crops, animals_confidence_score,

            recommendations, recommendations_summary,

            semantic_tags, search_context,

            image_quality, lighting_conditions, viewing_angle, coverage_area, visual_description,

            text_embedding, image_embedding, hybrid_embedding,

            image_path, startDateTime, endDateTime, duration
        ) VALUES
    ''', [(
        # Basic crop identification
        data['crop'],
        data['alternate_names'],
        data['color'],
        data['confidence'],
        data.get('overall_description', ''),

        # Growth stage
        data['growth_stage']['stage'],
        data['growth_stage']['estimated_age_months'],
        data['growth_stage']['description'],

        # Health assessment
        data['health_assessment']['overall_health'],
        data['health_assessment']['vigor_score'],
        data['health_assessment']['disease_indicators'],
        data['health_assessment']['pest_indicators'],
        data['health_assessment']['stress_indicators'],
        data['health_assessment'].get('health_description', ''),

        # Field characteristics
        data['field_characteristics']['planting_pattern'],
        data['field_characteristics']['plant_density'],
        data['field_characteristics']['field_size_estimate'],
        data['field_characteristics']['crop_uniformity'],
        data['field_characteristics']['weed_presence'],
        data['field_characteristics'].get('field_description', ''),

        # Environmental context
        data['environmental_context']['setting'],
        data['environmental_context']['terrain'],
        data['environmental_context']['surrounding_vegetation'],
        data['environmental_context']['infrastructure_visible'],
        data['environmental_context']['weather_conditions'],
        data['environmental_context'].get('environment_description', ''),

        # Growing conditions
        data['growing_conditions']['moisture_level'],
        data['growing_conditions']['soil_visibility'],
        data['growing_conditions']['irrigation_evidence'],
        data['growing_conditions']['season_indication'],
        data['growing_conditions'].get('conditions_description', ''),

        # Agricultural insights
        data['agricultural_insights']['farming_type'],
        data['agricultural_insights']['management_quality'],
        data['agricultural_insights']['harvest_readiness'],
        data['agricultural_insights']['estimated_months_to_harvest'],
        data['agricultural_insights'].get('management_description', ''),

        # People detection
        data['people_detection']['people_present'],
        data['people_detection']['people_count'],
        data['people_detection'].get('people_description', ''),
        data['people_detection']['activities_observed'],
        data['people_detection']['confidence_score'],

        # Equipment detection
        data['equipment_detection']['equipment_present'],
        data['equipment_detection']['equipment_count'],
        data['equipment_detection']['equipment_types'],
        data['equipment_detection'].get('equipment_description', ''),
        data['equipment_detection']['equipment_condition'],
        data['equipment_detection']['equipment_usage'],
        data['equipment_detection']['confidence_score'],

        # Animal detection
        data['animal_detection']['animals_present'],
        data['animal_detection']['total_animal_count'],
        data['animal_detection']['animal_categories']['cattle'],
        data['animal_detection']['animal_categories']['poultry'],
        data['animal_detection']['animal_categories']['goats'],
        data['animal_detection']['animal_categories']['sheep'],
        data['animal_detection']['animal_categories']['pigs'],
        data['animal_detection']['animal_categories']['horses'],
        data['animal_detection']['animal_categories']['other_livestock'],
        data['animal_detection']['animal_categories']['wild_animals'],
        data['animal_detection']['animal_types_identified'],
        data['animal_detection'].get('animal_description', ''),
        data['animal_detection']['animal_activity'],
        data['animal_detection']['animal_health_indicators'],
        data['animal_detection']['integration_with_crops'],
        data['animal_detection']['confidence_score'],

        # Recommendations
        data['recommendations'],
        data.get('recommendations_summary', ''),

        # Semantic search fields
        data.get('semantic_tags', []),
        data.get('search_context', ''),

        # Image metadata
        data['image_metadata']['image_quality'],
        data['image_metadata']['lighting_conditions'],
        data['image_metadata']['viewing_angle'],
        data['image_metadata']['coverage_area'],
        data['image_metadata'].get('visual_description', ''),

        # Embedding vectors (empty arrays - to be populated by embedding pipeline)
        [],  # text_embedding
        [],  # image_embedding
        [],  # hybrid_embedding

        # Additional metadata
        image_path or '',
        start_dt,
        end_dt,
        data['metadata']['duration']
    )])


class EmbeddingGenerator:
    """
    Lightweight embedding generator for real-time processing during insert
    """

    _instance = None
    _models_loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._models_loaded:
            self._initialize_models()
            self._models_loaded = True

    def _initialize_models(self):
        """Initialize embedding models (singleton pattern for efficiency)"""
        try:
            # Text embedding model - fast and efficient
            self.text_model = SentenceTransformer('all-MiniLM-L6-v2')

            # CLIP model for image embeddings
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

            logging.info("Embedding models loaded successfully")

        except Exception as e:
            logging.error(f"Error loading embedding models: {e}")
            # Set to None to handle gracefully
            self.text_model = None
            self.clip_model = None
            self.clip_processor = None

    def generate_text_embedding(self, text: str) -> List[float]:
        """Generate text embedding with error handling"""
        try:
            if not self.text_model or not text or not text.strip():
                return [0.0] * 384  # Return zero vector for empty text or model failure

            # Clean text
            cleaned_text = ' '.join(text.split())

            # Generate and normalize embedding
            embedding = self.text_model.encode(cleaned_text)
            embedding = normalize([embedding])[0]

            return embedding.tolist()

        except Exception as e:
            logging.error(f"Error generating text embedding: {e}")
            return [0.0] * 384

    def generate_image_embedding(self, image_path: str) -> List[float]:
        """Generate image embedding with error handling"""
        try:
            if not self.clip_model or not self.clip_processor:
                return [0.0] * 512

            if not os.path.exists(image_path):
                logging.warning(f"Image file not found: {image_path}")
                return [0.0] * 512

            # Load and process image
            image = Image.open(image_path).convert('RGB')
            inputs = self.clip_processor(images=image, return_tensors="pt")

            with torch.no_grad():
                image_features = self.clip_model.get_image_features(**inputs)

            # Normalize embedding
            image_embedding = normalize(image_features.numpy())[0]
            return image_embedding.tolist()

        except Exception as e:
            logging.error(f"Error generating image embedding for {image_path}: {e}")
            return [0.0] * 512

    def generate_hybrid_embedding(self, text_embedding: List[float],
                                  image_embedding: List[float],
                                  text_weight: float = 0.6,
                                  image_weight: float = 0.4) -> List[float]:
        """Generate hybrid embedding"""
        try:
            text_emb = np.array(text_embedding)
            image_emb = np.array(image_embedding)

            # Handle different dimensions
            max_dim = max(len(text_emb), len(image_emb))
            if len(text_emb) < max_dim:
                text_emb = np.pad(text_emb, (0, max_dim - len(text_emb)))
            if len(image_emb) < max_dim:
                image_emb = np.pad(image_emb, (0, max_dim - len(image_emb)))

            # Weighted combination and normalization
            hybrid_emb = text_weight * text_emb + image_weight * image_emb
            hybrid_emb = normalize([hybrid_emb])[0]

            return hybrid_emb.tolist()

        except Exception as e:
            logging.error(f"Error generating hybrid embedding: {e}")
            return [0.0] * max(len(text_embedding), len(image_embedding))


def create_comprehensive_text_for_embedding(data: dict) -> str:
    """
    Enhanced version for the updated flat table schema
    Optimized for agricultural crop analysis with people, equipment, and animal detection
    """
    text_components = []

    # Primary crop identification (highest weight)
    text_components.append(f"Crop: {data['crop']}")
    if data.get('alternate_names'):
        text_components.append(f"Also known as: {', '.join(data['alternate_names'])}")
    if data.get('color'):
        text_components.append(f"Colors: {', '.join(data['color'])}")

    # Overall description
    if data.get('overall_description'):
        text_components.append(data['overall_description'])

    # Growth stage information
    if data.get('growth_stage'):
        text_components.append(f"Growth stage: {data['growth_stage']}")
        if data.get('estimated_age_months'):
            text_components.append(f"Age: {data['estimated_age_months']} months")
    if data.get('growth_description'):
        text_components.append(data['growth_description'])

    # Health assessment (critical for similarity)
    if data.get('overall_health'):
        text_components.append(f"Health: {data['overall_health']}")
    if data.get('disease_indicators') and data['disease_indicators'] != ['empty list']:
        text_components.append(f"Diseases: {', '.join(data['disease_indicators'])}")
    if data.get('pest_indicators') and data['pest_indicators'] != ['empty list']:
        text_components.append(f"Pests: {', '.join(data['pest_indicators'])}")
    if data.get('stress_indicators') and 'none_detected' not in str(data['stress_indicators']):
        text_components.append(f"Stress: {', '.join(data['stress_indicators'])}")
    if data.get('health_description'):
        text_components.append(data['health_description'])

    # Field characteristics
    field_details = []
    if data.get('planting_pattern'):
        field_details.append(f"planted in {data['planting_pattern']}")
    if data.get('plant_density'):
        field_details.append(f"{data['plant_density']} density")
    if data.get('crop_uniformity'):
        field_details.append(f"{data['crop_uniformity']} uniformity")
    if data.get('weed_presence'):
        field_details.append(f"{data['weed_presence']} weeds")
    if field_details:
        text_components.append("Field characteristics: " + ", ".join(field_details))
    if data.get('field_description'):
        text_components.append(data['field_description'])

    # Environmental context
    env_details = []
    if data.get('setting'):
        env_details.append(f"{data['setting']} setting")
    if data.get('terrain'):
        env_details.append(f"{data['terrain']} terrain")
    if data.get('weather_conditions'):
        env_details.append(f"{data['weather_conditions']} weather")
    if data.get('surrounding_vegetation'):
        env_details.append(f"surrounded by {data['surrounding_vegetation']}")
    if env_details:
        text_components.append("Environment: " + ", ".join(env_details))
    if data.get('environment_description'):
        text_components.append(data['environment_description'])
    if data.get('infrastructure_visible'):
        text_components.append(f"Infrastructure: {', '.join(data['infrastructure_visible'])}")

    # Growing conditions
    condition_details = []
    if data.get('moisture_level'):
        condition_details.append(f"{data['moisture_level']} moisture")
    if data.get('irrigation_evidence') and data['irrigation_evidence'] != 'not_visible':
        condition_details.append(f"{data['irrigation_evidence']} irrigation")
    if data.get('season_indication'):
        condition_details.append(f"{data['season_indication']}")
    if condition_details:
        text_components.append("Conditions: " + ", ".join(condition_details))
    if data.get('conditions_description'):
        text_components.append(data['conditions_description'])

    # Agricultural insights
    if data.get('farming_type'):
        text_components.append(f"Farming: {data['farming_type']}")
    if data.get('management_quality'):
        text_components.append(f"Management: {data['management_quality']}")
    if data.get('harvest_readiness'):
        text_components.append(f"Harvest readiness: {data['harvest_readiness']}")
        if data.get('estimated_months_to_harvest'):
            text_components.append(f"Months to harvest: {data['estimated_months_to_harvest']}")
    if data.get('management_description'):
        text_components.append(data['management_description'])

    # People detection
    if data.get('people_present'):
        people_info = f"People present: {data.get('people_count', 0)} people"
        if data.get('activities_observed'):
            people_info += f", activities: {', '.join(data['activities_observed'])}"
        text_components.append(people_info)
        if data.get('people_description'):
            text_components.append(data['people_description'])

    # Equipment detection
    if data.get('equipment_present'):
        equipment_info = f"Equipment present: {data.get('equipment_count', 0)} pieces"
        if data.get('equipment_types'):
            equipment_info += f", types: {', '.join(data['equipment_types'])}"
        if data.get('equipment_condition'):
            equipment_info += f", condition: {data['equipment_condition']}"
        if data.get('equipment_usage'):
            equipment_info += f", usage: {data['equipment_usage']}"
        text_components.append(equipment_info)
        if data.get('equipment_description'):
            text_components.append(data['equipment_description'])

    # Animal detection
    if data.get('animals_present'):
        animal_counts = []
        if data.get('cattle_count', 0) > 0:
            animal_counts.append(f"{data['cattle_count']} cattle")
        if data.get('poultry_count', 0) > 0:
            animal_counts.append(f"{data['poultry_count']} poultry")
        if data.get('goats_count', 0) > 0:
            animal_counts.append(f"{data['goats_count']} goats")
        if data.get('sheep_count', 0) > 0:
            animal_counts.append(f"{data['sheep_count']} sheep")
        if data.get('pigs_count', 0) > 0:
            animal_counts.append(f"{data['pigs_count']} pigs")
        if data.get('horses_count', 0) > 0:
            animal_counts.append(f"{data['horses_count']} horses")
        if data.get('other_livestock_count', 0) > 0:
            animal_counts.append(f"{data['other_livestock_count']} other livestock")
        if data.get('wild_animals_count', 0) > 0:
            animal_counts.append(f"{data['wild_animals_count']} wild animals")

        animal_info = f"Animals present: total {data.get('total_animal_count', 0)}"
        if animal_counts:
            animal_info += f" ({', '.join(animal_counts)})"
        text_components.append(animal_info)

        if data.get('animal_types_identified'):
            text_components.append(f"Animal types: {', '.join(data['animal_types_identified'])}")
        if data.get('animal_activity'):
            text_components.append(f"Animal activities: {', '.join(data['animal_activity'])}")
        if data.get('animal_health_indicators'):
            text_components.append(f"Animal health: {data['animal_health_indicators']}")
        if data.get('integration_with_crops'):
            text_components.append(f"Crop-animal integration: {data['integration_with_crops']}")
        if data.get('animal_description'):
            text_components.append(data['animal_description'])

    # Recommendations (important for finding similar solutions)
    if data.get('recommendations'):
        recommendations_text = ". ".join(data['recommendations'])
        text_components.append(f"Recommendations: {recommendations_text}")
    if data.get('recommendations_summary'):
        text_components.append(data['recommendations_summary'])

    # Semantic tags and search context
    if data.get('semantic_tags'):
        text_components.append("Tags: " + ", ".join(data['semantic_tags']))
    if data.get('search_context'):
        text_components.append(data['search_context'])

    # Image metadata context
    if data.get('image_quality'):
        text_components.append(f"Image quality: {data['image_quality']}")
    if data.get('viewing_angle'):
        text_components.append(f"View: {data['viewing_angle']}")
    if data.get('coverage_area'):
        text_components.append(f"Coverage: {data['coverage_area']}")
    if data.get('visual_description'):
        text_components.append(data['visual_description'])

    # Join all components
    comprehensive_text = ". ".join([comp.strip() for comp in text_components if comp.strip()])
    return comprehensive_text


def save_to_clickhouse_with_embeddings(config: dict, data: dict, image_path: str = None):
    """
    Enhanced version for the updated flat table schema with embeddings
    Includes all new fields: people, equipment, and animal detection
    """

    # Initialize embedding generator (singleton)
    embedding_gen = EmbeddingGenerator()

    # Generate comprehensive text for embedding
    comprehensive_text = create_comprehensive_text_for_embedding(data)

    # Generate embeddings
    text_embedding = embedding_gen.generate_text_embedding(comprehensive_text)
    image_embedding = embedding_gen.generate_image_embedding(image_path) if image_path else [0.0] * 512
    hybrid_embedding = embedding_gen.generate_hybrid_embedding(text_embedding, image_embedding)

    # Connect to ClickHouse
    client = Client(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

    start_dt = datetime.fromisoformat(data['metadata']['startDateTime'])
    end_dt = datetime.fromisoformat(data['metadata']['endDateTime'])

    # Insert with all fields from flat schema
    client.execute(f'''
        INSERT INTO {config['table_crop_analysis']} (
            crop, alternate_names, color, confidence, overall_description,
            growth_stage, estimated_age_months, growth_description,
            overall_health, vigor_score, disease_indicators, pest_indicators, stress_indicators, health_description,
            planting_pattern, plant_density, field_size_estimate, crop_uniformity, weed_presence, field_description,
            setting, terrain, surrounding_vegetation, infrastructure_visible, weather_conditions, environment_description,
            moisture_level, soil_visibility, irrigation_evidence, season_indication, conditions_description,
            farming_type, management_quality, harvest_readiness, estimated_months_to_harvest, management_description,
            people_present, people_count, people_description, activities_observed, people_confidence_score,
            equipment_present, equipment_count, equipment_types, equipment_description, equipment_condition, equipment_usage, equipment_confidence_score,
            animals_present, total_animal_count, cattle_count, poultry_count, goats_count, sheep_count, pigs_count, horses_count, other_livestock_count, wild_animals_count,
            animal_types_identified, animal_description, animal_activity, animal_health_indicators, integration_with_crops, animals_confidence_score,
            recommendations, recommendations_summary,
            semantic_tags, search_context,
            image_quality, lighting_conditions, viewing_angle, coverage_area, visual_description,
            text_embedding, image_embedding, hybrid_embedding,
            image_path, startDateTime, endDateTime, duration
        ) VALUES
    ''', [(
        # Basic crop identification
        data['crop'],
        data['alternate_names'],
        data['color'],
        data['confidence'],
        data.get('overall_description', ''),

        # Growth stage
        data['growth_stage']['stage'],
        data['growth_stage']['estimated_age_months'],
        data['growth_stage']['description'],

        # Health assessment
        data['health_assessment']['overall_health'],
        data['health_assessment']['vigor_score'],
        data['health_assessment']['disease_indicators'],
        data['health_assessment']['pest_indicators'],
        data['health_assessment']['stress_indicators'],
        data['health_assessment'].get('health_description', ''),

        # Field characteristics
        data['field_characteristics']['planting_pattern'],
        data['field_characteristics']['plant_density'],
        data['field_characteristics']['field_size_estimate'],
        data['field_characteristics']['crop_uniformity'],
        data['field_characteristics']['weed_presence'],
        data['field_characteristics'].get('field_description', ''),

        # Environmental context
        data['environmental_context']['setting'],
        data['environmental_context']['terrain'],
        data['environmental_context']['surrounding_vegetation'],
        data['environmental_context']['infrastructure_visible'],
        data['environmental_context']['weather_conditions'],
        data['environmental_context'].get('environment_description', ''),

        # Growing conditions
        data['growing_conditions']['moisture_level'],
        data['growing_conditions']['soil_visibility'],
        data['growing_conditions']['irrigation_evidence'],
        data['growing_conditions']['season_indication'],
        data['growing_conditions'].get('conditions_description', ''),

        # Agricultural insights
        data['agricultural_insights']['farming_type'],
        data['agricultural_insights']['management_quality'],
        data['agricultural_insights']['harvest_readiness'],
        data['agricultural_insights']['estimated_months_to_harvest'],
        data['agricultural_insights'].get('management_description', ''),

        # People detection
        data.get('people_detection', {}).get('people_present', False),
        data.get('people_detection', {}).get('people_count', 0),
        data.get('people_detection', {}).get('people_description', ''),
        data.get('people_detection', {}).get('activities_observed', []),
        data.get('people_detection', {}).get('people_confidence_score', 0.0),

        # Equipment detection
        data.get('equipment_detection', {}).get('equipment_present', False),
        data.get('equipment_detection', {}).get('equipment_count', 0),
        data.get('equipment_detection', {}).get('equipment_types', []),
        data.get('equipment_detection', {}).get('equipment_description', ''),
        data.get('equipment_detection', {}).get('equipment_condition', ''),
        data.get('equipment_detection', {}).get('equipment_usage', ''),
        data.get('equipment_detection', {}).get('equipment_confidence_score', 0.0),

        # Animal detection
        data.get('animal_detection', {}).get('animals_present', False),
        data.get('animal_detection', {}).get('total_animal_count', 0),
        data.get('animal_detection', {}).get('cattle_count', 0),
        data.get('animal_detection', {}).get('poultry_count', 0),
        data.get('animal_detection', {}).get('goats_count', 0),
        data.get('animal_detection', {}).get('sheep_count', 0),
        data.get('animal_detection', {}).get('pigs_count', 0),
        data.get('animal_detection', {}).get('horses_count', 0),
        data.get('animal_detection', {}).get('other_livestock_count', 0),
        data.get('animal_detection', {}).get('wild_animals_count', 0),
        data.get('animal_detection', {}).get('animal_types_identified', []),
        data.get('animal_detection', {}).get('animal_description', ''),
        data.get('animal_detection', {}).get('animal_activity', []),
        data.get('animal_detection', {}).get('animal_health_indicators', ''),
        data.get('animal_detection', {}).get('integration_with_crops', ''),
        data.get('animal_detection', {}).get('animals_confidence_score', 0.0),

        # Recommendations
        data['recommendations'],
        data.get('recommendations_summary', ''),

        # Semantic search fields
        data.get('semantic_tags', []),
        data.get('search_context', ''),

        # Image metadata
        data['image_metadata']['image_quality'],
        data['image_metadata']['lighting_conditions'],
        data['image_metadata']['viewing_angle'],
        data['image_metadata']['coverage_area'],
        data['image_metadata'].get('visual_description', ''),

        # Embedding vectors (computed in real-time)
        text_embedding,
        image_embedding,
        hybrid_embedding,

        # Additional metadata
        image_path or '',
        start_dt,
        end_dt,
        data['metadata']['duration']
    )])