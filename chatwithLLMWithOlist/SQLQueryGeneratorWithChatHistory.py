from pydantic import BaseModel, Field
from openai import AzureOpenAI
import dotenv
import os
import json
import time  # For introducing small delays if needed

from chatwithLLMWithOlist.olist_dataset import OlistDatasetInfo

# Load environment variables
dotenv.load_dotenv()
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_openai_model = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Initialize OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=openai_api_key,
    api_version=azure_openai_api_version
)


# Structured output format for generated SQL
class SQLGeneration(BaseModel):
    reasoning: list[str] = Field(..., description="Short reasoning steps explaining the approach")
    sql_query: str = Field(..., description="The final SQL query (PostgreSQL syntax)")


# Function to evaluate SQL quality
def evaluate_sql(generated_sql, correct_sql, query_description):
    """Evaluate the generated SQL against the correct SQL using an LLM"""
    eval_prompt = f"""
    As a SQL expert, evaluate the generated SQL query against the correct SQL query.

    Query task: {query_description}

    Generated SQL: {generated_sql}

    Correct SQL: {correct_sql}

    Provide a JSON response with the following fields:
    - "is_correct": boolean (true if functionally equivalent, false otherwise)
    - "errors": list of string errors if any (empty list if correct)
    - "correction": string with corrected SQL if needed (empty string if correct)
    - "explanation": string explaining what was wrong and how it was fixed
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a SQL expert evaluator."},
                  {"role": "user", "content": eval_prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    return result


# Function to iteratively improve SQL using feedback
def refine_sql_with_feedback(question, correct_sql, system_prompt, max_attempts=3):
    """
    Iteratively improves SQL generation with feedback until correctness is achieved or max attempts reached.
    """
    conversation = [{"role": "system", "content": system_prompt}]

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        print(f"\n Attempt {attempt}: Generating SQL...\n")

        # Ask LLM for SQL query
        messages = conversation + [{"role": "user", "content": question}]
        try:
            completion = client.beta.chat.completions.parse(
                model=azure_openai_model,
                messages=messages,
                response_format=SQLGeneration
            )
            generated_sql = completion.choices[0].message.parsed.sql_query
        except Exception as e:
            raise ConnectionError(f"Error generating SQL: {e}")

        # Evaluate the SQL
        evaluation = evaluate_sql(generated_sql, correct_sql, question)

        # Add generated SQL to conversation history
        conversation.append({"role": "assistant", "content": generated_sql})

        # If correct, return the final SQL
        if evaluation["is_correct"]:
            print("✅ Correct SQL generated on attempt", attempt)
            return generated_sql, conversation

        # If incorrect, provide feedback and retry
        feedback = f"""
        Your SQL query has some issues:
        {evaluation["explanation"]}

        Suggested Correction:
        {evaluation["correction"]}
        """
        print(f"\n SQL Incorrect. Providing feedback...\n{feedback}")

        # Append feedback to conversation
        conversation.append({"role": "user", "content": feedback})

        # Small delay to avoid overwhelming API
        time.sleep(1)

    print(" Maximum attempts reached. Returning last attempted SQL.")
    return generated_sql, conversation


# Example Query Execution with Iterative Refinement
question = "Which product category has the highest rate of 5-star reviews? [string: category_name]"
correct_sql_map = {
    question: """
    SELECT p.product_category_name 
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN order_reviews r ON oi.order_id = r.order_id
    GROUP BY p.product_category_name
    HAVING COUNT(*) > 100
    ORDER BY (COUNT(CASE WHEN r.review_score = 5 THEN 1 END) * 100.0 / COUNT(*)) DESC
    LIMIT 1;
    """
}

# Load dataset info
dataset_info = OlistDatasetInfo.get_dataset_info2()

# Generate and refine SQL iteratively
final_sql, conversation_history = refine_sql_with_feedback(
    question, correct_sql_map[question], dataset_info
)

print("\n Final Optimized SQL:\n", final_sql)
print("\n Full Conversation History:\n", conversation_history)
