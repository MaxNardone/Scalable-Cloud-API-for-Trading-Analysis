import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    #I needed to define the security group, otherwise it will always get the default one
    security_group_name = 'MyWebServerGroup'
    #the check below is necessary in order to verify the security group
    #Methods used are described here: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_security_groups.html
    try:
        security_group = ec2_client.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': [security_group_name]}]
        )
        security_group_id = security_group['SecurityGroups'][0]['GroupId']
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error finding security group: {str(e)}")
        }
    #If scale is passed only the instance Ids are returned
    if 'scale' in event:
        #Hardcoded instance informations, the ami needs to be changed if the initial instance gets updated
        ami_id = 'ami-04a46eb0e8295d644'
        instance_type = 't2.micro'
        scale = event['scale']
        try:
            instances = ec2.create_instances(
                ImageId=ami_id,
                InstanceType=instance_type,
                MinCount=scale,
                MaxCount=scale,
                SecurityGroupIds=[security_group_id]
            )

            instance_ids = [instance.id for instance in instances]
            return {
                'statusCode': 200,
                'body': json.dumps({'instance_ids': instance_ids})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f"Errors: {str(e)}")
            }
    #Else we check the instance status by usin the input 'instance_ids'
    elif 'instance_ids' in event:
        instance_ids = event['instance_ids']
        if not instance_ids:
            return {
                'statusCode': 400,
                'body': json.dumps('No instance IDs given, retry.')
            }
        try:
            instances = ec2.instances.filter(InstanceIds=instance_ids)
            instances_info = []
            for instance in instances:
                instance.load()
                instance_status = ec2_client.describe_instance_status(InstanceIds=[instance.id])
                if instance.state['Name'] == 'running' and instance_status['InstanceStatuses'][0]['InstanceStatus']['Status'] == 'ok' and instance_status['InstanceStatuses'][0]['SystemStatus']['Status'] == 'ok':
                    instances_info.append({
                        'instance_id': instance.id,
                        'public_dns': instance.public_dns_name,
                        'public_ip': instance.public_ip_address
                    })
            
            #If all instances are ready
            all_ready = all(['public_dns' in info and 'public_ip' in info for info in instances_info])
            if all_ready:
                return {
                    'statusCode': 200,
                    'body': json.dumps(instances_info)
                }
            else:
                return {
                    'statusCode': 200,
                    'body': json.dumps('Not ready')
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f"Errors: {str(e)}")
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid input')
        }

