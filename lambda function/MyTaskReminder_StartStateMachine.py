import json
import datetime

def lambda_handler(event, context):
    # Extract event details from the input event
    event_date_str = event.get('EventDate')
    current_date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)

    # Parse the event date
    try:
        event_date = datetime.datetime.strptime(event_date_str, "%B %d, %Y")
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Invalid date format. Expected format is %B %d, %Y.',
                'error': str(e)
            })
        }

    # Compare dates
    if event_date <= current_date + datetime.timedelta(days=1):
        status = "IfDue"
    else:
        status = "NotDue"

    # Return the status
    return {
        'status': status,
        'EventType': event.get('EventType'),
        'EventDate': event.get('EventDate'),
        'UserId': event.get('UserId')
    }