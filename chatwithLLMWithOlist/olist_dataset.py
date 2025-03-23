class OlistDatasetInfo:
    """
    This class provides a structured description of the Olist dataset,
    making it easier for AI models to understand and generate accurate SQL queries.
    """

    @staticmethod
    def get_dataset_info():
        return """
        The Olist dataset contains order-related information from an e-commerce platform. 
        Below is a detailed description of each table.

        --- 

        ### ** 1. Table: `orders`**
        Stores details about customer orders, including timestamps and delivery status.

        **Columns:**
        - `order_id` (STRING, PRIMARY KEY): Unique identifier for each order (UUID).
        - `customer_id` (STRING, FOREIGN KEY): Links order to a customer.
        - `order_status` (STRING): Current order status (e.g., 'shipped', 'delivered', 'canceled').
        - `order_purchase_timestamp` (DATETIME): Timestamp when the order was placed.
        - `order_approved_at` (DATETIME): Timestamp when the payment was approved.
        - `order_delivered_carrier_date` (DATETIME): When the order was handed over to the shipping carrier.
        - `order_delivered_customer_date` (DATETIME): When the customer received the order.
        - `order_estimated_delivery_date` (DATETIME): Estimated delivery date.

        **Sample Data:**
        ```sql
        INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date) 
        VALUES 
        ('949d5b44dbf5de918fe9c16f97b45f8a', 'f88197465ea7920adcdbec7375364d82', 'delivered', '2017-11-18 19:28:06', '2017-11-18 19:45:59', '2017-11-22 13:39:59', '2017-12-02 00:28:42', '2017-12-15 00:00:00');
        ```

        --- 

        ### ** 2. Table: `order_items`**
        Stores details of individual items in an order.

        **Columns:**
        - `order_id` (STRING, FOREIGN KEY): Links item to an order.
        - `order_item_id` (STRING): Sequential ID for each item in an order.
        - `product_id` (STRING, FOREIGN KEY): Links item to a product.
        - `seller_id` (STRING, FOREIGN KEY): Identifies the seller.
        - `shipping_limit_date` (DATETIME): Deadline for shipping the item.
        - `price` (FLOAT): Price of the item.
        - `freight_value` (FLOAT): Total price paid for shipping.

        **Sample Data:**
        ```sql
        INSERT INTO order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value)
        VALUES ('00010242fe8c5a6d1ba2dd792cb16214', 1, '4244733e06e7ecb4970a6e2683c13e61', '48436dade18ac8b2bce089ec2a041202', '2017-09-19 09:45:35', 58.9, 13.29);
        ```

        --- 

        ### ** 3. Table: `order_payments`**
        Stores payment details for each order.

        **Columns:**
        - `order_id` (STRING, FOREIGN KEY): Links to an order.
        - `payment_sequential` (INT): Unique sequential ID for each payment.
        - `payment_type` (STRING): Payment method (e.g., credit_card, debit_card, boleto).
        - `payment_installments` (INT): Number of payment installments.
        - `payment_value` (FLOAT): Total payment amount.

        **Sample Data:**
        ```sql
        INSERT INTO order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value)
        VALUES ('8cd68144cdb62dc0d60848cf8616d2a4', 1, 'boleto', 1, 330.66);
        ```

        --- 

        ### ** 4. Table: `order_reviews`**
        Stores customer reviews for orders.

        **Columns:**
        - `review_id` (STRING, PRIMARY KEY): Unique review identifier.
        - `order_id` (STRING, FOREIGN KEY): Links to an order.
        - `review_score` (INT): Rating given by the customer (1-5).
        - `review_comment_title` (STRING, NULLABLE): Title of the review.
        - `review_comment_message` (STRING, NULLABLE): Review message.
        - `review_creation_date` (DATETIME): When the review was created.
        - `review_answer_timestamp` (DATETIME): When the review was answered.

        **Sample Data:**
        ```sql
        INSERT INTO order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp)
        VALUES ('373cbeecea8286a2b66c97b1b157ec46', '583174fbe37d3d5f0d6661be3aad1786', 1, 'Não chegou meu produto', 'Péssimo', '2018-08-15 00:00:00', '2018-08-15 04:10:37');
        ```

        --- 

        ### ** 5. Table: `customers`**
        Stores customer details.

        **Columns:**
        - `customer_id` (STRING, PRIMARY KEY): Unique customer ID.
        - `customer_unique_id` (STRING): Unique identifier across multiple orders.
        - `customer_zip_code_prefix` (STRING): Customer's zip code prefix.
        - `customer_city` (STRING): City of the customer.
        - `customer_state` (STRING): State of the customer.
        
        **Sample Data:**
        ```sql
        INSERT INTO "customers" ("customer_id","customer_unique_id","customer_zip_code_prefix","customer_city","customer_state") 
        VALUES ('a7c125a0a07b75146167b7f04a7f8e98','5c2991dbd08bbf3cf410713c4de5a0b5',22750,'rio de janeiro','RJ');
        ```

        --- 

        ### ** 6. Table: `sellers`**
        Stores seller details.

        **Columns:**
        - `seller_id` (STRING, PRIMARY KEY): Unique seller ID.
        - `seller_zip_code_prefix` (STRING): Seller's zip code prefix.
        - `seller_city` (STRING): Seller's city.
        - `seller_state` (STRING): Seller's state.
        
        **Sample Data:**
        ```sql
        INSERT INTO "sellers" ("seller_id","seller_zip_code_prefix","seller_city","seller_state") 
        VALUES ('c0f3eea2e14555b6faeea3dd58c1b1c3',4195,'sao paulo','SP');
        ```

        --- 

        ### ** 7. Table: `products`**
        Stores product details.

        **Columns:**
        - `product_id` (STRING, PRIMARY KEY): Unique product ID.
        - `product_category_name` (STRING): Product category name.
        - `product_name_length` (INT): Length of the product name.
        - `product_description_length` (INT): Length of the product description.
        - `product_photos_qty` (INT): Number of product images.
        - `product_weight_g` (FLOAT): Product weight in grams.
        - `product_length_cm` (FLOAT): Product length in cm.
        - `product_height_cm` (FLOAT): Product height in cm.
        - `product_width_cm` (FLOAT): Product width in cm.
        
        **Sample Data:**
        ```sql
        INSERT INTO "products" ("product_id","product_category_name","product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm") 
        VALUES ('1e9e8ef04dbcff4541ed26657ea517e5','perfumaria',40.0,287.0,1.0,225.0,16.0,10.0,14.0);
        ```

        --- 

        ### ** 8. Table: `geolocation`**
        Stores geolocation data.

        **Columns:**
        - `geolocation_zip_code_prefix` (STRING): Zip code prefix.
        - `geolocation_lat` (FLOAT): Latitude.
        - `geolocation_lng` (FLOAT): Longitude.
        - `geolocation_city` (STRING): City name.
        - `geolocation_state` (STRING): State name.
        
        **Sample Data:**
        ```sql
        INSERT INTO "geolocation" ("geolocation_zip_code_prefix","geolocation_lat","geolocation_lng","geolocation_city","geolocation_state") 
        VALUES (12243,-23.1950788950892,-45.8916570319119,'sao jose dos campos','SP');
        ```

        --- 

        ### ** 9. Table: `leads_closed`**
        Stores information about successfully converted sales leads.

        **Columns:**
        - `mql_id` (STRING): Unique Marketing Qualified Lead ID.
        - `seller_id` (STRING, FOREIGN KEY): Associated seller.
        - `won_date` (DATETIME): Date when the lead converted.
        - `business_segment` (STRING): Business category.
        - `lead_type` (STRING): Classification of lead (e.g., online_medium, offline).
        
        **Sample Data:**
        ```sql
        INSERT INTO "leads_closed" ("mql_id","seller_id","sdr_id","sr_id","won_date","business_segment","lead_type","lead_behaviour_profile","has_company","has_gtin","average_stock","business_type","declared_product_catalog_size","declared_monthly_revenue") 
        VALUES ('bae38661a27f6228ba38c36e766ed769','6a6b1614baaaf766293c17d8cb8c5a9d','f42a2bd194f7802ab052a815c8de65b7','495d4e95a8cf8bbf8b432b612a2aa328','2018-09-10 14:18:01','stationery','industry','cat',NULL,NULL,'20-50','reseller',2000.0,100000.0);
        ```

        --- 

        ### ** 10. Table: `leads_qualified`**
        Stores information about qualified leads.

        **Columns:**
        - `mql_id` (STRING): Unique ID.
        - `first_contact_date` (DATETIME): Date of first contact.
        - `landing_page_id` (STRING): Landing page identifier.
        - `origin` (STRING): Lead source (e.g., email, social).
        
        **Sample Data:**
        ```sql
        INSERT INTO "leads_qualified" ("mql_id","first_contact_date","landing_page_id","origin") 
        VALUES ('f76136f54d14a3345951f25b7932366b','2018-05-24','d51b0d02f063ba1d053db6d97226eec3','email');
        ```

        ---
        
        ### ** 11. Table: `product_category_name_translation`**
        Stores information about qualified leads.

        **Columns:**
        - `product_category_name` (STRING): product category name in Portuguese.
        - `product_category_name_english` (STRING): product category name translation in english.
        
        **Sample Data:**
        ```sql
         INSERT INTO "product_category_name_translation" ("product_category_name","product_category_name_english") 
         VALUES ('beleza_saude','health_beauty');
        ```
        
        ## Relationships among tables -
        
        - Orders contain Order Items, Order Payments, and Order Reviews.
         - Orders are placed by Customers.
         - Order Items include Products and are sold by Sellers.
         - Sellers and Customers are located in a specific Geolocation.
         - Orders & Customers: Each order (orders table) is linked to a customer (customers table) via customer_id.
         - Orders & Order Items: Each order (orders table) can have multiple items (order_items table) linked via order_id.
         - Order Items & Products: Each item in an order is associated with a product (products table) via product_id.
         - Order Items & Sellers: Each order item is sold by a seller (sellers table) via seller_id.
         - Orders & Payments: Each order (orders table) can have multiple payment transactions (order_payments table) linked via order_id.
         - Orders & Reviews: Customers can leave reviews (order_reviews table) for orders, linked via order_id.
         - Customers & Geolocation: Customers are linked to geolocation data (geolocation table) via customer_zip_code_prefix.
         - Sellers & Geolocation: Sellers are linked to geolocation data (geolocation table) via seller_zip_code_prefix.
         - Products & Product Category Translation: Each product (products table) is categorized, with translations stored in product_category_name_translation.
         - Leads Qualified & Leads Closed: Leads (leads_qualified table) that convert into sales are stored in leads_closed, linked via mql_id.
         - Leads Closed & Sellers: A closed lead is assigned to a seller (sellers table) via seller_id.
   
        """

    @staticmethod
    def get_dataset_info2():
        return """
        # LLM SQL Query Generation Prompt

You are an expert in converting natural language questions to SQL queries for an e-commerce database. Given a question about the Olist database, your task is to write a correct SQL query that will provide the answer.

## Database Schema

```mermaid
erDiagram
    orders ||--o{ order_items : contains
    orders ||--o{ order_payments : has
    orders ||--o{ order_reviews : has
    orders }|--|| customers : placed_by
    order_items }|--|| products : includes
    order_items }|--|| sellers : sold_by
    sellers }|--|| geolocation : located_in
    customers }|--|| geolocation : located_in

    orders {
        string order_id
        string customer_id
        string order_status
        datetime order_purchase_timestamp
        datetime order_approved_at
        datetime order_delivered_carrier_date
        datetime order_delivered_customer_date
        datetime order_estimated_delivery_date
    }

    order_items {
        string order_id
        int order_item_id
        string product_id
        string seller_id
        datetime shipping_limit_date
        float price
        float freight_value
    }

    order_payments {
        string order_id
        int payment_sequential
        string payment_type
        int payment_installments
        float payment_value
    }

    order_reviews {
        string review_id
        string order_id
        int review_score
        string review_comment_title
        string review_comment_message
        datetime review_creation_date
        datetime review_answer_timestamp
    }

    customers {
        string customer_id
        string customer_unique_id
        string customer_zip_code_prefix
        string customer_city
        string customer_state
    }

    sellers {
        string seller_id
        string seller_zip_code_prefix
        string seller_city
        string seller_state
    }

    products {
        string product_id
        string product_category_name
        int product_name_length
        int product_description_length
        int product_photos_qty
        float product_weight_g
        float product_length_cm
        float product_height_cm
        float product_width_cm
    }

    geolocation {
        string geolocation_zip_code_prefix
        float geolocation_lat
        float geolocation_lng
        string geolocation_city
        string geolocation_state
    }
```

## Database Overview

This is a Brazilian e-commerce dataset from Olist Store with the following characteristics:

- **orders**: Contains ~99.4k order records. 97% are 'delivered' status, with others including 'shipped', 'canceled', etc. Timestamps track the order journey from purchase to delivery.
- **order_items**: Contains ~113k records. Each order can have multiple items, with price and freight values for each item.
- **order_payments**: Contains ~104k records. 74% of payments are by credit card, 19% by 'boleto', with installment options ranging from 1-24.
- **customers**: Contains ~99.4k records. Major cities include São Paulo (16%) and Rio de Janeiro (7%), with SP being the most common state (42%).
- **sellers**: Contains ~3k records. Primarily located in São Paulo (22%) and Curitiba (4%), with SP being the most common state (60%).
- **products**: Contains ~33k records. Top categories include 'cama_mesa_banho' (9%) and 'esporte_lazer' (9%).
- **order_reviews**: Contains review scores from 1-5, with comments and timestamps.
- **geolocation**: Contains geographic coordinates for Brazilian ZIP codes.

## Key Relationships and Data Notes

1. Customers and sellers are linked via zip code prefixes to geolocation.
2. The `order_items` table shows how to calculate order totals (item price + freight).
3. Multiple payment methods may appear for a single order.
4. Product categories are in Portuguese (e.g., 'beleza_saude' = health & beauty).
5. Some records contain unusual values (e.g., 'Infinity' for customer_unique_id).
6. Date fields sometimes contain '01/01/0001 00:00:00' as placeholder.
7. Orders can have multiple items from different sellers.

## Guidelines for Query Generation

1. Always begin with understanding what tables need to be joined to answer the question.
2. Ensure proper join conditions between tables (e.g., order_id, customer_id, seller_id, product_id).
3. Handle NULL values appropriately, especially in date fields.
4. For aggregation:
   - Use appropriate aggregate functions (COUNT, AVG, SUM, etc.)
   - Include proper GROUP BY clauses
   - Apply HAVING for filtering aggregated results
5. Always use the correct column names as defined in the schema.
6. For percentage calculations, use floating-point division: `100.0 * COUNT(case) / COUNT(total)`.
7. Use LIMIT 1 for questions asking about a single "most" or "top" item.
8. For date calculations, use JULIANDAY function for SQLite.
9. Return only the required columns mentioned in the question.
10. If review scores are requested, round to 2 decimal places.
11. When filtering by Brazilian states, use the two-letter abbreviations (SP, RJ, MG, etc.).
12. When joining with geolocation table, remember zip codes are only prefixes (first 5 digits).

## Example Questions and Answers

Question: Which seller has delivered the most orders to customers in Rio de Janeiro? [string: seller_id]
```sql
SELECT 
    s.seller_id
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_city = 'rio de janeiro'
    AND o.order_status = 'delivered'
GROUP BY s.seller_id
ORDER BY COUNT(DISTINCT o.order_id) DESC
LIMIT 1;
```

Question: What's the average review score for products in the 'beleza_saude' category? [float: score]
```sql
SELECT 
    ROUND(AVG(r.review_score), 2) as avg_score
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN order_reviews r ON oi.order_id = r.order_id
WHERE p.product_category_name = 'beleza_saude';
```

Question: How many sellers have completed orders worth more than 100,000 BRL in total? [integer: count]
```sql
SELECT COUNT(*) as seller_count
FROM (
    SELECT s.seller_id
    FROM sellers s
    JOIN order_items oi ON s.seller_id = oi.seller_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY s.seller_id
    HAVING SUM(oi.price) > 100000
) high_value_sellers;
```

The expected answer format is indicated in brackets after each question (e.g., [string: seller_id], [float: score], [integer: count]). Make sure your query returns results in exactly this format.
        """
