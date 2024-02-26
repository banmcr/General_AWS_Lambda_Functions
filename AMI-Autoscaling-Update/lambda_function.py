import json
import os
import boto3
import datetime
import time
from datetime import datetime
from datetime import datetime, timedelta

start_date = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
region = os.getenv("region")
client = boto3.client('ec2',region)


def lambda_handler(event, context):

    launch_template_id = os.environ["launch_template_id"]
    
    reservations = client.describe_instances( Filters=[{ 'Name': 'tag-key', 'Values': ['backup']},], DryRun=False).get('Reservations', [])
    print(reservations)
    x=(reservations[0]['Instances'][0]['InstanceId'])
    print(x)
    name= x + " from "+start_date
    description= "AMI for created by lambda"
    image = client.create_image(Description=description,DryRun=False, InstanceId=x, Name=name, NoReboot=True)
    print(image['ImageId'])
    image_name = image['ImageId']
        # get autoscaling client
    
    response = client.create_launch_template_version(
            LaunchTemplateId=launch_template_id,
            SourceVersion="$Latest",
            VersionDescription="Latest-AMI "+start_date,
            LaunchTemplateData={
                "ImageId": image_name
            }
        )
    print("Latest Launch Template version created with " + image_name)
    
    response = client.modify_launch_template(
            LaunchTemplateId=launch_template_id,
            DefaultVersion="$Latest")
    print("Default launch template set to $Latest.")
    previous_version = str(int(response["LaunchTemplate"]["LatestVersionNumber"]) - 2)
    response = client.delete_launch_template_versions(
            LaunchTemplateId=launch_template_id,
            Versions=[
                previous_version,
            ]
        )
    
    now1=str(datetime.date(datetime.now()-timedelta(days = 1)).strftime('%Y-%m-%d'))
    print(now1)
    now=str(datetime.date(datetime.now()).strftime('%Y-%m-%d'))
    print(now)
    try:
        image=client.describe_images(Filters=[{'Name': 'description','Values': ['AMI for created by lambda']}])
        print(image)
        for imag in image['Images']:
            print(imag['CreationDate'].split("T")[0])
            if imag['CreationDate'].split("T")[0]<=now1 :
                image_id=imag['ImageId']
                print("Deleting: "+image_id)
                response = client.deregister_image(ImageId=image_id)
                snap=client.describe_snapshots(Filters=[{'Name':'description','Values':['*'+image_id+'*']}])
                for snapshot in snap['Snapshots']:
                    print(snapshot['SnapshotId'])
                    response = client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            else :
                print("No AMI Image with deletion date of today.")
    except Exception as e:
        print(e)

