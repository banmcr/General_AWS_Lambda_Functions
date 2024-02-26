import time
import json
import boto3


def lambda_handler(event, context):
    
    actionValue = event['action']
    ec2 = boto3.client('ec2')
    #Cycle through all regions
    regionResponse = ec2.describe_regions()

    regionlist = []
    for region in (regionResponse['Regions']):
        regionlist.append(region["RegionName"])
    print(len(regionlist))
    for r in regionlist:
        print(r)
        AutoscalingUpScaleDownScale(actionValue, r)
####time.sleep(300)
        EC2StartStop(actionValue, r)
        RDSInstanceStop(actionValue, r)
            #Make them STOP
        #List all RDS
            #Make them STOP
        ecs_start_stop(actionValue, r)


########### Make All Autoscaling 0            
def AutoscalingUpScaleDownScale(actionValue, r):

#########list all AutoScaling
    asgList = []
    client = boto3.client('autoscaling',region_name=r)
    ASGresponse = client.describe_auto_scaling_groups()
    for asg in (ASGresponse['AutoScalingGroups']):
        asgList.append(asg['AutoScalingGroupName'])
    if (actionValue.lower() == 'stop') and (asgList != []):
           print(asgList)
#########Make them 0        
    for ag in asgList:
        if actionValue.lower() == 'start':
            print('Upscaling the min/max/desired values')
            client.update_auto_scaling_group(AutoScalingGroupName=ag,MinSize=1,MaxSize=2,DesiredCapacity=1)
        elif actionValue.lower() == 'stop':
            print('downscaling the min/max/desired values to 0')
            client.update_auto_scaling_group(AutoScalingGroupName=ag,MinSize=0,MaxSize=1,DesiredCapacity=0)
###############EC2-Start-Stop
def EC2StartStop(actionValue, r):

    ec2List = []
    ec2client = boto3.client('ec2',region_name=r)
    ec2response = ec2client.describe_instances(
        Filters=[
            {
            'Name': 'instance-state-name',
            'Values': ['running']
            }
        ]
    )
    for reservation in (ec2response["Reservations"]):
        for instance in reservation["Instances"]:
            ec2List.append(instance["InstanceId"])
    if (actionValue.lower() == 'stop') and (ec2List != []):
        print(ec2List)
    if (actionValue.lower() == 'start') and (ec2List != []):
        print('Starting EC2 instances.')
        ec2client.start_instances(InstanceIds=ec2List)
    elif (actionValue.lower() == 'stop') and (ec2List != []):
        print('Stopping EC2 instances.')
        ec2client.stop_instances(InstanceIds=ec2List)


###############RDS-Start-Stop        
def RDSInstanceStop(actionValue, r):
    rdsList = []
    rdsclient = boto3.client('rds',region_name=r)
    rdsResponse = rdsclient.describe_db_instances()
    for dbInstance in (rdsResponse["DBInstances"]):
        dbInstanceIdentifier = dbInstance['DBInstanceIdentifier']
        dbInstanceStatus = dbInstance['DBInstanceStatus']
        print(dbInstanceIdentifier+' is '+ dbInstanceStatus)
        if dbInstanceStatus == 'available':
            rdsclient.stop_db_instance(DBInstanceIdentifier=dbInstanceIdentifier)
            print(dbInstanceIdentifier+' will be stopped')
            
###############ECS-STOP

def ecs_start_stop(actionValue, r):
    ecsList = []
    ecsclient = boto3.client('ecs',region_name=r)
    ecsResponse = ecsclient.list_clusters()
    clusters_arns=ecsResponse["clusterArns"]
    for cluster_arn in clusters_arns:
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
            