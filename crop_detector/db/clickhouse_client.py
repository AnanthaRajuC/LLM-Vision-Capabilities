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
    Enhanced version of your existing create_text_for_embedding function
    Optimized for agricultural crop analysis
    """
    text_components = []

    # Primary crop identification (highest weight)
    text_components.append(f"Crop: {data['crop']}")
    if data.get('alternate_names'):
        text_components.append(f"Also known as: {', '.join(data['alternate_names'])}")

    # Overall description
    if data.get('overall_description'):
        text_components.append(data['overall_description'])

    # Growth stage information
    growth_info = data.get('growth_stage', {})
    if growth_info.get('stage'):
        text_components.append(f"Growth stage: {growth_info['stage']}")
        if growth_info.get('estimated_age_months'):
            text_components.append(f"Age: {growth_info['estimated_age_months']} months")
    if growth_info.get('description'):
        text_components.append(growth_info['description'])

    # Health assessment (critical for similarity)
    health_info = data.get('health_assessment', {})
    if health_info.get('overall_health'):
        text_components.append(f"Health: {health_info['overall_health']}")
    if health_info.get('disease_indicators') and health_info['disease_indicators'] != ['empty list']:
        text_components.append(f"Diseases: {', '.join(health_info['disease_indicators'])}")
    if health_info.get('pest_indicators') and health_info['pest_indicators'] != ['empty list']:
        text_components.append(f"Pests: {', '.join(health_info['pest_indicators'])}")
    if health_info.get('stress_indicators') and 'none_detected' not in health_info['stress_indicators']:
        text_components.append(f"Stress: {', '.join(health_info['stress_indicators'])}")
    if health_info.get('health_description'):
        text_components.append(health_info['health_description'])

    # Field characteristics
    field_info = data.get('field_characteristics', {})
    field_details = []
    if field_info.get('planting_pattern'):
        field_details.append(f"planted in {field_info['planting_pattern']}")
    if field_info.get('plant_density'):
        field_details.append(f"{field_info['plant_density']} density")
    if field_info.get('crop_uniformity'):
        field_details.append(f"{field_info['crop_uniformity']} uniformity")
    if field_details:
        text_components.append("Field characteristics: " + ", ".join(field_details))
    if field_info.get('field_description'):
        text_components.append(field_info['field_description'])

    # Environmental context
    env_info = data.get('environmental_context', {})
    env_details = []
    if env_info.get('setting'):
        env_details.append(f"{env_info['setting']} setting")
    if env_info.get('terrain'):
        env_details.append(f"{env_info['terrain']} terrain")
    if env_info.get('weather_conditions'):
        env_details.append(f"{env_info['weather_conditions']} weather")
    if env_details:
        text_components.append("Environment: " + ", ".join(env_details))
    if env_info.get('environment_description'):
        text_components.append(env_info['environment_description'])

    # Growing conditions
    conditions_info = data.get('growing_conditions', {})
    condition_details = []
    if conditions_info.get('moisture_level'):
        condition_details.append(f"{conditions_info['moisture_level']} moisture")
    if conditions_info.get('irrigation_evidence') and conditions_info['irrigation_evidence'] != 'not_visible':
        condition_details.append(f"{conditions_info['irrigation_evidence']} irrigation")
    if conditions_info.get('season_indication'):
        condition_details.append(f"{conditions_info['season_indication']}")
    if condition_details:
        text_components.append("Conditions: " + ", ".join(condition_details))
    if conditions_info.get('conditions_description'):
        text_components.append(conditions_info['conditions_description'])

    # Agricultural insights
    insights_info = data.get('agricultural_insights', {})
    if insights_info.get('farming_type'):
        text_components.append(f"Farming: {insights_info['farming_type']}")
    if insights_info.get('management_quality'):
        text_components.append(f"Management: {insights_info['management_quality']}")
    if insights_info.get('harvest_readiness'):
        text_components.append(f"Harvest readiness: {insights_info['harvest_readiness']}")
    if insights_info.get('management_description'):
        text_components.append(insights_info['management_description'])

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

    # Join all components
    comprehensive_text = ". ".join([comp.strip() for comp in text_components if comp.strip()])
    return comprehensive_text


def save_to_clickhouse_with_embeddings(config: dict, data: dict, image_path: str = None):
    """
    Enhanced version of your save_to_clickhouse_detailed function that computes embeddings during insert
    This replaces your existing save_to_clickhouse_detailed function
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

    # Insert with embeddings
    client.execute(f'''
        INSERT INTO {config['table_crop_analysis']} (
            crop, alternate_names, color, confidence, overall_description,
            growth_stage, estimated_age_months, growth_description,
            overall_health, vigor_score, disease_indicators, pest_indicators, stress_indicators, health_description,
            planting_pattern, plant_density, field_size_estimate, crop_uniformity, weed_presence, field_description,
            setting, terrain, surrounding_vegetation, infrastructure_visible, weather_conditions, environment_description,
            moisture_level, soil_visibility, irrigation_evidence, season_indication, conditions_description,
            farming_type, management_quality, harvest_readiness, estimated_months_to_harvest, management_description,
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