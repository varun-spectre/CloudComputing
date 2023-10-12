import boto3
import os
import time
import numpy
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

cloudwatch = boto3.client('cloudwatch')
autoscaling = boto3.client('autoscaling')
client_ec2 = boto3.client('ec2')

while True:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    period = 30

    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': "AWS/SQS",
                        'MetricName': "ApproximateNumberOfMessagesVisible",
                        'Dimensions': [
                            {
                                'Name': 'QueueName',
                                'Value': 'RequestQueue'
                            },
                        ]
                    },
                    'Period': period,
                    'Stat': 'Sum',
                },
                'ReturnData': False,
            },
            {
                'Id': 'm2',
                'MetricStat': {
                    'Metric': {
                        'Namespace': "AWS/AutoScaling",
                        'MetricName': "GroupInServiceInstances",
                        'Dimensions': [
                            {
                                'Name': 'AutoScalingGroupName',
                                'Value': 'app-instance-autoscaling'
                            },
                        ]
                    },
                    'Period': period,
                    'Stat': 'Average',
                },
                'ReturnData': False,
            },
            {
                "Label": "Calculate the backlog per instance",
                "Id": "e1",
                "Expression": "m1 / m2",
                "ReturnData": True
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        ScanBy='TimestampDescending',
        MaxDatapoints=10,
    )

    updated_desired_state = 1
    print(response['MetricDataResults'][0]['Values'])

    if response['MetricDataResults'][0]['Values']:
        current = numpy.average(response['MetricDataResults'][0]['Values'])

        if current >= 20:
            updated_desired_state = 19
            # updated_desired_state = 5
        elif current >= 15 and current < 20:
            updated_desired_state = 15
        elif current >= 10 and current < 15:
            updated_desired_state = 10
            # updated_desired_state = 4
        elif current >= 5 and current < 10:
            updated_desired_state = 5
            # updated_desired_state = 3
        elif current >=1 and current < 5:
            # updated_desired_state = 3
            updated_desired_state = 2

        response = autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=['app-instance-autoscaling']
        )

        desired_capacity = response['AutoScalingGroups'][0]['DesiredCapacity']

        print(desired_capacity)
        print(updated_desired_state)

        if desired_capacity != updated_desired_state:
            logging.info("Scaling will be triggered from %s to %s instance", desired_capacity, updated_desired_state)
            response = autoscaling.update_auto_scaling_group(
                AutoScalingGroupName='app-instance-autoscaling',
                DesiredCapacity=updated_desired_state
            )
            # get the current instance IDs in the Auto Scaling group
            # instance_ids = []
            # for instance in response['AutoScalingGroups'][0]['Instances']:
            #     instance_ids.append(instance['InstanceId'])

            # # add a suffix to the names of the instances
            # for i, instance_id in enumerate(instance_ids):
            #     response = client_ec2.describe_instances(InstanceIds=[instance_id])
            #     name = response['Reservations'][0]['Instances'][0]['Tags'][0]['Value']
            #     new_name = f"{name}-{i}"
            #     client_ec2.create_tags(
            #         Resources=[instance_id],
            #         Tags=[{'Key': 'Name', 'Value': new_name}]
            #     )
            time.sleep(30)
    time.sleep(10)
    
