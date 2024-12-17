import json
import boto3
import os

# Khởi tạo tài nguyên DynamoDB
dynamodb = boto3.resource('dynamodb')
# Lấy tên bảng từ biến môi trường
table_name = 'MyTaskReminder_EventData'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Kiểm tra xem có phần thân trong sự kiện không
        if 'body' not in event:
            raise KeyError('body')
        
        # Lấy dữ liệu từ phần thân của sự kiện (JSON body từ API Gateway)
        body = json.loads(event['body'])
        for res_item in body:
            item = {
                'EventID': res_item['id'],
                'EventType': res_item['type'],
                'EventName': res_item['name'],
                'EventDate': res_item['date']
            }
            # Ghi dữ liệu vào DynamoDB
            table.put_item(Item=item)
        
        # res_item = table.get_item(
        #     Key={
        #         'EventID': body['id']
        #     }
        # )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({'msg':'Item added to DynamoDB'})
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps(f'Missing key: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps(f'Error: {str(e)}')
        }
