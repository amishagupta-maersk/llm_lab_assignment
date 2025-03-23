from chatwithLLMWithOlist.SQLQueryGeneratorWithJsonSchema import SQLQueryGeneratorWithJsonSchema


class SQLQueryExecutor:
    """A class to execute and print results from SQLQueryGenerator."""

    def __init__(self):
        self.sql_generator = SQLQueryGeneratorWithJsonSchema()

    def run(self, user_question):
        """Executes the SQL generation process and prints the results."""
        steps, sql_query = self.sql_generator.generate_sql_query(user_question)

        print("Explanation Steps:")
        for step in steps:
            print("-", step)

        print("\nGenerated SQL Query:")
        print(sql_query)


if __name__ == "__main__":
    executor = SQLQueryExecutor()

    user_questions = [
        "Which seller has delivered the most orders to customers in Rio de Janeiro? [string: seller_id]",
        "What's the average review score for products in the 'beleza_saude' category? [float: score]",
        "How many sellers have completed orders worth more than 100,000 BRL in total? [integer: count]",
        "Which product category has the highest rate of 5-star reviews? [string: category_name]",
        "What's the most common payment installment count for orders over 1000 BRL? [integer: installments]",
        "Which city has the highest average freight value per order? [string: city_name]",
        "What's the most expensive product category based on average price? [string: category_name]",
        "Which product category has the shortest average delivery time? [string: category_name]",
        "How many orders have items from multiple sellers? [integer: count]",
        "What percentage of orders are delivered before the estimated delivery date? [float: percentage]",
    ]

    for question in user_questions:
        executor.run(question)
