"""S3-to-Qdrant ingestion skeleton; invoke from EventBridge/SQS worker in production."""
import boto3
from qdrant_client.models import PointStruct
from app.core.config import get_settings
from app.services.retriever import QdrantRetriever

def ingest_s3_object(bucket: str, key: str, tenant_id: str) -> int:
    # Production: malware scan first, extract PDF/DOCX with a hardened service, classify PII.
    body = boto3.client("s3", region_name=get_settings().aws_region).get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8")
    retriever = QdrantRetriever(); retriever.ensure_collection()
    chunks = [body[i:i + 1000] for i in range(0, len(body), 850)]
    points = [PointStruct(id=abs(hash(f"{tenant_id}:{key}:{i}")) % (2**63), vector=retriever.embed(text), payload={"text": text, "tenant_id": tenant_id, "s3_uri": f"s3://{bucket}/{key}"}) for i, text in enumerate(chunks)]
    retriever.client.upsert(retriever.cfg.qdrant_collection, points=points)
    return len(points)
