import streamlit as st
from llm_processor import LocalLLMProcessor

st.set_page_config(page_title="Local LLM OCR Enhancer", layout="wide")

st.title("📄 Local LLM OCR Enhancer")
st.markdown("Enhance OCR output and ask questions using your local LLM (via Ollama).")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    model_name = st.text_input("Ollama Model Name", value="llama3")
    st.info("Make sure you have Ollama running and the model installed: `ollama pull llama3`")

# Initialize Session State
if "enhanced_text" not in st.session_state:
    st.session_state.enhanced_text = ""

# Main Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input OCR Text")
    ocr_input = st.text_area("Paste your raw OCR output here:", height=300)
    
    if st.button("Enhance Text"):
        if ocr_input:
            with st.spinner("Processing with Local LLM..."):
                processor = LocalLLMProcessor(model_name=model_name)
                enhanced = processor.enhance_text(ocr_input)
                st.session_state.enhanced_text = enhanced
            st.success("Enhancement Complete!")
        else:
            st.warning("Please paste some text first.")

with col2:
    st.subheader("Enhanced Output")
    st.text_area("Result:", value=st.session_state.enhanced_text, height=300, key="output_area")

# Query Section
st.divider()
st.subheader("Ask Questions about the Document")
query = st.text_input("Ask a question based on the text:")

if st.button("Get Answer"):
    if st.session_state.enhanced_text and query:
        with st.spinner("Thinking..."):
            processor = LocalLLMProcessor(model_name=model_name)
            answer = processor.query_text(st.session_state.enhanced_text, query)
        st.write("### Answer:")
        st.write(answer)
    elif not st.session_state.enhanced_text:
        st.warning("Please enhance some text first to provide context.")
    else:
        st.warning("Please enter a question.")
