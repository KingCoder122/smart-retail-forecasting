import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"


def load_data():
    customers = pd.read_csv(f"{RAW_PATH}/customers.csv")
    products = pd.read_csv(f"{RAW_PATH}/products.csv")
    transactions = pd.read_csv(f"{RAW_PATH}/transactions.csv")

    return customers, products, transactions


def clean_customers(df):
    df["name"] = df["name"].astype(str)
    df["city"] = df["city"].astype(str)

    # Fill missing ages if any
    df["age"] = df["age"].fillna(df["age"].median())

    # Convert signup_date to datetime
    df["signup_date"] = pd.to_datetime(df["signup_date"])

    return df


def clean_products(df):
    df["product_name"] = df["product_name"].astype(str)
    df["category"] = df["category"].astype(str)
    df["base_price"] = df["base_price"].astype(float)

    return df


def clean_transactions(df):
    df["date"] = pd.to_datetime(df["date"])

    # Ensure numeric types
    df["price"] = df["price"].astype(float)
    df["total_amount"] = df["total_amount"].astype(float)

    # Fill missing quantities if any
    df["quantity"] = df["quantity"].fillna(1)

    return df


def feature_engineering(transactions_df):
    # Extract time features
    transactions_df["year"] = transactions_df["date"].dt.year
    transactions_df["month"] = transactions_df["date"].dt.month
    transactions_df["day"] = transactions_df["date"].dt.day
    transactions_df["day_of_week"] = transactions_df["date"].dt.dayofweek

    # Revenue per transaction is already computed but add a "discounted" signal
    transactions_df["effective_price"] = (
        transactions_df["total_amount"] / transactions_df["quantity"]
    )

    return transactions_df


def save_clean_data(customers, products, transactions):
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    customers.to_csv(f"{PROCESSED_PATH}/customers_clean.csv", index=False)
    products.to_csv(f"{PROCESSED_PATH}/products_clean.csv", index=False)
    transactions.to_csv(f"{PROCESSED_PATH}/transactions_clean.csv", index=False)

    print("Cleaned data saved in data/processed/")


def main():
    customers, products, transactions = load_data()

    customers_clean = clean_customers(customers)
    products_clean = clean_products(products)
    transactions_clean = clean_transactions(transactions)
    transactions_clean = feature_engineering(transactions_clean)

    save_clean_data(customers_clean, products_clean, transactions_clean)
    print("Data cleaning pipeline completed!")


if __name__ == "__main__":
    main()
