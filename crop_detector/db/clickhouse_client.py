from clickhouse_driver import Client
from datetime import datetime

def save_to_clickhouse(config: dict, data: dict):
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
        INSERT INTO {config['table']} 
        (crop, alternate_names, color, confidence, startDateTime, endDateTime, duration)
        VALUES
    ''', [(data['crop'], data['alternate_names'], data['color'], data['confidence'],
           start_dt, end_dt, data['metadata']['duration'])])
