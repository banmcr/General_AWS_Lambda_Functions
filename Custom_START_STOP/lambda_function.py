import time
import json
import boto3


def lambda_handler(event, context):
    print(json.dumps(event))
    tagName = event['tagname']
    tagValue = event['tagvalue']
    actionValue = event['action']
    
    if (actionValue is not None) and (tagName is not None) and (tagValue is not None):
        #EC2
        ec2InstanceList = listEC2InstancesByTag(tagName, tagValue)
        startStopEC2Instances(actionValue, ec2InstanceList)
        #RDS
        startStopRDSInstances(tagName, tagValue, actionValue)
        #OpenSearch
        
        #Elasticache - Redis
        #stopRedisCluster('test-cluster')
        #startRedisCluster('test-cluster')
        #startStopDocDBCluster(tagName, tagValue, actionValue)
        #startStopEKSNG - GIVE NodeGroup name in the function
        #ecs_start_stop('cluster_arn',actionValue)
    return {
        'statusCode': 200,
        'body': json.dumps('SUCCESS')
    }

#EC2 Instances.    
def startStopEC2Instances(actionValue, instanceIds):
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')
    if actionValue.lower() == 'start':
        print('Starting EC2 instances.')
        return client.start_instances(InstanceIds=instanceIds)
    elif actionValue.lower() == 'stop':
        print('Stopping EC2 instances.')
        return client.stop_instances(InstanceIds=instanceIds)    
                        
                    
def listEC2InstancesByTag(tagkey, tagvalue):
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
    return instancelist       
  
#RDS Instances.
def startStopRDSInstances(tagkey, tagvalue, actionValue):
    rdsclient = boto3.client('rds')
    response = rdsclient.describe_db_instances()
    for dbInstance in (response["DBInstances"]):
        for tag in (dbInstance["TagList"]):
            if tag["Key"] == tagkey and tag["Value"] == tagvalue:
                dbInstanceIdentifier = dbInstance['DBInstanceIdentifier']
                if actionValue.lower() == 'start' and dbInstance['DBInstanceStatus'] == 'stopped':
                    print('Starting RDS DB instance. - ' + dbInstanceIdentifier)
                    rdsclient.start_db_instance(DBInstanceIdentifier=dbInstanceIdentifier)
                elif actionValue.lower() == 'stop' and dbInstance['DBInstanceStatus'] == 'available':
                    print('Stopping RDS DB instance. - ' + dbInstanceIdentifier)
                    rdsclient.stop_db_instance(DBInstanceIdentifier=dbInstanceIdentifier)
                    
        
#ECS
    #Scheduled Auto Scaling

#OpenSearch
    #While Stopping - 
        #take the snapshot using API
        #Delete the OpenSearch domain in the night
    #While Starting - 
        #Launch the new domain from snapshot.
        
#Redis
    #While Stopping - 
        #take the snapshot using API
        #Delete the Cluster
    #While Starting - 
        #Launch the new cluster from snapshot.
def stopRedisCluster(cacheClusterName):
    redisClient = boto3.client('elasticache')
    snapshotName = cacheClusterName + '-manual-latest'
    responseSnapDesc = redisClient.describe_snapshots(SnapshotName=snapshotName)
    snapshotList = responseSnapDesc['Snapshots'] 
    if  snapshotList:
        print('Existing snapshot found. Deleting it now.')
        deleteSnapshotResponse = redisClient.delete_snapshot(SnapshotName=snapshotName)
    #Waiting for the existing snapshot to be deleted.
    while redisClient.describe_snapshots(SnapshotName=snapshotName)['Snapshots']:
        time.sleep(1)
    
    print('Previous Snapshot Deleted. Creating new snapshot now and deleting the cluster.')
    response = redisClient.delete_cache_cluster(CacheClusterId=cacheClusterName, FinalSnapshotIdentifier=snapshotName)
    print(response)
    
    
                    
def startRedisCluster(cacheClusterName):
    redisClient = boto3.client('elasticache')
    snapshotName = cacheClusterName + '-manual-latest'
    response = redisClient.create_cache_cluster(CacheClusterId=cacheClusterName, SnapshotName=snapshotName)
    print(json.dumps(response))  
    
    
    
#DocumentDB Instances.
def startStopDocDBCluster(tagkey, tagvalue, actionValue):
    client = boto3.client('docdb')
    response = client.describe_db_clusters(
        Filters=[
        {
            'Name': 'engine',
            'Values': [
                'docdb'
            ]
        },
    ])
    for docDBCluster in (response["DBClusters"]):
        tagListResponse = client.list_tags_for_resource(ResourceName=docDBCluster['DBClusterArn'])
        tagList = tagListResponse['TagList']
        for tag in tagList:
            if tag["Key"] == tagkey and tag["Value"] == tagvalue:
                if actionValue.lower() == 'start' and docDBCluster['Status'] == 'stopped':
                    print('DocumentDB cluster ' + docDBCluster['DBClusterIdentifier'] + ' is in stopped state. Starting it now.')
                    client.start_db_cluster(DBClusterIdentifier=docDBCluster['DBClusterIdentifier'])
                elif actionValue.lower() == 'stop' and docDBCluster['Status'] == 'available':
                    print('DocumentDB ' + docDBCluster['DBClusterIdentifier'] + ' is in available state. Stopping it now.')
                    client.stop_db_cluster(DBClusterIdentifier=docDBCluster['DBClusterIdentifier'])



def startStopEKSNG(actionValue):
    eks_client = boto3.client('eks')
    if actionValue.lower() == 'start':
        print('Upscaling the min/max/desired values')
        return eks_client.update_nodegroup_config(clusterName='Test2',nodegroupName='S22IT-UAT-NG-SPOT',scalingConfig={'minSize': 2,'maxSize': 5,'desiredSize': 2})
    elif actionValue.lower() == 'stop':
        print('downscaling the min/max/desired values to 0')
        return eks_client.update_nodegroup_config(clusterName='Test2',nodegroupName='S22IT-UAT-NG-SPOT',scalingConfig={'minSize': 0,'maxSize': 5,'desiredSize': 0})

def ecs_start_stop(cluster_arn, actionValue):
    #ecsList = []
    ecsclient = boto3.client('ecs')
    #ecsResponse = ecsclient.list_clusters()
    #clusters_arns=ecsResponse["clusterArns"]
    #for cluster_arn in clusters_arns:
    cluster_name = cluster_arn.split('/')[-1]
    print(f"Services in ECS cluster {cluster_name}:")
    services_response = ecsclient.list_services(cluster=cluster_arn)
    service_arns = services_response['serviceArns']
    for service_arn in service_arns:
        service_name = service_arn.split('/')[-1]
        if actionValue.lower() == 'stop':
            print(f"\t- changing {service_name} count to 0")
            ecsclient.update_service(cluster=cluster_name,service=service_name,desiredCount=0)
        elif actionValue.lower() == 'start':
            print(f"\t- changing {service_name} count to 1")
            ecsclient.update_service(cluster=cluster_name,service=service_name,desiredCount=1)