from clickhouse_driver import Client
from datetime import datetime

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


def save_to_clickhouse_with_embeddings(config: dict, data: dict, image_path: str,
                                       text_embedding: list, image_embedding: list,
                                       hybrid_embedding: list):
    """
    Enhanced version that includes pre-computed embeddings
    """
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

        # Embedding vectors
        text_embedding,
        image_embedding,
        hybrid_embedding,

        # Additional metadata
        image_path,
        start_dt,
        end_dt,
        data['metadata']['duration']
    )])


def create_text_for_embedding(data: dict) -> str:
    """
    Helper function to create comprehensive text from all description fields
    for embedding generation
    """
    text_parts = [
        data.get('overall_description', ''),
        data['growth_stage']['description'],
        data['health_assessment'].get('health_description', ''),
        data['field_characteristics'].get('field_description', ''),
        data['environmental_context'].get('environment_description', ''),
        data['growing_conditions'].get('conditions_description', ''),
        data['agricultural_insights'].get('management_description', ''),
        data.get('recommendations_summary', ''),
        data.get('search_context', ''),
        ' '.join(data.get('semantic_tags', [])),
        ' '.join(data['recommendations'])
    ]

    # Filter out empty strings and join
    return ' '.join([part.strip() for part in text_parts if part.strip()])


def batch_save_to_clickhouse(config: dict, data_list: list):
    """
    Batch insert function for better performance with multiple records
    """
    if not data_list:
        return

    client = Client(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

    batch_data = []
    for item in data_list:
        data = item['data']
        image_path = item.get('image_path', '')
        text_embedding = item.get('text_embedding', [])
        image_embedding = item.get('image_embedding', [])
        hybrid_embedding = item.get('hybrid_embedding', [])

        start_dt = datetime.fromisoformat(data['metadata']['startDateTime'])
        end_dt = datetime.fromisoformat(data['metadata']['endDateTime'])

        batch_data.append((
            # All fields as in the single insert function above
            data['crop'],
            data['alternate_names'],
            data['color'],
            data['confidence'],
            data.get('overall_description', ''),
            data['growth_stage']['stage'],
            data['growth_stage']['estimated_age_months'],
            data['growth_stage']['description'],
            data['health_assessment']['overall_health'],
            data['health_assessment']['vigor_score'],
            data['health_assessment']['disease_indicators'],
            data['health_assessment']['pest_indicators'],
            data['health_assessment']['stress_indicators'],
            data['health_assessment'].get('health_description', ''),
            data['field_characteristics']['planting_pattern'],
            data['field_characteristics']['plant_density'],
            data['field_characteristics']['field_size_estimate'],
            data['field_characteristics']['crop_uniformity'],
            data['field_characteristics']['weed_presence'],
            data['field_characteristics'].get('field_description', ''),
            data['environmental_context']['setting'],
            data['environmental_context']['terrain'],
            data['environmental_context']['surrounding_vegetation'],
            data['environmental_context']['infrastructure_visible'],
            data['environmental_context']['weather_conditions'],
            data['environmental_context'].get('environment_description', ''),
            data['growing_conditions']['moisture_level'],
            data['growing_conditions']['soil_visibility'],
            data['growing_conditions']['irrigation_evidence'],
            data['growing_conditions']['season_indication'],
            data['growing_conditions'].get('conditions_description', ''),
            data['agricultural_insights']['farming_type'],
            data['agricultural_insights']['management_quality'],
            data['agricultural_insights']['harvest_readiness'],
            data['agricultural_insights']['estimated_months_to_harvest'],
            data['agricultural_insights'].get('management_description', ''),
            data['recommendations'],
            data.get('recommendations_summary', ''),
            data.get('semantic_tags', []),
            data.get('search_context', ''),
            data['image_metadata']['image_quality'],
            data['image_metadata']['lighting_conditions'],
            data['image_metadata']['viewing_angle'],
            data['image_metadata']['coverage_area'],
            data['image_metadata'].get('visual_description', ''),
            text_embedding,
            image_embedding,
            hybrid_embedding,
            image_path,
            start_dt,
            end_dt,
            data['metadata']['duration']
        ))

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
    ''', batch_data)