import json
import boto3
from app.core.config import get_settings

def load_runtime_secret() -> dict[str, str]:
    """Optional production bootstrap. ECS task role grants secretsmanager:GetSecretValue."""
    secret_id = get_settings().secrets_manager_secret_id
    if not secret_id:
        return {}
    client = boto3.client("secretsmanager", region_name=get_settings().aws_region)
    return json.loads(client.get_secret_value(SecretId=secret_id)["SecretString"])
