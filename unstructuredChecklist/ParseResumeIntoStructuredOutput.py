import os

from openai import AzureOpenAI
from unstructuredChecklist.ResumeChecklist import ResumeChecklist
import json

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

resume_text = """
Jane Doe is a seasoned software engineer with 5 years of experience in full-stack development.
She holds a Master’s degree in Computer Science. Currently a Senior Developer at TechCorp, Jane has led 3 major projects and is seeking new opportunities with a salary expectation of around $120k.
Her skills include Python, JavaScript, React, and AWS.
"""


# Step 1: Generate JSON Schema from ResumeChecklist
json_schema = ResumeChecklist.model_json_schema()

# Wrap schema as a tool/function definition
tool = {
    "type": "function",
    "function": {
        "name": "extract_resume_fields",  # required by Azure, must be lowercase+underscores
        "description": "Extract structured resume information",
        "parameters": json_schema
    }
}

# Step 2: Create the response_format dict as per SDK spec
response_format = {
    "type": "json_schema",
    "json_schema": json_schema
}

# Make the request using tools and tool_choice
response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "Extract structured details from the resume using the tool."},
        {"role": "user", "content": resume_text}
    ],
    tools=[tool],  # ✅ this replaces response_format
    tool_choice={"type": "function", "function": {"name": "extract_resume_fields"}},  # optional, to force tool call
    max_tokens=4096,
    temperature=0.0,
    top_p=1.0
)

# Extract arguments from tool call
tool_args = response.choices[0].message.tool_calls[0].function.arguments
resume_data = ResumeChecklist(**json.loads(tool_args))

print(json.dumps(resume_data.model_dump(), indent=2))
