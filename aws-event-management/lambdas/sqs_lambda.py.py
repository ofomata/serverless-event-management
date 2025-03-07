import json
import boto3
import os

# Initialize AWS Services
sns = boto3.client('sns')

# Get environment variable
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))  # Log event

        for record in event['Records']:
            body = json.loads(record['body'])
            name = body.get('name')
            email = body.get('email')
            event_name = body.get('event')

            if not name or not email or not event_name:
                print("Skipping invalid message:", body)
                continue

            # Send SNS notification
            message = f"Hello {name},\n\nYou have successfully registered for {event_name}.\n\nThank you!"
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject="Event Registration Confirmation"
            )

            print(f"Sent email to {email} for event {event_name}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Processed messages successfully"})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
