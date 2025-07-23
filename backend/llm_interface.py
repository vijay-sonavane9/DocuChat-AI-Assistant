# backend/llm_interface.py
import boto3
import json

def call_bedrock(prompt: str) -> str:
    bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps({
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7
        }),
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['completion']
