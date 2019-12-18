import boto3
from datetime import datetime, timedelta


def lambda_handler(event, context):
    # Run this command if you are running it on local machine. Replace profile name.
    # boto3.setup_default_session(profile_name='admin-analyticshut')
    ec2_client = boto3.client('ec2')
    sts_client = boto3.client('sts')
    account_id = sts_client.get_caller_identity()["Account"]
    print(account_id)

    expiry_date = datetime.strftime(datetime.now() - timedelta(0), '%Y-%m-%d')
    print(expiry_date)
    # regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    regions_list = ec2_client.describe_regions()['Regions']
    regions = [region['RegionName'] for region in regions_list]
    # print(regions)

    for region in regions:
        print(region)
        ec2 = boto3.client('ec2', region_name=region)

        snapshots = ec2.describe_snapshots(OwnerIds=[account_id])['Snapshots']

        old_snapshots = filter(lambda x: datetime.strftime(x['StartTime'], '%Y-%m-%d') <= expiry_date, snapshots)

        for snapshot in old_snapshots:
            # instance.start()
            try:
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                print("\t Deleted Snapshot : " + snapshot['SnapshotId'])
            except Exception as e:
                print('Delete failed for Snapshot: ' + snapshot['SnapshotId'])


