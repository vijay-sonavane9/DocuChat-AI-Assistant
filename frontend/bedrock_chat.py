# bedrock_chat.py
import boto3
import json

def ask_claude(message: str) -> str:
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": message}
        ],
        "max_tokens": 500
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    result = json.loads(response['body'].read())
    return result['content'][0]['text']
