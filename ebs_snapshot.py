import boto3


def lambda_handler(event, context):
    # Run this command if you are running it on local machine. Replace profile name.
    # boto3.setup_default_session(profile_name='admin-analyticshut')
    ec2_client = boto3.client('ec2')

    # listing all regions
    # regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # listing all regions with slightly more readable code.
    regions_list = ec2_client.describe_regions()['Regions']
    regions = [region['RegionName'] for region in regions_list]
    # print(regions)

    # looping over all regions in our account and finding instances which we want to stop
    for region in regions:
        print(region)
        ec2 = boto3.resource('ec2', region_name=region)

        # Filtering instances with tag Env and value Dev
        instances = ec2.instances.filter(Filters=[{
            'Name': 'tag:Env', 'Values': ['Dev']
        }])

        for instance in instances:
            for volume in instance.volumes.all():
                print(volume.id)
                volume.create_snapshot()
            # instance.start()
            # print("\t Starting instance : " + instance.id)


