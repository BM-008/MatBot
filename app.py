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
ENDPOINT = "materialssciencebot"

# Function to call API with improved error handling
def run_flow(message: str):
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60, stream=True)
        response.raise_for_status()  # Raise error for HTTP failures
        
        collected_response = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                collected_response += chunk.decode()
                yield collected_response  # Stream output gradually
        
    except requests.exceptions.RequestException as e:
        yield f"Error: {str(e)}"
    except json.JSONDecodeError:
        yield "Error: Invalid JSON response from API"

# Cache previous API responses to improve performance
@st.cache_data
def get_response(message: str):
    return list(run_flow(message))[-1]  # Get final response

# UI Elements
st.image("img.jpg", use_container_width=True)

st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
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
                response_placeholder = st.empty()
                full_response = ""

                for chunk in run_flow(message):  # Stream response
                    full_response += chunk  # Append the latest chunk
                    response_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")


if __name__ == "__main__":
    main()
