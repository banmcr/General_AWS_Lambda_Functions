import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    createdby = (event['detail']['userIdentity']['principalId']).split(':')[1]
    message = ''
    if event['detail-type'] == 'AWS API Call via CloudTrail':
        event_name = event['detail']['eventName']
        if event_name == 'CreateUser':
            user_name = event['detail']['requestParameters']['userName']
            message = f'A new user {user_name} has been created in AWS IAM by {createdby}'
        elif event_name == 'CreateAccessKey':
            user_name = event['detail']['userIdentity']['userName']
            access_key = event['detail']['responseElements']['accessKey']['accessKeyId']
            message = f'An access key {access_key} has been created for user {user_name} in AWS IAM by {createdby}'
        elif event_name == 'ChangePassword':
            user_name = event['detail']['userIdentity']['userName']
            message = f'The password for user {user_name} has been changed in AWS IAM by {createdby}'
        else:
            message = 'Unknown event type'
        if message != '':
            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:222333344455:IAM-Sandbox-Event',
                Subject='AWS IAM User creation Activity Performed',
                Message=message
            )
