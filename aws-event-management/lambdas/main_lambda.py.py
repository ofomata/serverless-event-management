import json
import boto3
import uuid
import os
import pymysql  # MySQL library

# Initialize AWS Services
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

# Get environment variables
try:
    DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
    SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']
    RDS_HOST = os.environ['RDS_HOST']
    RDS_USER = os.environ['RDS_USER']
    RDS_PASSWORD = os.environ['RDS_PASSWORD']
    RDS_DATABASE = os.environ['RDS_DATABASE']
except KeyError as e:
    print(f"Missing environment variable: {str(e)}")
    raise Exception(f"Missing environment variable: {str(e)}")

table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))  # Log full event

        # Parse request body
        body = json.loads(event['body']) if 'body' in event else event
        name = body.get('name')
        email = body.get('email')
        event_name = body.get('event')

        if not name or not email or not event_name:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing required fields"})
            }

        # Store in DynamoDB
        item_id = str(uuid.uuid4())
        item = {
            'id': item_id,
            'name': name,
            'email': email,
            'event': event_name
        }
        table.put_item(Item=item)
        print("Stored in DynamoDB:", item)

        # Insert into RDS
        try:
            print("Connecting to RDS...")
            conn = pymysql.connect(
                host=RDS_HOST,
                user=RDS_USER,
                password=RDS_PASSWORD,
                database=RDS_DATABASE,
                connect_timeout=5
            )
            cursor = conn.cursor()

            sql = "INSERT INTO registrations (id, name, email, event) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (item_id, name, email, event_name))
            conn.commit()

            cursor.close()
            conn.close()
            print("User inserted into RDS successfully:", item)
        except pymysql.MySQLError as rds_error:
            print("RDS Insert Error:", str(rds_error))
            return {
                "statusCode": 500,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Failed to insert into RDS", "details": str(rds_error)})
            }

        # Send message to SQS
        try:
            sqs_message = {
                "id": item_id,
                "name": name,
                "email": email,
                "event": event_name
            }
            response = sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(sqs_message)
            )
            print("SQS Response:", response)
        except Exception as sqs_error:
            print("SQS Send Error:", str(sqs_error))

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Registration successful!", "item": item})
        }

    except Exception as e:
        print("Unexpected Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
