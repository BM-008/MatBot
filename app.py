import requests
from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "478dd003-8ac0-4d40-815e-77e7d1ae9343"
FLOW_ID = "0853dfd7-558c-4958-9ca4-dc9ca8c69302"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "materialssciencebot" # You can set a specific endpoint name in the flow settings

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
   
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Adding an image at the top
st.image(r"C:/Users/topic/OneDrive/Pictures/WhatsApp Image 2025-02-10 at 16.18.20_a1254462.jpg", use_container_width=True)

st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            padding: 10px;
            font-size: 16px;
            color: #333;
            background-color: #f1f1f1;
        }
    </style>
    <div class="footer">
        Made with ❤️ by Baibhav Malviya
    </div>
""", unsafe_allow_html=True)

def main():
    st.title("Materials Science Bot")
    st.markdown("<h4 style='font-size: 20px;'> Ask anything related to the world of materials! 😉</h4>", unsafe_allow_html=True)
    message = st.text_area("Message", placeholder="What is oxidation?...")

    if st.button("Run"):
        if not message.strip():
            st.error("Please enter a message")
            return
        
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)

            response = response['outputs'][0]['outputs'][0]['results']['message']['text']
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
