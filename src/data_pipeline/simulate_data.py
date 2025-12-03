import numpy as np
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()

# ----------------------------
# PARAMETERS
# ----------------------------
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 120
NUM_TRANSACTIONS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31)

# ----------------------------
# Helper functions
# ----------------------------
def generate_customers(n):
    customers = []
    for i in range(n):
        customers.append({
            "customer_id": i + 1,
            "name": fake.name(),
            "age": random.randint(18, 65),
            "city": fake.city(),
            "signup_date": fake.date_between(start_date="-3y", end_date="today")
        })
    return pd.DataFrame(customers)

def generate_products(n):
    categories = ["Electronics", "Grocery", "Clothing", "Sports", "Home Decor"]
    
    products = []
    for i in range(n):
        category = random.choice(categories)
        base_price = random.uniform(5, 500)
        products.append({
            "product_id": i + 1,
            "product_name": fake.word().capitalize(),
            "category": category,
            "base_price": round(base_price, 2)
        })
    return pd.DataFrame(products)

def generate_transactions(num_tx, customers_df, products_df):
    date_range = (END_DATE - START_DATE).days
    
    transactions = []
    for i in range(num_tx):
        cust = customers_df.sample(1).iloc[0]
        prod = products_df.sample(1).iloc[0]
        
        date = START_DATE + timedelta(days=random.randint(0, date_range))
        quantity = np.random.randint(1, 5)
        price = prod["base_price"] * random.uniform(0.8, 1.2)

        transactions.append({
            "transaction_id": i + 1,
            "customer_id": int(cust["customer_id"]),
            "product_id": int(prod["product_id"]),
            "quantity": quantity,
            "price": round(price, 2),
            "total_amount": round(quantity * price, 2),
            "date": date
        })
    return pd.DataFrame(transactions)

# ----------------------------
# MAIN GENERATION LOGIC
# ----------------------------
def main():
    # Create output folder if not exists
    output_path = "data/raw"
    os.makedirs(output_path, exist_ok=True)

    customers = generate_customers(NUM_CUSTOMERS)
    products = generate_products(NUM_PRODUCTS)
    transactions = generate_transactions(NUM_TRANSACTIONS, customers, products)

    customers.to_csv(f"{output_path}/customers.csv", index=False)
    products.to_csv(f"{output_path}/products.csv", index=False)
    transactions.to_csv(f"{output_path}/transactions.csv", index=False)

    print("Synthetic data generated!")
    print("Files saved in data/raw/")

if __name__ == "__main__":
    main()
