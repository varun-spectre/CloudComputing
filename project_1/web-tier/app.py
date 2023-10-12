from flask import Flask, request
import boto3
import io
import base64
import json
import time
import threading
import logging


app = Flask(__name__)
app.config['TIMEOUT'] = 600

# Amazon SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

# Dictionaries to store the response message from the response queue corresponding to each client
responses = {}
client_to_thread = {}

def poll_response_queue():
    """
    Poll the response queue to receive messages
    """
    while True:
        # Receive a message from the response queue
        thread_id = threading.get_ident()
        print(f"Thread {thread_id} is polling the response queue")
        # print(responses)

        while True:

            response = sqs.receive_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/275316137412/ResponseQueue',
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )
            if 'Messages' not in response:
                # No messages in the queue, wait for a few seconds before polling again
                # time.sleep(5)
                continue

            else:
                for message in response['Messages']:
                    # Get the image name from the message body
                    response_body = json.loads(message['Body'])
                    image_name = response_body['image_name']

                    # Add the response message to the responses dictionary
                    responses[image_name] = response_body

                    # Notify the thread waiting on this response
                    if image_name in client_to_thread:
                        client_to_thread[image_name].set()

                    sqs.delete_message(
                        QueueUrl='https://sqs.us-east-1.amazonaws.com/275316137412/ResponseQueue',
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    print(
                        f"Message {message['MessageId']} deleted from response queue")
            # time.sleep(1)


# Start the response queue polling thread
thread = threading.Thread(target=poll_response_queue)
thread.start()


@app.route('/classify', methods=['POST'])
def classify():
    image = request.files['myfile'].read()
    image_encoded = base64.b64encode(image).decode('utf-8')

    thread_id1 = threading.get_ident()


    image_name = request.files['myfile'].filename
    req = {'image': image_encoded, 'image_name': image_name}
    json_req = json.dumps(req)
    print(f"Thread {thread_id1} is sending {image_name} to the request queue")
    # Send the image to the request queue
    sqs.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/275316137412/RequestQueue',
        MessageBody=json_req
    )

    # Create an event object to wait on the response
    event = threading.Event()
    client_to_thread[image_name] = event

    # Wait until the response is received
    event.wait()

    # Get the response message corresponding to this client
    response = responses.pop(image_name, None)
    # print(f"Thread {thread_id1} is sending {image_name} to the client")

    logging.info("Thread %s is sending %s to the client", thread_id1, image_name)
    # Return the response to the client
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
