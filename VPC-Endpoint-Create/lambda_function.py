import time
import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('ec2')
    
    # ECR-api Endpoint #
    
    ecrapiEndpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.ecr.api',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'ECR-api-Endpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])

    

    # ECR-dkr Endpoint #
    
    ecrdkrEndpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.ecr.dkr',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'ECR-dkr-Endpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])

    
    # Logs Endpoint #
    
    logsEndpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.logs',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Logs-Endpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])

 
    # EC2 Endpoint #
    
    ec2Endpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.ec2',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'EC2-Endpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])

 
    # STS Endpoint #
    
    stsEndpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.sts',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'stsEndpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])
    
    
    # ec2-Messages Endpoint #
    
    ec2MessagesEndpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.ec2messages',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'ec2MessagesEndpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])
        
    # SSM-Messages Endpoint #
    
    ssmnessagesEndpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.ssmmessages',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'ssmnessagesEndpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])
        
    # SSM Endpoint #    
        
    ssmEndpoint = client.create_vpc_endpoint(
        VpcEndpointType='Interface',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.ssm',
        SubnetIds=['subnet-0d8122d9f9cbd52d4'],
        SecurityGroupIds=['sg-0be6d21ff05d816ab'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'SSM-Endpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])
    
    # S3 Endpoint #  
    
    S3Endpoint = client.create_vpc_endpoint(
        VpcEndpointType='Gateway',
        VpcId='vpc-0438ed7f0bcb6a4dd',
        ServiceName='com.amazonaws.us-west-2.s3',
        RouteTableIds=['rtb-0b1decd864c4f8dcf'],
        TagSpecifications=[{
            'ResourceType': 'vpc-endpoint',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'S3-Endpoint'
                },
                {
                    'Key': 'map-migra',
                    'Value': '564s8d478fea6f11'
                }]
            },
        ])    
