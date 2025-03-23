import unittest
import sqlite3
import re  # Import the regex module
from chatwithLLMWithOlist.SQLQueryGeneratorWithJsonSchema import SQLQueryGeneratorWithJsonSchema


class TestSQLQueryGenerator(unittest.TestCase):
    """Test class to validate SQL query generation and execution using an Olist SQLite database."""

    @classmethod
    def setUpClass(cls):
        """Set up the SQLite database connection before running tests."""
        cls.db_path = "../olist.sqlite"  # Path to the SQLite database file
        cls.connection = sqlite3.connect(cls.db_path)
        cls.cursor = cls.connection.cursor()
        cls.sql_generator = SQLQueryGeneratorWithJsonSchema()

    @classmethod
    def tearDownClass(cls):
        """Close the database connection after tests complete."""
        cls.cursor.close()
        cls.connection.close()

    def execute_sql(self, sql_query):
        """Helper function to execute SQL and fetch results."""
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()  # Fetch all rows
        except sqlite3.Error as e:
            self.fail(f"SQL execution failed: {e}")  # Fails test if SQL execution fails

    def normalize_sql(self, sql):
        """Helper function to remove extra spaces, newlines, and normalize SQL."""
        return re.sub(r"\s+", " ", sql.strip()).lower()  # Replace multiple spaces with one & lowercase

    def test_scenario1(self):
        user_question = "Which seller has delivered the most orders to customers in Rio de Janeiro? [string: seller_id]"
        steps, generated_query = self.sql_generator.generate_sql_query(user_question)

        expected_sql_query = """
        SELECT s.seller_id
        FROM sellers s
        JOIN order_items oi ON s.seller_id = oi.seller_id
        JOIN orders o ON oi.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_city = 'rio de janeiro'
        AND o.order_status = 'delivered'
        GROUP BY s.seller_id
        ORDER BY COUNT(DISTINCT o.order_id) DESC
        LIMIT 1;
        """

        expected_seller_id = "4a3ca9315b744ce9f8e9374361493884"

        print("\nGenerated SQL Query:")
        print(generated_query)

        # Normalize both queries before comparing
        self.assertEqual(
            self.normalize_sql(generated_query),
            self.normalize_sql(expected_sql_query),
            "Generated SQL does not match expected SQL."
        )

        try:
            self.cursor.execute(generated_query)
            result = self.cursor.fetchone()  # Fetch the first row

            self.assertIsNotNone(result, "Query returned no results.")
            actual_seller_id = result[0]  # Assuming seller_id is the first column

            print("Seller ID from DB:", actual_seller_id)
            self.assertEqual(expected_seller_id, actual_seller_id, "Seller ID does not match expected.")

        except sqlite3.Error as e:
            self.fail(f"Database execution failed: {e}")  # Fails test if SQL execution fails


    """Test case failed: generated query has column name as avg_score instead of average_review_score"""
    def test_scenario2(self):
        user_question = "What's the average review score for products in the 'beleza_saude' category? [float: average_review_score]"
        steps, generated_query = self.sql_generator.generate_sql_query(user_question)

        expected_sql_query = """
        SELECT 
            ROUND(AVG(r.review_score), 2) as avg_score
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN order_reviews r ON oi.order_id = r.order_id
        WHERE p.product_category_name = 'beleza_saude';
        """

        expected_average_review_score = 4.14

        print("\nGenerated SQL Query:")
        print(generated_query)

        # Normalize both queries before comparing
        self.assertEqual(
            self.normalize_sql(generated_query),
            self.normalize_sql(expected_sql_query),
            "Generated SQL does not match expected SQL."
        )

        try:
            self.cursor.execute(generated_query)
            result = self.cursor.fetchone()  # Fetch the first row

            self.assertIsNotNone(result, "Query returned no results.")
            actual_average_review_score = result[0]  # Assuming avg_score is the first column

            print("Average Review Score from DB:", actual_average_review_score)

            # Round both values for comparison
            self.assertEqual(
                round(expected_average_review_score, 2),
                round(actual_average_review_score, 2),
                "Average review score does not match expected."
            )

        except sqlite3.Error as e:
            self.fail(f"Database execution failed: {e}")  # Fails test if SQL execution fails




if __name__ == "__main__":
    unittest.main()