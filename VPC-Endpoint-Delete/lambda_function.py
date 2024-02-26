import time
import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('ec2')
    response = client.describe_vpc_endpoints(
    Filters=[
        {
            'Name': 'vpc-endpoint-state',
            'Values': [
                'available'
            ]
        },
    ],
    MaxResults=123
    )
    endpointlist = []
    for endpoint in (response["VpcEndpoints"]):
        print(endpoint)
        endpointlist.append(endpoint["VpcEndpointId"])
        
    print(endpointlist)
 
  
    responsedelete = client.delete_vpc_endpoints(VpcEndpointIds=endpointlist)