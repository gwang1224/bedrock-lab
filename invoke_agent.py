import boto3
import json

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = client.invoke_agent(
    agentId='NWGB4HEP4Y',
    agentAliasId='ZJYZIZNSQW',
    sessionId='test-session-001',
    inputText='What are the fees associated with an account?',
    enableTrace=True
)

completion_stream = response['completion']
full_response = ""

for event in completion_stream:
    if 'chunk' in event:
        chunk_bytes = event['chunk']['bytes']
        chunk_str = chunk_bytes.decode("utf-8").strip()

        if chunk_str:
            try:
                decoded = json.loads(chunk_str)
                full_response += decoded.get("content", "")
            except json.JSONDecodeError:
                print("Skipping invalid JSON chunk:", chunk_str)

print("Agent response:", full_response)
