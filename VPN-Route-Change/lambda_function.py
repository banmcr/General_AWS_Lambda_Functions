import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('ec2')
    sns = boto3.client('sns')
    # TODO implement
    message_data = json.loads(event['Records'][0]["Sns"]["Message"])
    new_state_value = message_data['NewStateValue']
    print(new_state_value)
    if new_state_value == "ALARM":
        print("This is in Alarm state")
        sns_message = "Firewall in Alarm state, maybe down, changing the Middleware VPN to AWS Site-to-Site VPN"
        sns.publish(
                TopicArn='arn:aws:sns:us-east-1:666611442233:VPN-Change-Topic',
                Message=sns_message
            )
        route_response = client.replace_route(
            DestinationCidrBlock='10.0.1.0/20',
            GatewayId='vgw-0093be35bd7ebd1eb',
            RouteTableId='rtb-8ecfa7f0'
            )
        vpn_response = client.modify_vpn_connection(
            VpnConnectionId='vpn-0b359a92b490068dc',
            CustomerGatewayId='cgw-05a25e5a30bc364b9'
            )
         
            
    elif new_state_value == "OK":
        print("This is in OK state")
        sns_message = "Firewall in OK state, changing the Middleware VPN to Firewall VPN"
        sns.publish(
                TopicArn='arn:aws:sns:us-east-1:666611442233:VPN-Change-Topic',
                Message=sns_message
            )
        route_response = client.replace_route(
            DestinationCidrBlock='10.0.1.0/20',
            NetworkInterfaceId='eni-0d9d4525c289828cd',
            RouteTableId='rtb-8ecfa7f0'
            )
        vpn_response = client.modify_vpn_connection(
            VpnConnectionId='vpn-0b359a92b490068dc',
            CustomerGatewayId='cgw-08e421ee95d7fc38f'
            )