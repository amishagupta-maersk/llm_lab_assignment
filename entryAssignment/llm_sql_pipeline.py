import logging
import os

from openai import AzureOpenAI
import pandas as pd
import sqlite3
import re
from typing import Union
import unittest

from entryAssignment.olist_dataset import OlistDatasetInfo

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === Azure OpenAI Setup ===
endpoint = os.getenv("DH_ENDPOINT")
api_key=os.getenv("DH_API_KEY")
deployment = "gpt-4o"
api_version = "2024-12-01-preview"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key
)

# === DB Access ===
def query_db(sql: str) -> pd.DataFrame:
    try:
        with sqlite3.connect("olist.sqlite") as conn:
            df = pd.read_sql_query(sql, conn)
        logging.info("Query executed successfully.")
        return df
    except Exception as e:
        logging.error(f"Query failed:\n{sql}")
        raise e

# === Prompt Builder ===
def generate_sql_from_prompt(question: str, schema_hint: str = "") -> str:
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system",
                 "content": "You are an expert in Olist's DB. Return only valid SQL. No explanation or markdown."},
                {"role": "user",
                 "content": f"Dataset info:\n{schema_hint}\n\nQuestion:\n{question}"}
            ],
            temperature=0.0,
        )

        sql_code = response.choices[0].message.content  # ✅ CORRECTED this line

        # Optional: Clean output (useful if LLM adds any extra lines)
        match = re.search(r"(SELECT .*?;?$)", sql_code, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else sql_code.strip()

    except Exception as e:
        logging.error(f"LLM failed to generate SQL for: {question}")
        raise e

# === Basic SQL Safety Check ===
def is_safe_sql(sql: str) -> bool:
    forbidden = ['DROP', 'DELETE', 'UPDATE', 'ALTER', 'INSERT']
    return not any(cmd in sql.upper() for cmd in forbidden)

# === Pipeline ===
def run_llm_query(question: str, expected_type: type) -> Union[int, float, str, pd.DataFrame]:
    schema_hint = OlistDatasetInfo.get_dataset_info()
    sql = generate_sql_from_prompt(question, schema_hint)

    if not is_safe_sql(sql):
        raise ValueError(f"Unsafe SQL detected:\n{sql}")

    result = query_db(sql)

    # Auto-cast to expected type for scalar outputs
    if expected_type in [int, float, str] and len(result) == 1 and len(result.columns) == 1:
        val = result.iloc[0, 0]
        if expected_type == float:
            return float(val)
        return expected_type(val)

    return result

# === Questions & Expected Output Types ===
QUESTIONS = [
    ("Which seller has delivered the most orders to customers in Rio de Janeiro?", str),
    ("What's the average review score for products in the 'beleza_saude' category?", float),
    ("How many sellers have completed orders worth more than 100,000 BRL in total?", int),
    ("Which product category has the highest rate of 5-star reviews?", str),
    ("What's the most common payment installment count for orders over 1000 BRL?", int),
    ("Which city has the highest average freight value per order?", str),
    ("What's the most expensive product category based on average price?", str),
    ("Which product category has the shortest average delivery time?", str),
    ("How many orders have items from multiple sellers?", int),
    ("What percentage of orders are delivered before the estimated delivery date?", float)
]

# # === Unit Tests ===
# class TestLLMQueries(unittest.TestCase):
#     def test_queries(self):
#         for q, expected_type in QUESTIONS:
#             with self.subTest(q=q):
#                 try:
#                     result = run_llm_query(q, expected_type)
#                     self.assertIsInstance(result, expected_type)
#                     logging.info(f"✅ Test passed for: {q} → {result}")
#                 except Exception as e:
#                     logging.error(f"❌ Test failed for: {q} → {e}")
#                     self.fail(str(e))
#
# # === Run Tests ===
# if __name__ == "__main__":
#     unittest.main()

from typing import Union
import pandas as pd
import logging


def run_single_question(question: str, expected_type: type) -> Union[int, float, str, pd.DataFrame]:
    schema_hint = OlistDatasetInfo.get_dataset_info2()
    sql = generate_sql_from_prompt(question, schema_hint)

    sql = sql.strip().rstrip(";")
    print(f"\n🔍 Generated SQL:\n{sql}")

    if not is_safe_sql(sql):
        raise ValueError(f"❌ Unsafe SQL detected:\n{sql}")

    result = query_db(sql)

    if expected_type in [int, float, str] and len(result) == 1 and len(result.columns) == 1:
        val = result.iloc[0, 0]
        try:
            return expected_type(val)
        except Exception as e:
            logging.warning(f"⚠️ Failed to cast result to {expected_type}: {e}")
            return val  # fallback

    return result


if __name__ == "__main__":
    user_question = "Which seller has delivered the most orders to customers in Rio de Janeiro?"
    expected_type = str  # Change based on your expected output type
    answer = run_single_question(user_question, expected_type)
    print(f"\n✅ Final Answer: {answer}")

