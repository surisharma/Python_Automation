import boto3
def list_unused_volumes_in_all_regions():
  ec2 = boto3.client('ec2')
  # Get list of AWS regions
  regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
  all_unused_volumes = []
  # Iterate over each region
  for region in regions:
    print("Checking region:", region)
    ec2 = boto3.client('ec2', region_name=region)
  # Describe all volumes in the region
  response = ec2.describe_volumes()
  unused_volumes = []
  # Iterate through volumes
  for volume in response['Volumes']:
    # Check if volume is available ( not attached to any instance)
    if volume['State'] = 'available':
      unused_volumes.append(volume)
    # Add unused volumes in this region to the overall list
    all_unused_volumes.extend(unused_volumes)
  return all_unused_volumes
unused_volumes_all_regions = list_unused_volumes_in_all_regions
for volume in unused_volumes_all_regions:
  region = volume['AvailabilityZone'][:-1]
  print(f"Unused Volume ID: {volume['VolumeId']} | State: {volume['State']} | Region: {region} | | Size: {volume['Size']}, GiB ")
  print("------------------------")
  #print("Volume ID:" volume['VolumeID']
  #print(Size:", volume['Size'], "GiB")
  #print("Availability Zone:", volume['AvailabilityZone'])
  #print("State:", volume['State'])
  #print("------------------------")
  
