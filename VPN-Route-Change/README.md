# AWS VPC route table route change

For this function, an AWS SNS topic is the trigger, whenever the cloudwatch alarm is triggered this lambda executes.

If the alarm is in ALARM state and the lambda is triggered

--> this change the route from state A to state B

once the alarm is back to OK state and the lambda is triggered

--> this changes the route from state B to state A