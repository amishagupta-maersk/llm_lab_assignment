from openai import AzureOpenAI
import dotenv
import os
import json

dotenv.load_dotenv() #looks in the same dir for a .env file
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_openai_model = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=openai_api_key,
    api_version=azure_openai_api_version
)

completion = client.beta.chat.completions.parse(
    model=azure_openai_api_version,
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"}
    ],
response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "math_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "string"},
                                "output": {"type": "string"}
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False
                        }
                    },
                    "final_answer": {"type": "string"}
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": False
            }
        }
    }
)

# Extract relevant information
response_text = completion.choices[0].message.content  # Extract response content (string)
response_data = json.loads(response_text)  # Convert string to dictionary

# Extract steps and final answer
math_solution = response_data.get("steps", [])
final_answer = response_data.get("final_answer", "No final answer found")

# Print step-by-step solution
print("Step-by-step solution:")
for step in math_solution:
    print(f"- {step['explanation']} -> {step['output']}")

# Print the final answer
print(f"\nFinal Answer: {final_answer}")


