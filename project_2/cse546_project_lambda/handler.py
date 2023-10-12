from boto3 import client as boto3_client
import face_recognition
import pickle
import urllib.parse
import boto3
import json
import os
import numpy as np
import pandas as pd
from io import StringIO
import logging


input_bucket = "cse546proj2"
output_bucket = "cse546proj2output"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("wehghosenogwneog")

s3 = boto3.client(
	's3',
	aws_access_key_id="",
	aws_secret_access_key=""
)

dynamoDB  = boto3.client(
	"dynamodb",
	region_name='us-east-1',
	aws_access_key_id="",
	aws_secret_access_key=""
)

# specify the table name and partition key value
table_name = 'Student'
partition_key_value = 'name'


# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data


def face_recognition_handler(event, context):
	logger.info("Received event: {}".format(json.dumps(event, indent=2)))

	# Get the object from the event and show its content type
	bucket = event['Records'][0]['s3']['bucket']['name']
	key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
	try:
		video_path = "/tmp/" + key
		response = s3.get_object(Bucket=bucket, Key=key)
		with open(video_path, 'wb') as f:
			f.write(response['Body'].read())
		path = "/tmp/frames"
		try:
			os.mkdir(path)
		except Exception as e:
			print(e)
        
		os.system("ffmpeg -i " + video_path + " -r 1 " + str(path) + "/image-%3d.jpeg")
		encodings = open_encoding("./encoding")

		for filename in os.listdir(path):
			image = face_recognition.load_image_file(path + "/" + filename)
			face_encodings = face_recognition.face_encodings(image)
			matches = face_recognition.compare_faces(encodings['encoding'], face_encodings[0])

			face_distances = face_recognition.face_distance(encodings['encoding'], face_encodings[0])
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = encodings['name'][best_match_index]
				logger.info("name {}".format(name))
				# query the table with the partition key value
				response = dynamoDB.get_item(
				  TableName=table_name,
				  Key={
					'name': {'S': str(name)}
				  }
				)
				major = ""
				year = ""
				try:
					major = response["Item"]["major"]["S"]
					year = response["Item"]["year"]["S"]
				except:
					logger.info("Error in getting major and year")
				data = {
				  "name": name,
				  "major": major,
				  "year": year
				}
				df = pd.DataFrame([data])

				# write the CSV data to a buffer`
				csv_buffer = StringIO()
				df.to_csv(csv_buffer, index=False)

				# upload the CSV file to S3
				file_key = key.split(".")[0] + ".csv"
				s3.put_object(Bucket=output_bucket, Key=file_key, Body=csv_buffer.getvalue())
				logger.info("files uploaded")
				return "Hello World!"
				
	except Exception as e:
		print(e)
		print(
			'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as '
			'this function.'.format(
				key, bucket))
		raise e