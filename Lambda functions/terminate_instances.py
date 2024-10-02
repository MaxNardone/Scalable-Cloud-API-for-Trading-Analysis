import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    #If this is received, we send the signal to terminate all instances in the ids list
    if 'terminate_instance_ids' in event:
        instance_ids = event['terminate_instance_ids']
        ec2_client.terminate_instances(InstanceIds=instance_ids)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Termination initiated', 'instance_ids': instance_ids})
        }
    #Check their status
    elif 'instance_ids' in event:
        instance_ids = event['instance_ids']
        instances = ec2.instances.filter(InstanceIds=instance_ids)
        terminated_instances = []

        for instance in instances:
            instance.load()
            instance_status = ec2_client.describe_instance_status(InstanceIds=[instance.id])
            if instance.state['Name'] == 'terminated':
                terminated_instances.append(instance.id)
        all_terminated = len(terminated_instances) == len(instance_ids)
        #Print on console to debug
        print(f"All terminated: {all_terminated}, terminated instances: {terminated_instances}")
        return {
            'statusCode': 200,
            'body': json.dumps({'terminated': all_terminated, 'instance_ids': terminated_instances})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid input  ')
        }

