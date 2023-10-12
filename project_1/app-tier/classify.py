from flask import Flask, request, jsonify
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from urllib.request import urlopen
from PIL import Image
import numpy as np
import json
import sys
import io
import boto3
import os
import base64
import signal
import logging,time
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


s3 = boto3.client('s3')
sqs = boto3.client('sqs', region_name='us-east-1')

request_queue_url = 'https://sqs.us-east-1.amazonaws.com/275316137412/RequestQueue'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/275316137412/ResponseQueue'



def store_image_in_s3(image_data, image_name):
    s3.put_object(Bucket='input-bucket-541p1',
                  Key=image_name, Body=image_data)


def store_classification_in_s3(classification_result, image_name):
    s3.put_object(Bucket='output-bucket-cse541p1',
                  Key=image_name, Body=classification_result)


# app = Flask(__name__)

loop = True


def classify_from_queue(image, image_name ): 

        # Load the model
        model = models.resnet18(pretrained=True)
        model.eval()

        # Transform image and make predictions
        img_tensor = transforms.ToTensor()(image).unsqueeze_(0)
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs.data, 1)

        # Load the labels
        with open('/home/ubuntu/Cloud_computing_546/project_1/app-tier/imagenet-labels.json') as f:
            labels = json.load(f)
        result = labels[np.array(predicted)[0]]
        logging.info('predicted the image: %s',image_name) 
        time.sleep(5)
        return result

        
        # # Return the result as a JSON response
        # return jsonify({"classification": result})


def signal_handler(sig, frame):
    # Perform any necessary cleanup operations here
    logging.FATAL('Received SIGTERM signal, shutting down gracefully...')
    loop = False
    sys.exit(0)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    signal.signal(signal.SIGTERM, signal_handler)
    while loop:
        request = sqs.receive_message(QueueUrl=request_queue_url)

        if 'Messages' in request:
            print("message received")
            request = request['Messages'][0]
            receipt_handle = request['ReceiptHandle']
            
            message_body = json.loads(request['Body'])
                
            image = base64.b64decode(message_body['image'])
            # print(image)
            image = Image.open(io.BytesIO(image))
            image_name = message_body['image_name']

            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            buffer.seek(0)

            store_image_in_s3(buffer.read(), image_name)

            result = classify_from_queue(image, image_name)

            store_classification_in_s3(json.dumps({image_name.strip(
                '.JPEG'): result}, ensure_ascii=False), image_name.strip('.JPEG'))

            response = {'image_name': image_name, 'classification': result}
            print(response)
            sqs.send_message(QueueUrl=response_queue_url,
                            MessageBody=json.dumps(response))

            sqs.delete_message(QueueUrl=request_queue_url,
                               ReceiptHandle=receipt_handle)

        # else:
        #     print('No messages in queue')



        





# @app.route("/classify", methods=["POST"])
# def classify():
#     # Get image from request
    

#     image = Image.open(io.BytesIO(request.files['image'].read()))
#     image_name = request.files['image'].filename

#     buffer = io.BytesIO()
#     image.save(buffer, format='JPEG')
#     buffer.seek(0)


#     store_image_in_s3(buffer.read(), image_name)



#     # Load the model
#     model = models.resnet18(pretrained=True)
#     model.eval()

#     # Transform image and make predictions
#     img_tensor = transforms.ToTensor()(image).unsqueeze_(0)
#     outputs = model(img_tensor)
#     _, predicted = torch.max(outputs.data, 1)

#     # Load the labels
#     with open('./imagenet-labels.json') as f:
#         labels = json.load(f)
#     result = labels[np.array(predicted)[0]]


#     store_classification_in_s3(json.dumps({image_name.strip('.JPEG'): result},ensure_ascii=False), image_name.strip('.JPEG'))

#     # Return the result as a JSON response
#     return jsonify({"classification": result})


# if __name__ == "__main__":
#     # logging.basicConfig(level=logging.INFO)
#     app.run(host="0.0.0.0",port = "8000",debug=True)
