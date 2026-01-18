# Local LLM OCR Enhancer

This application takes raw text output from an OCR system (like Donut or Tesseract), enhances it using a locally running Large Language Model (LLM), and allows you to ask questions about the content.

It runs entirely on your local machine to ensure privacy and avoid API costs.

## Prerequisites

1.  **Python 3.8+** installed.
2.  **Ollama** installed and running.
    *   Download from [ollama.com](https://ollama.com/).
    *   Pull a model (e.g., Llama 3): `ollama pull llama3`

## Installation

1.  Clone this repository.
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Make sure Ollama is running (`ollama serve` in a terminal).
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3.  **Enhance**: Paste your raw OCR text into the left text area and click "Enhance Text".
4.  **Query**: Once enhanced, scroll down to the "Ask Questions" section to query the document.

## Structure

*   `app.py`: The main frontend application built with Streamlit.
*   `llm_processor.py`: Handles the logic for connecting to Ollama and processing text.
*   `requirements.txt`: Python dependencies.
