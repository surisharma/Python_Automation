import boto3
import json
client = boto3.Session('sns')
sns_client = boto3.client('sns')

def lambda_handler(event,context):
    # Initialize a session using Amazon EC2
    session = boto3.Session()
    ec2_client = session.client('ec2')
    
    #Get list of all AWS Regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    #List to hold unused volumes
    unused_volumes = []
    
    #Iterate over each region
    for region in regions:
        print(f"Checking region: {region}")
        ec2 = session.client('ec2', region_name=region) 
        
        try:
            #Describe volumes in the current region
            volumes = ec2.describe_volumes()['Volumes'] 
            
            for volume in volumes:
                # Check If the volume is attached to any instance
                if not volume['Attachments']:
                    volume_details = (
                        f"Unused Volume ID = {volume['VolumeId']} | "
                        f"Volume Name = {volume.get('Tags', [{}])[0].get('Value', 'N/A')} | "
                        f"Region: {region} | "
                        f"Size: {volume['Size']} GiB"
                    )
                    unused_volumes.append(volume_details)
        except Exception as e:
            print(f"Error in region {region}: {str(e)}")   
            
    # Return the result
    result_body = '\n'.join(unused_volumes)
    
     # SNS topic details
    sns_topic_arn = "arn:aws:sns:us-east-example:EBS"  # Replace with your SNS topic ARN
    sns_subject = "Unused EBS Volumes Report"
    sns_message = f"Here is the list of unused EBS volumes:\n\n{result_body}"

    # Publish message to SNS topic
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject=sns_subject,
            Message=sns_message
        )
        print("Message successfully published to SNS topic.")
    except Exception as e:
        print(f"Error publishing message to SNS topic: {str(e)}")

    # Return a response
    return {
        'statusCode': 200,
        'body': 'Report has been published to the SNS topic.'
    }
