import requests
import json
import random
from datetime import datetime
import argparse
import base64

# URL of the producer endpoint
url = 'http://0.0.0.0:80/producer'

# Generate a random JSON body request

def generate_request(num_preds):
    device_id = 'device_' + str(random.randint(1, 100))
    client_id = 'client_' + str(random.randint(1, 100))
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    license_id = 'license_' + str(random.randint(1, 100))
    
    preds = []

    for i in range(num_preds):
        image_frame = 'image' + str(random.randint(1, 100))
        image_frame = base64.b64encode(image_frame.encode("ascii"))
        prob = random.random()
        tags = ['tag' + str(random.randint(1, 100)) for _ in range(random.randint(1,3))]
        preds.append({
                'image_frame': image_frame.decode("utf-8"),
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

# Send requests to the producer endpoint
def main(num_msgs, num_preds):
    for i in range(num_msgs):
        request_data = generate_request(num_preds)
        headers = {'Content-Type': 'application/json',
                    'accept': 'application/json'}
        
        response = requests.post(url, data=json.dumps(request_data), headers=headers)
        print(f'Response for request {i + 1}: {response.status_code}')
    print(f'Count of rows in CSV is {num_msgs*num_preds}')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--num_msgs', type=int, required=True, help="Kindly provide num of messages")
    parser.add_argument('--num_preds', type=int, required=True, help="Kindly provide num of preds in each message")
    args = parser.parse_args()

    main(args.num_msgs, args.num_preds)

