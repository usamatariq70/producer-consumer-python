import requests
import json
import random
from datetime import datetime

# URL of the producer endpoint
url = 'http://0.0.0.0:80/producer'

# Generate a random JSON body request

def generate_request():
    device_id = 'device_' + str(random.randint(1, 100))
    client_id = 'client_' + str(random.randint(1, 100))
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    license_id = 'license_' + str(random.randint(1, 100))
    
    preds = []

    for i in range(2):
        image_frame = 'image' + str(random.randint(1, 100))
        prob = random.random()
        tags = ['tag' + str(random.randint(1, 100)) for _ in range(random.randint(1,3))]
        preds.append({
                'image_frame': image_frame,
                'prob': prob,
                'tags': tags
            })
    
    request = {
        'device_id': device_id,
        'client_id': client_id,
        'created_at': created_at,
        'data': {
            'license_id': license_id,
            'preds': preds
        }
    }
    return request

# Send 1000 requests to the producer endpoint
for i in range(1000):
    request_data = generate_request()
    headers = {'Content-Type': 'application/json',
                'accept': 'application/json'}
    
    response = requests.post(url, data=json.dumps(request_data), headers=headers)
    print(f'Response for request {i + 1}: {response.status_code}')
print(f'Count of rows in CSV is {2*1000}')
