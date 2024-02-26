import json
import boto3

from datetime import date
from datetime import datetime, timedelta
# Query string to execute
t1=date.today() - timedelta(1)
d=t1.strftime("%Y-%m-%d")
query = "select eventversion, useridentity.type,useridentity.principalid,useridentity.arn,useridentity.accountid,useridentity.invokedby,useridentity.accesskeyid,useridentity.userName, useridentity.sessioncontext.attributes.mfaauthenticated,useridentity.sessioncontext.attributes.creationdate, useridentity.sessioncontext.sessionissuer.type,useridentity.sessioncontext.sessionissuer.principalId,useridentity.sessioncontext.sessionissuer.arn,useridentity.sessioncontext.sessionissuer.accountId,useridentity.sessioncontext.sessionissuer.userName, useridentity.sessioncontext.ec2RoleDelivery,useridentity.sessioncontext.webIdFederationData, eventtime,eventsource,eventname,awsregion,sourceipaddress,useragent,errorcode,errormessage,requestparameters,responseelements,additionaleventdata,requestid,eventid, resources[1][1] as resource_ARN,resources[1][2] as resource_AccountID,resources[1][3] as resource_Type, eventtype,apiversion,readonly,recipientaccountid,serviceeventdetails,sharedeventid,vpcendpointid, tlsDetails.tlsVersion,tlsDetails.cipherSuite,tlsDetails.clientProvidedHostHeader from cloudtrail_logs_main WHERE (parse_datetime(eventtime,'yyyy-MM-dd''T''HH:mm:ss''Z') BETWEEN parse_datetime('"+d+"-00:00:00','yyyy-MM-dd-HH:mm:ss') AND parse_datetime('"+d+"-23:59:59','yyyy-MM-dd-HH:mm:ss'))"
# Database to execute the query against
DATABASE = 'adasdasd'

today = date.today() - timedelta(1)
d1 = today.strftime("%Y/%m/%d")

BUCKET_NAME= 'outputalbbucket'
# Output location for query results
output='s3://' + BUCKET_NAME + '/Unsaved/'+d1+'/'

def lambda_handler(event, context):

    print(d)
    print(d1)

    # Initiate the Boto3 Client
    client = boto3.client('athena')
    s3 = boto3.resource('s3')
    print("path =", output)
    # Start the query execution

    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': output
        }
    )
    filename=response.get('QueryExecutionId')+'.csv'
    fullpath=output+filename
    KEY= 'Unsaved/'+d1+'/' + filename
    print(KEY)
    ################ S3 URL Getting/creating ############

    url = boto3.client('s3').generate_presigned_url(
    ClientMethod='get_object', 
    Params={'Bucket': BUCKET_NAME, 'Key': KEY},
    ExpiresIn=3600)
    
    print(url)
    
    ################ SNS notification ##################
    
    notification = "Please open the below URL to access the file. \n\nThe link is valid for next 1 hour only. \n\nURL :- \n\n" + url + ""
    sub="Athena logs for the today dated 07/03/2023"
    client = boto3.client('sns')
    response = client.publish (
        TargetArn = "arn:aws:sns:ap-south-1:22333444555:Athena-Cloudtrail",
        Message = json.dumps({'default': notification}),
        MessageStructure = 'json',
        Subject=sub
    )
    # Return response after starting the query execution
    return response

