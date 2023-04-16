This project is a producer-consumer system that receives JSON messages from a producer endpoint, processes the messages, and writes the data to a CSV file.

# Setup

## Prerequisites

- Docker installed on your system


## Installation

- Clone the repository: git clone https://github.com/usamatariq70/producer-consumer-python.git
- Change to the project directory: cd producer-consumer-python
- To create and run all docker containers use the following command:
```bash
    docker-compose up --build
```


## Sample data
```json
{
	"device_id": str,
	"client_id": str,
	"created_at": str, # timestamp, e.g. '2023-02-07 14:56:49.386042'
	"data": {
		"license_id": str,
		"preds": [
			{
				"image_frame": str, # base64 string
				"prob": float,
				"tags": str[]
			},
			...
		] 
	}
}
```


## Usage

- Run the docker containers using docker compose command mentioned above
- Check the logs of the containers to ensure it's running successfully
- Post the data to this cURL:
```
curl -X 'POST' \
  'http://0.0.0.0/publish' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d DATA
```
- Posted data will get into RabbitMQ queue and consumer will process it update it to CSV
- You can find the CSV file named output.csv in code folder within the consumer container
- I have also mounted the consumer folder with consumer container, therefore you can find output.csv in consumer folder too without getting into the container (You will be able to find output.csv, once you start posting the data)


## Test Script

To test the whole ecosystem, you can run the provided test_script.py. It will post random generated data to producer and you will be able to see the result in output.csv in consumer folder

To run the test_script.py, kindly install requests library using the below given command:
```bash
    pip install requests
```

You are supposed to provide number of messages and number of preds to run the test script. Sample command is:
```bash
    python test_script.py --num_msgs 1000 --num_preds 2
```