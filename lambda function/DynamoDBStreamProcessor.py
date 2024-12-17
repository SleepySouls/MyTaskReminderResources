import json
import boto3

sfn_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            item = {k: list(v.values())[0] for k, v in new_image.items()}
            
            response = sfn_client.start_execution(
                stateMachineArn='arn:aws:states:ap-southeast-1:203918871595:stateMachine:MyTaskReminder-StateMachine',
                input=json.dumps(item)
            )
            print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Step Function triggered successfully!')
    }