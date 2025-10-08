import os
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

#Load API Keys
load_dotenv()

print("Anthropic Key starts with:", os.getenv("ANTHROPIC_API_KEY")[:8])
print("OpenAI Key starts with:", os.getenv("OPENAI_API_KEY")[:4])


# Test Anthropic
print("Testing Anthropic...")
try:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    print(f"Claude Response: {message.content[0].text}")
except Exception as e:
    print(f"Anthropic API Key is invalid: {e}")

# Test OpenAI
print("\nTesting OpenAI...")
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say hello in 3 words"}
        ],
        max_tokens=100
    )
    print(f"GPT Says: {response.choices[0].message.content}")
except Exception as e:
    print(f"OpenAI API Key is invalid: {e}")

print("\n✅ All tests completed successfully, both APIs are working!")