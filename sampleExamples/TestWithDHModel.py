import os
from openai import AzureOpenAI

# Configuration
endpoint = os.getenv("DH_ENDPOINT")
model_name = "gpt-4o"
deployment = "gpt-4o"
api_version = "2024-12-01-preview"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=os.getenv("DH_API_KEY")
)

# Create chat completion
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?"
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

# Print the response
print(response.choices[0].message.content)
