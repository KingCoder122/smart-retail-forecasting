import streamlit as st
import requests

API_URL = "http://127.0.0.1:53994"  # replace with your Minikube service URL

st.title("Smart Retail Forecasting Dashboard")
st.subheader("Powered by FastAPI + Kubernetes + Streamlit")

# Forecast Section
st.header("Sales Forecasting")

days = st.slider("Number of days to forecast", 7, 90, 30)

if st.button("Generate Forecast"):
    response = requests.post(f"{API_URL}/forecast", json={"days": days})
    if response.status_code == 200:
        data = response.json()
        st.success("Forecast generated successfully!")

        forecast_data = {"forecast": data["forecast"]}

        # Add bounds if they exist
        if "yhat_lower" in data:
            forecast_data["yhat_lower"] = data["yhat_lower"]

        if "yhat_upper" in data:
            forecast_data["yhat_upper"] = data["yhat_upper"]

        st.line_chart(forecast_data)
    else:
        st.error("Failed to fetch forecast from API")

# Pricing Section
st.header("Optimal Pricing Engine")

base_price = st.number_input("Base Price", value=100)

if st.button("Calculate Optimal Price"):
    response = requests.post(f"{API_URL}/optimal-price", json={"base_price": base_price})
    if response.status_code == 200:
        data = response.json()
        st.success(f"Optimal Price: ₹{data['optimal_price']:.2f}")
    else:
        st.error("Failed to fetch optimal price from API")
