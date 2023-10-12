**Group : Anthos**
![image](https://user-images.githubusercontent.com/31825973/235280262-567df52b-6bdf-4bfc-a0ff-343c4f0beb5b.png)

---

** Contributions **

<details>
<summary> Munaganuru Siva Nagi Reddy - Component (3, 5, 6) </summary>
As part of my project responsibilities, I took charge of configuring the output S3 buckets, and also 
worked on installing OpenStack in an Azure VM and configuring the necessary network settings such as security groups, assigning a floating ip, and creating a new private network and a subnet. Then i have uploaded a Centos minimal to the glance and created a VM using Centos and set up the network reachability of the VM. I also set up the CentOS environment with the required tools and libraries, enabling seamless integration with Git and Python. This allowed us to efficiently monitor the Simple Queue Service (SQS) for new messages and trigger the AWS Lambda function as needed, ensuring the smooth operation of our smart classroom assistant application.
Also updated the dynamo DB with student academic records and have provided permissions for the lambda function so that it can fetch the student records and then these outputs are stored in the output bucket in the form of CSV.

## </details>

<details>
<summary> Sai Varun Reddy Mullangi - Component (3, 4) </summary>
As part of my project responsibilities, I worked on Component 4 which involves frame extraction and recognition. To facilitate debugging, I set up logging to capture and analyze any errors encountered during the project setup on AWS. 
I focused on the face recognition event handler, which triggers the processing of videos when there is an object create event, such as a video uploaded to S3. Using ffmpeg, I divided the video into frames and stored them in a temporary folder as Lambda has write access only to the tmp folder. 
Next, I used the face recognition library to detect faces among the frames, and optimized the process by implementing a loop-breaking logic that stops the processing once the first match is found, thereby avoiding processing of the remaining frames. Finally, based on the name of the identified face, I queried the DynamoDB to retrieve the academic information of the person and wrote the information into a CSV for storage in the S3 bucket.
Further I have also worked on integrating an AWS Lambda function with an AWS SQS queue to achieve a fully-managed serverless architecture for my project. To achieve this, I wrote a Python code that uses the boto3 library to receive messages from an SQS queue and trigger a Lambda function, passing information from the message body as a payload. The Lambda function then retrieves a CSV file from S3, extracts a specific line of content from the file, and prints it along with the object key to the console.

## </details>

<details>
<summary> Pavan Krishna Reddy Madireddy – Component (1, 3) </summary>
As part of the project, I worked on two parts, the first one being the Dockerfile where I had to go through the given file and understanding all the details within the file. To complete the project I had to make some customizations like adding some extra files using COPY command. Then I built the docker image locally using the docker client which was saved in my macbook. Then I assigned a tag and uploaded it to Amazon Elastic Cloud Registry private repository which can be used in further steps of the projects to create a lambda function from the image. 
I also worked on the workload generator part where I had run various tests and verified the sanity of the output produced by the lambda functions. The workload generator uploads videos into input S3 bucket which inturn triggers the lambda functions as configured and generated the output csv files into output buckets. Verified the output csv files data with the expected output.
I also worked on setting up the virtual machine in Openstack by uploading the centos image and installing python and all the dependencies required to run trigger.py which is the script which triggers lambda on receiving messages from SQS.

</details>

---

_AWS credentials_
Root Email -
Password -

---

Pem file - in the folder

Pem file - in the folder

---

S3 Bucket Name - anthosccproj3input, anthosccproj3output

---

## Steps for running the Hybrid Cloud

- Run the trigger.py script in the vm created in openstack which will tigger the lambda on upload of a video in s3 bucket.
