"""Example SQS worker for S3-created events; run as a separate ECS service."""
import json
import boto3
from app.core.config import get_settings
from app.services.ingestion.s3_ingestor import ingest_s3_object

def process_once(queue_url: str) -> int:
    sqs = boto3.client("sqs", region_name=get_settings().aws_region)
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=10).get("Messages", [])
    for message in messages:
        event = json.loads(message["Body"])
        for record in event.get("Records", []):
            ingest_s3_object(record["s3"]["bucket"]["name"], record["s3"]["object"]["key"], record.get("tenant_id", "default"))
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
    return len(messages)
