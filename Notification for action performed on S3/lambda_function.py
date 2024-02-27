import json
import boto3

def lambda_handler(event, context):
    # Log the event for debugging purposes
    #print("Received event: " + json.dumps(event, indent=2))
    print(event)

    # Get the S3 bucket and object information from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    iam_username = event['Records'][0]['userIdentity']['principalId'].split(":")[-1]
    event_name = event['Records'][0]['eventName']
    print(iam_username)
    # Your custom logic to handle the event (replace this with your own logic)
    notification_message = f"Hi,\n\nOperations have been performed on S3 bucket, please find the details below :-\n\nevent:'{event_name}' \nObject : '{key}' \nbucket : '{bucket}' \nUser : '{iam_username}"

    # Example: Send a notification via SNS
    sns_topic_arn = 'arn:aws:sns:ap-southeast-1:490167669940:eventbridge'
    sns_client = boto3.client('sns')
    sns_client.publish(TopicArn=sns_topic_arn, Message=notification_message, Subject='S3 Operation Performed on SAN DevOps buckets')

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent successfully!')
    }
