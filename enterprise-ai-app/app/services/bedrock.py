import json
import boto3
from app.core.config import get_settings

class BedrockChat:
    def answer(self, question: str, context: list[dict]) -> str:
        cfg = get_settings()
        prompt = "You are an enterprise assistant. Answer only using context; state when it is insufficient.\n\nContext:\n" + "\n".join(x["text"] for x in context) + f"\n\nQuestion: {question}"
        client = boto3.client("bedrock-runtime", region_name=cfg.aws_region)
        response = client.invoke_model(modelId=cfg.bedrock_model_id, body=json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 800, "messages": [{"role": "user", "content": prompt}]}))
        return json.loads(response["body"].read())["content"][0]["text"]
