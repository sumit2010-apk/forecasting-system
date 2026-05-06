import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title("📊 Sales Forecast Dashboard")

# Input state
state = st.text_input("Enter State (e.g., Alabama):")

if st.button("Get Forecast"):

    url = f"http://127.0.0.1:8000/forecast/{state}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if "error" in data:
            st.error(data["error"])
        else:
            forecast = data["next_8_weeks_forecast"]

            st.success(f"Forecast for {state}")

            # Show numbers
            st.write(forecast)

            # Plot graph
            plt.figure()
            plt.plot(forecast, marker='o')
            plt.title("Next 8 Weeks Forecast")
            plt.xlabel("Weeks")
            plt.ylabel("Sales")

            st.pyplot(plt)

    else:
        st.error(response.text)