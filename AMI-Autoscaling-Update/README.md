# AWS Autoscaling update

This Lambda function does the following

1. Create a AMI for the server which has a tag key named "backup"
2. create a new launch template version of the autoscaling launch templete, mention it in environment variable "launch_template_id". 
3. delete the old launch templete version
4. delete any old AMI which were created by this automation.
