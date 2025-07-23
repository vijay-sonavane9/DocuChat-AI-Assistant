import boto3
import json
import os

# Optional: set region and model in env vars
REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-instant-v1")

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

def query_bedrock(prompt: str) -> str:
    body = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 0.9,
        "stop_sequences": ["\n\nHuman:"]
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response['body'].read())
    return response_body['completion'].strip()
