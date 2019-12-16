import boto3


def lambda_handler(event, context):
    boto3.setup_default_session(profile_name='admin-analyticshut')
    ec2_client = boto3.client('ec2')
    # regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    regions_list = ec2_client.describe_regions()['Regions']
    regions = [region['RegionName'] for region in regions_list]
    # print(regions)

    for region in regions:
        print(region)
        ec2 = boto3.resource('ec2', region_name=region)
        """instances = ec2.instances.filter(Filters=[{
            'Name': 'instance-state-name',
            'Values': [
                'running'
            ]
        }])"""

        instances = ec2.instances.filter(Filters=[{
            'Name': 'tag:Env',
            'Values': [
                'Dev'
            ]
        }])

        for instance in instances:
            instance.stop()
            print("\t Stopping instance : " + instance.id)


lambda_handler('event', 'context')
