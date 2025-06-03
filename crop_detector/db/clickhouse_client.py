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

def save_to_clickhouse_detailed(config: dict, data: dict):
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
            crop, alternate_names, color, confidence,
            growth_stage, estimated_age_months, growth_description,
            overall_health, vigor_score, disease_indicators, pest_indicators, stress_indicators,
            planting_pattern, plant_density, field_size_estimate, crop_uniformity, weed_presence,
            setting, terrain, surrounding_vegetation, infrastructure_visible, weather_conditions,
            moisture_level, soil_visibility, irrigation_evidence, season_indication,
            farming_type, management_quality, harvest_readiness, estimated_months_to_harvest,
            recommendations,image_quality, lighting_conditions, viewing_angle, coverage_area,
            startDateTime, endDateTime, duration
        ) VALUES
    ''', [(
        data['crop'],
        data['alternate_names'],
        data['color'],
        data['confidence'],

        data['growth_stage']['stage'],
        data['growth_stage']['estimated_age_months'],
        data['growth_stage']['description'],

        data['health_assessment']['overall_health'],
        data['health_assessment']['vigor_score'],
        data['health_assessment']['disease_indicators'],
        data['health_assessment']['pest_indicators'],
        data['health_assessment']['stress_indicators'],

        data['field_characteristics']['planting_pattern'],
        data['field_characteristics']['plant_density'],
        data['field_characteristics']['field_size_estimate'],
        data['field_characteristics']['crop_uniformity'],
        data['field_characteristics']['weed_presence'],

        data['environmental_context']['setting'],
        data['environmental_context']['terrain'],
        data['environmental_context']['surrounding_vegetation'],
        data['environmental_context']['infrastructure_visible'],
        data['environmental_context']['weather_conditions'],

        data['growing_conditions']['moisture_level'],
        data['growing_conditions']['soil_visibility'],
        data['growing_conditions']['irrigation_evidence'],
        data['growing_conditions']['season_indication'],

        data['agricultural_insights']['farming_type'],
        data['agricultural_insights']['management_quality'],
        data['agricultural_insights']['harvest_readiness'],
        data['agricultural_insights']['estimated_months_to_harvest'],

        data['recommendations'],

        data['image_metadata']['image_quality'],
        data['image_metadata']['lighting_conditions'],
        data['image_metadata']['viewing_angle'],
        data['image_metadata']['coverage_area'],

        start_dt,
        end_dt,
        data['metadata']['duration']
    )])

