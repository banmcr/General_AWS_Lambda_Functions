import json
import logging
import boto3

#Logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

#Initialise Boto3 for RDS
rdsClient = boto3.client('rds')


def lambda_handler(event, context):
    

    #log input event
    LOGGER.info(event)
    
    #rdsInstanceId is passed as input to the lambda function from the AWS StepFunctions state machine.  
    rdsInstanceId = event['rdsInstanceId']
    db_instances = rdsClient.describe_db_instances(DBInstanceIdentifier=rdsInstanceId)['DBInstances']
    db_instance = db_instances[0]
    rdsInstanceState = db_instance['DBInstanceStatus']
    return {
        'statusCode': 200,
        'rdsInstanceState': rdsInstanceState,
        'rdsInstanceId': rdsInstanceId
    }