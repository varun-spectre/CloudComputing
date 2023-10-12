**Group : Anthos**

![image](https://user-images.githubusercontent.com/28705784/227815591-d1f30349-9e09-43c2-bd36-86123e80bcbf.png)

---

** Contributions **

<details>
<summary> Munaganuru Siva Nagi Reddy - Component (2,4,5) </summary>
As part of my project responsibilities, I took charge of configuring the Input and out S3 buckets and attached for lambda attached a trigger to the input bucket(component 2). So that whenever a user uploads a video file in the form of mp4 into it a trigger is sent to invoke the lambda function. And also updated the dynamo DB with student academic records and have provided permissions for the lambda function so that it can fetch the student records and then these outputs are stored in the output bucket in the form of CSV.

## </details>

<details>
<summary> Sai Varun Reddy Mullangi - Component (3) </summary>
As part of my project responsibilities, I worked on Component 3 which involves frame extraction and recognition. To facilitate debugging, I set up logging to capture and analyze any errors encountered during the project setup on AWS.
I focused on the face recognition event handler, which triggers the processing of videos when there is an object create event, such as a video uploaded to S3. Using ffmpeg, I divided the video into frames and stored them in a temporary folder as Lambda has write access only to the tmp folder.
Next, I used the face recognition library to detect faces among the frames, and optimized the process by implementing a loop-breaking logic that stops the processing once the first match is found, thereby avoiding processing of the remaining frames. Finally, based on the name of the identified face, I queried the DynamoDB to retrieve the academic information of the person and wrote the information into a CSV for storage in the S3 bucket.

## </details>

<details>
<summary> Pavan Krishna Reddy Madireddy – Component (1, 3) </summary>
As part of the project, I worked on two parts, the first one being the Dockerfile where I had to go through the given file and understanding all the details within the file. To complete the project I had to make some customizations like adding some extra files using COPY command. Then I built the docker image locally using the docker client which was saved in my macbook. Then I assigned a tag and uploaded it to Amazon Elastic Cloud Registry private repository which can be used in further steps of the projects to create a lambda function from the image.
I also worked on the workload generator part where I had run various tests and verified the sanity of the output produced by the lambda functions. The workload generator uploads videos into input S3 bucket which inturn triggers the lambda functions as configured and generated the output csv files into output buckets. Verified the output csv files data with the expected output.

</details>

---

_AWS credentials_

---

Pem file - - in the folder

---

S3 Bucket Name - cse546proj2, cse546proj2output

---

## Steps for running the Image Recognition as a service

- Run the workload.py script which will upload the videos into the input bucket and then check the responses in the ot
