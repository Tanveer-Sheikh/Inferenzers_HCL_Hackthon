import streamlit as st
import requests

st.title("GenAI Form Information Extraction")

BACKEND_URL = "http://127.0.0.1:8000"

user_id = st.text_input("Enter User ID", "pradyumna")
uploaded_file = st.file_uploader("Upload a scanned form")

if st.button("Submit") and uploaded_file is not None:
    files = {"file": uploaded_file}
    data = {"user_id": user_id}

    response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        st.success("File uploaded successfully!")
        st.json(result)

        job_id = result["job_id"]

        job_response = requests.get(f"{BACKEND_URL}/jobs/{job_id}")
        st.subheader("Extraction Result")
        st.json(job_response.json())
    else:
        st.error("Upload failed")
