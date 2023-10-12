import boto3
import json

# open the JSON file in read mode
with open('./student_data.json', 'r') as f:
    # parse the JSON data using the json.load() method
    data = json.load(f)

new_data = []
for item in data:
  temp = {}
  for k,v in item.items():
    if k=="id":
      temp[k] = {"N" : str(v)}
    else:
      temp[k] = {"S" : str(v)}
  new_data.append(temp)

# create a DynamoDB client
dynamodb = boto3.client(
    "dynamodb",
    region_name='us-east-1',
    aws_access_key_id="",
    aws_secret_access_key=""
)

# specify the table name
table_name = 'Student'

# upload the data to the table
for item in new_data:
  response = dynamodb.put_item(
      TableName=table_name,
      Item=item
  )

# print the response
print(response)
