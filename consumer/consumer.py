import pika
import csv
import json
import logging

header = True

#Function to get all the keys from the JSON, to create a header
def get_all_keys(data):
    keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            keys.extend(get_all_keys(value))
        elif isinstance(value, list):
            if value:
                if isinstance(value[0], dict):
                    keys.extend(get_all_keys(value[0]))
                else:
                    keys.append(key)
        else:
            keys.append(key)
    return keys

#Function to parse incoming message, turn it into a form of row and write it to CSV
def process_message(msg, keys, filename):
    data = msg["data"]
    preds = data["preds"]
    
    #Creating base dictionary having all values other than preds
    single_message = {k: v for k, v in msg.items() if k in keys}
    single_message.update({k: v for k, v in data.items() if k in keys})
    
    with open(filename, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        
        for item in preds:
            #Reading preds one by one and writing into CSV as a seperate row
            writer.writerow({**single_message, **item})
            


def main():
    #Creating connection with rabbitmq, using default cridentials
    credentials = pika.PlainCredentials(username='guest', password='guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-host', credentials=credentials))
    channel = connection.channel()
    
    #Declaring queue in which data is pushed by the producer
    channel.queue_declare(queue='preds')

    #Receiving data from queue
    def callback(ch, method, properties, body):
        global header

        message = json.loads(body.decode('utf-8'))
        
        keys = get_all_keys(message)
        filename = 'output.csv'
        
        #Adding header into CSV if needed
        if header:
            with open(filename, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()

            header = False
        
        process_message(message, keys, filename)
        logging.info("CSV updated successfully...")
    
    #Continously reading messages from queue, whenever it get populated
    channel.basic_consume(queue='preds', on_message_callback=callback, auto_ack=True)

    logging.info("Waiting for messages. To exit press CTRL+C...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
