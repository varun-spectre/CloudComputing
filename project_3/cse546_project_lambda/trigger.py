import boto3
import time
import json
import threading

ACCESS_KEY = ''
SECRET_KEY = ''
region = 'us-east-1'

print("Starting the watcher")

s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
request_queue_url = 'https://sqs.us-east-1.amazonaws.com/226375241842/CCProject3'
lambda_client = boto3.client('lambda', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=region)
loop = True

def lambda_trigger(message):
    receipt_handle = message['ReceiptHandle']
    message_body = eval(message['Body'])

    print("message received ", message_body["Records"][0]["s3"]["object"]["key"])

    payload_data = {
        'bucket': message_body["Records"][0]["s3"]["bucket"]["name"],
        'key': message_body["Records"][0]["s3"]["object"]["key"]
    }
    payload = json.dumps(payload_data)

    response = lambda_client.invoke(
        FunctionName='ccproj3',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=payload
    )

    sqs.delete_message(QueueUrl=request_queue_url,
                        ReceiptHandle=receipt_handle)

    file = message_body["Records"][0]["s3"]["object"]["key"].split(".")[0] + ".csv"
    response = s3.get_object(Bucket="anthosccproj3output", Key=file)
    content = response['Body'].read().decode('utf-8').split('\n')[1]
    print(message_body["Records"][0]["s3"]["object"]["key"], content)

while loop:
    sqs_response = sqs.receive_message(
        QueueUrl=request_queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20
    )
    print("Looking for new messages")
    if 'Messages' not in sqs_response:
        time.sleep(5)
        continue
    else:
        for message in sqs_response['Messages']:
            thread = threading.Thread(target=lambda_trigger, args=(message,))
            thread.start()
    time.sleep(5)