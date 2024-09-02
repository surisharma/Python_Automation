import boto3

# Initialize AWS clients
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # List to hold unused EIPs
    unused_eips = []

    try:
        # Describe all Elastic IPs
        eips = ec2_client.describe_addresses()['Addresses']
        
        for eip in eips:
            # Check if the EIP is associated with an instance
            if 'InstanceId' not in eip:
                eip_details = (
                    f"EIP = {eip['PublicIp']} | "
                    f"Allocation ID = {eip['AllocationId']} | "
                    f"Region: {eip.get('NetworkInterfaceOwnerId', 'N/A')}"
                )
                unused_eips.append(eip_details)
    except Exception as e:
        print(f"Error describing EIPs: {str(e)}")

    # Format the result
    result_body = '\n'.join(unused_eips) if unused_eips else "No unused EIPs found."

    # SNS topic details
    sns_topic_arn = "arn:aws:sns:your-region:your-account-id:your-topic-name"  # Replace with your SNS topic ARN
    sns_subject = "Unused Elastic IPs Report"
    sns_message = f"Here is the list of unused Elastic IPs:\n\n{result_body}"

    # Publish message to SNS topic
    try:
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject=sns_subject,
            Message=sns_message
        )
        print("Message successfully published to SNS topic.")
        print(f"Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error publishing message to SNS topic: {str(e)}")

    # Return a response
    return {
        'statusCode': 200,
        'body': 'Report has been published to the SNS topic.'
    }
