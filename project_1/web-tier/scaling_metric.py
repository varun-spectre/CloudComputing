import boto3
import time

# Create a CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# Define the customized metric specification
custom_metric_spec = {
    "Metrics": [
        {
            "Id": "m1",
            "MetricStat": {
                "Metric": {
                    "Namespace": "AWS/SQS",
                    "MetricName": "ApproximateNumberOfMessagesVisible",
                    "Dimensions": [
                        {
                            "Name": "QueueName",
                            "Value": "RequestQueue"
                        }
                    ]
                },
                "Stat": "Sum"
            },
            "ReturnData": False,
            "Label": "Get the queue size (the number of messages waiting to be processed)"
        },
        {
            "Label": "Get the group size (the number of InService instances)",
            "Id": "m2",
            "MetricStat": {
                "Metric": {
                    "MetricName": "GroupInServiceInstances",
                    "Namespace": "AWS/AutoScaling",
                    "Dimensions": [
                        {
                            "Name": "AutoScalingGroupName",
                            "Value": "app-instance-autoscaling"
                        }
                    ]
                },
                "Stat": "Average"
            },
            "ReturnData": False
        },
        {
            "Label": "Calculate the backlog per instance",
            "Id": "e1",
            "Expression": "m1 / m2",
            "ReturnData": True
        }
    ],
    "TargetValue": 10
}

# Loop forever, publishing the custom metric data every 10 seconds
while True:
    # Get the customized metric data
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'e1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'CustomMetrics',
                        'MetricName': 'BacklogPerInstance',
                        'Dimensions': [
                            {
                                'Name': 'AutoScalingGroupName',
                                'Value': 'app-instance-autoscaling'
                            }
                        ]
                    },
                    'Period': 10,
                    'Stat': 'Average'
                },
                'ReturnData': False
            }
        ],
        StartTime=time.time() - 240,
        EndTime=time.time(),
        ScanBy='TimestampDescending'
    )
    print(f"Got metric data: {response}")
    m1 = response['MetricDataResults'][0]['Values'][0]

    # Update the custom metric data with the calculated value
    custom_metric_spec['TargetValue'] = m1

    # Publish the custom metric data to CloudWatch
    response = cloudwatch.put_metric_data(
        Namespace='CustomMetrics',
        MetricData=[
            {
                'MetricName': 'BacklogPerInstance',
                'Dimensions': [
                    {
                        'Name': 'AutoScalingGroupName',
                        'Value': 'app-instance-autoscaling'
                    }
                ],
                'Value': m1,
                'Unit': 'None'
            }
        ],
        ClientRequestToken=str(time.time()),
        CustomUnit='BacklogPerInstance'
    )

    print(f"Published metric data: {response}")

    # Wait for 10 seconds before publishing the next metric data
    time.sleep(10)
