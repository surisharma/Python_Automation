import boto3
import os
from datetime import datetime, timezone,timedelta
# Create an EC2 resource
ec2 = boto3.resource('ec2')
# Define the tag key to check for (change this if needed)
tag_key = os.getenv('TAG_KEY', 'Backup')
# Define the age threshold (30 day in this case)
age_threshold_days = 0

SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN' , 'arn:aws:sns:Your region:Aws Account :EBS')

def get_regions():
    """Fetch all available AWS regions for EC2"""
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()
    return[region['RegionName']for region in regions['Regions']]

def send_sns_notification(subject,message):
     """Send a notification using Amazon SNS"""
     response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )
     return reponse
     

def delete_old_volumes(region):
    """Delete old EBS volumes in a given region"""
    ec2 = boto3.resource('ec2',region_name=region)
    # Calculate the data threshold
    now = datetime.now(timezone.utc)
    threshold_date = now - timedelta(days=age_threshold_days)  
    # Filter volume based on creation time and tags
    volumes = ec2.volumes.filter(Filters=[{'Name': 'status','Values': ['available']}])
    deleted_volumes = []
    
    for volume in volumes:
        # Get volume creation time
        create_time = volume.create_time
        
        #Get tags for the volume
        tags = volume.tags or []
        tag_keys = {tag['key'] for tag in tags}   
        
        # Check if the volume is older than the threshold and lacks the specified tag
        
        if create_time < threshold_date and tag_key not in tag_keys:
            try:
                print(f"Deleting volume {volume.id} in region {region}")
                volume.delete()
            except Exception as e:
                print(f"Failed to delete volume {volume.id} in region {region}: {str(e)}")   
        # Send SNS notification if there are deleted volumes
        if deleted_volumes:
          subject = f"EBS Volume Deletion Report for {region}"
          message = f"The following EBS volumes were deleted in region {region}:\n\n" + "\n".join(deleted_volumes)
          send_sns_notification(subject, message)         
        
def lambda_handler(event, context):
    # Get all regions
    regions = get_regions()
    
    #Iterate over all regions and delete the old volume
    for region in regions:
        delete_old_volumes(region)
        
    return {
        'statusCode': 200,
        'body': 'Old volumes cleanup across all regions complete'
    }    
