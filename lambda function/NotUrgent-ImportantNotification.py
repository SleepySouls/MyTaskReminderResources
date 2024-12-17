import boto3
import json
import random
from datetime import datetime, timedelta

# Khởi tạo kết nối đến DynamoDB
dynamodb = boto3.client('dynamodb')

# Khởi tạo kết nối đến Cognito
cognito = boto3.client('cognito-idp', region_name='ap-southeast-1')

# Khởi tạo kết nối đến SNS
sns_client = boto3.client('sns', region_name='ap-southeast-1')

# Biến môi trường
PoolID = 'ap-southeast-1_qATzXHFqM'
TopicARN = 'arn:aws:sns:ap-southeast-1:203918871595:MyTaskReminderNotification'

def get_user_name(user_id):
    try:
        response = cognito.admin_get_user(
            UserPoolId=PoolID,
            Username=user_id
        )
        for attr in response['UserAttributes']:
            if attr['Name'] == 'email':
                return attr['Value'], ""
        return None, response
    except Exception as e:
        print(f"Error getting user name: {str(e)}")
        return None, f"Error getting user name: {str(e)}"

def send_notification(user_name, EventDate, message):
    # Tính toán thời gian cần gửi thông báo (trước 5 tiếng)
    send_time = EventDate - timedelta(hours=5)

    try:
        sns_client.publish(
            TopicArn=TopicARN,
            Message=message,
            MessageAttributes={
                'ScheduledTime': {
                    'DataType': 'String',
                    'StringValue': send_time.strftime('%Y-%m-%dT%H:%M:%S')
                }
            }
        )
        print(f"Notification sent to {user_name}")
    except Exception as e:
        print(f"Error sending notification: {str(e)}")

def lambda_handler(event, context):
    user_id = event['UserId']
    user_name, err = get_user_name(user_id)
    if user_name is None:
        return {
            'statusCode': 500,
            'msg': json.dumps(str(err))
        }
        
    selected_datetime_str = event['EventDate']  # Ngày và giờ được chọn bởi người dùng
    selected_datetime = datetime.strptime(selected_datetime_str, '%B %d, %Y')

    message = random.choice([
        f"Dear {user_name}, 🌱 It's time to invest in your future. Start working on Task #1 today!",
        f"Dear {user_name}, 🌱 Remember, long-term success depends on working on important tasks, even if they're not urgent.",
        f"Dear {user_name}, 🌱 Don't delay your growth. Begin those important, non-urgent tasks now for a brighter tomorrow."
    ])

    send_notification(user_name, selected_datetime, message)

    return {
        'statusCode': 200,
        'body': json.dumps('Thông báo đã được đặt lịch gửi thành công.')
    }