**Group : Anthos**

![image](https://user-images.githubusercontent.com/31825973/221442638-8dd5417e-3e4b-45c2-9044-436535243367.png)

---

** Contributions **

<details>
<summary> Munaganuru Siva Nagi Reddy - Component (2,3,4) </summary>

As part of my project responsibilities, I took charge of configuring the web instance by installing all necessary dependencies, including Flask. I was also responsible for developing the core functionality of the web tier, which involved receiving HTTP requests from users with "myfile" as the key for the image. The web tier then processed the image and sent it to the SQS. I ensured that all interactions between the web tier and SQS were seamless and concurrent threads were handled effectively. Additionally, I implemented a background process to continuously poll the response queue and store response messages in a dictionary. This approach ensured that user threads were not blocked while waiting for responses. Furthermore, I leveraged system services and created a new service to perform a Git pull and keep the web tier up-to-date with the latest changes.

## </details>

<details>
<summary> Sai Varun Reddy Mullangi - Component (5, 7) </summary>

I had several crucial tasks to perform. Firstly, I was responsible for preparing the image for classification. To do this, I decoded the image data that was received from the request queue and used the Python Imaging Library (PIL) to open the image. Then, I transformed the image so that it could be used as input to the pretrained deep learning model. Additionally, I implemented the function to store the image in the input S3 bucket. This ensured that the image was properly stored and could be accessed later if needed.
Secondly, my role was to classify the image using the pretrained deep learning model. To do this, I loaded the model and used it to classify the transformed image. I also implemented the function to store the classification result in the output S3 bucket. This ensured that the result of the classification was properly stored and could be used later if needed.
Lastly, I was responsible for monitoring the process of image classification. I implemented a signal handler function to handle the SIGTERM signal and perform any necessary cleanup operations. This was important to ensure that the process of classification was performed efficiently and with minimal errors. Additionally, I added logging statements to monitor the process and to log when an image had been predicted. This provided useful information to users and helped in debugging any issues that may have occurred during the classification process.

## </details>

<details>
<summary> Pavan Krishna Reddy Madireddy – Component (1, 6) </summary>

For implementing the Autoscaling solution for an application that is hosted on Amazon Web Services (AWS). It had two main requirements on a very high level:
To ensure that the number of running instances is always in line with the number of incoming messages to an SQS queue and to ensure that the scaling operation does not take more than 7 minutes. To meet these requirements I have tried two approaches.

Approach 1: Using CloudWatch Alarms

The first approach involved setting up CloudWatch Alarms to monitor two custom metrics. The first metric monitored the number of messages in the SQS queue. The second metric monitored the number of instances currently running in the Auto Scaling Group (ASG). If the number of messages in the queue exceeded a certain threshold, the CloudWatch Alarm triggered an Upscaling policy to add more instances to the ASG. Similarly, if the number of messages in the queue decreased below a certain threshold, the CloudWatch Alarm triggered a Downscaling policy to remove instances from the ASG.
While this approach worked, the problem was that downscaling took 15 minutes and upscaling took 5 minutes. This was because of the "period" attribute in the scaling policy, which was not configurable. Since this was taking more than the threshold of 7 minutes indicated in the project requirements, an alternative approach was tried.

Approach 2: Using a Python Script

Approach 2 is a Python script that runs continuously and monitors the SQS queue's approximate number of visible messages and the number of instances running in the Auto Scaling Group (ASG) using the CloudWatch metric data. The script compares these metrics to predefined thresholds and scales up or down the ASG based on the comparison result.
The script starts by importing the necessary libraries and setting up the AWS SDK clients for CloudWatch, Auto Scaling, and EC2. It then enters a continuous loop that periodically retrieves the CloudWatch metric data for the defined period of the last 5 minutes, with a 30-second granularity. The metric data is retrieved using a CloudWatch GetMetricData API call, which allows for querying multiple metrics at once and performing calculations on the retrieved data. The script then calculates the average number of messages per instance to determine if the ASG needs to be scaled up or down. The calculated value is then compared to the predefined thresholds to determine the desired number of instances in the ASG. These thresholds can be adjusted to suit the specific needs of the application. The script then retrieves the current desired capacity of the ASG and If the desired capacity is not equal to the calculated desired capacity, the script updates the desired capacity of the ASG using the Auto Scaling. After updating the desired capacity, the script sleeps for 30 seconds before starting the loop again to ensure that the new instances have time to spin up before checking the metrics again.
Overall, the second approach provides a more flexible and customizable solution for scaling the ASG based on the SQS queue's message count, allowing for fine-tuning of the scaling thresholds and reducing the scaling time to a few minutes, as opposed to the 15-minute minimum for CloudWatch alarms.

</details>

---

## _AWS credentials_

---

Pem file - - in the folder

---

Web-tier Url - Currently Not Running (publicip:8000/classify)

---

SQS Queue Name - Request Queue, Response Queue

---

S3 Bucket Name - input-bucket-541p1, output-bucket-cse541p1

---

EC2 Instance Name - Web-tier
EC2 Instance Type - t2.micro
EC2 Instance Region - us-east-1
EC2 Instance Public IP -

---

## Steps for running the Image Recognition as a service

- Start a single App Tier instance in the autoscaling by setting the desired state to 1
- Start the Web Tier instance and launch the Flask application by running the command flask run -h 0.0.0.0 -p 8000 on the terminal.
- In a new terminal of Web Tier, run python scaling.py
- Take note of the public IP address of the web tier instance.
- Open a new terminal window and navigate to the folder containing the multithread_workload_generator.py script and the folder containing the images you want to classify.
- Run the multithread_workload_generator.py script with the following command, replacing public_ip_address with the public IP address of the web tier instance, image_folder with the path to the folder containing the images, and num_request with the desired number of image classification requests:
