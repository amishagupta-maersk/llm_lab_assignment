import os
import json
import dotenv
from openai import AzureOpenAI
from olist_dataset import OlistDatasetInfo  # Import the dataset info class

# Load environment variables from .env file
dotenv.load_dotenv()


class SQLQueryGeneratorWithJsonSchema:
    """A class to generate SQL queries based on user questions using OpenAI's structured output."""

    def __init__(self):
        """Initializes the OpenAI client using Azure credentials from environment variables."""
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

        if not all([azure_endpoint, openai_api_key, azure_openai_api_version]):
            raise ValueError("Missing required Azure OpenAI environment variables")

        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=openai_api_key,
            api_version=azure_openai_api_version
        )

        # Define the response format using JSON Schema
        self.response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "sql_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Short chain-of-thought steps explaining the logic"
                        },
                        "sql_query": {
                            "type": "string",
                            "description": "The final SQL query to answer the user request"
                        }
                    },
                    "required": ["steps", "sql_query"],
                    "additionalProperties": False
                }
            }
        }

    def generate_sql_query(self, user_question):
        """
        Generates an SQL query and explanation based on the Olist dataset.

        Parameters:
        - user_question (str): The SQL-related question from the user.

        Returns:
        - steps (list): Explanation of the query in multiple steps.
        - sql_query (str): The generated SQL query.
        """
        dataset_info = OlistDatasetInfo.get_dataset_info2()  # Retrieve dataset information

        messages = [
            {"role": "system",
             "content": "You are an expert in Olist's DB. Provide 1-3 short reasoning steps, then a final SQL."},
            {"role": "user", "content": f"Dataset info: {dataset_info}\n\nQuestion: {user_question}"}
        ]

        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format=self.response_format
        )

        # Extract response content (JSON string) and parse it
        response_text = completion.choices[0].message.content
        response_data = json.loads(response_text)

        # Extract steps and SQL query
        steps = response_data.get("steps", ["No explanation provided."])
        sql_query = response_data.get("sql_query", "No SQL query generated.")

        return steps, sql_query