from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
import json
from datetime import datetime
import pika

#Model for reading Preds dictionary from JSON
class Preds(BaseModel):
    image_frame: str
    prob: float
    tags: List[str]

#Model for reading Data dictionary from JSON 
class Data(BaseModel):
    license_id: str
    preds: List[Preds]

#Model for reading Message from JSON
class Message(BaseModel):
    device_id: str
    client_id: str
    created_at: str
    data: Data

    #Checking the validation of created_at
    @validator('created_at')
    def validate_created_at(created_at: str) -> str:
        try:
            #Assuming example mentioned in the requirement will always be the valid timestamp
            datetime.strptime(created_at, r'%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            raise ValueError('created_at must be a valid timestamp')
        return created_at

app = FastAPI()

@app.post("/producer")
async def post_message(message:Message):
    try:
        #Creating connection with rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-host'))
        channel = connection.channel()
        
        #Declaring queue to push data in
        channel.queue_declare(queue='preds')

        #Getting received message
        requested_message = json.loads(message.json())

        #If the prob field is less than 0.25, append the tag low_prob in the tags list.
        for pred in requested_message['data']['preds']:
            if pred['prob'] < 0.25:
                pred['tags'].append('low_prob')

        #Pushing message to declared queue
        channel.basic_publish(exchange='',
                      routing_key='preds',
                      body=json.dumps(requested_message))

        #Closing the connection
        connection.close()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to publish message to RabbitMQ")
        
