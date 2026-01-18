import gradio as gr
import os
import json
from pathlib import Path
from ocr_engine import DonutOCR
from llm_enhancer import GOTEnhancer
from PIL import Image

# Initialize Models (Lazy loading recommended for apps, but we do it globally for simple demo)
# Note: This will download GBs of data on first run.
print("Initializing models... (This may take time)")
try:
    donut_engine = DonutOCR()
    # got_engine = GOTEnhancer() # Uncomment if you have GPU and want to load both at once. 
    # For a GitHub demo, we might want to flag this.
    got_engine = None 
except Exception as e:
    print(f"Error loading models: {e}")
    donut_engine = None
    got_engine = None

def process_file(file_obj, use_enhancement):
    """
    Main processing pipeline.
    """
    if not donut_engine:
        return "Models not loaded. Check console for errors."

    image = Image.open(file_obj.name).convert("RGB")
    
    # 1. Donut OCR (Structure Extraction)
    print(f"Running Donut on {file_obj.name}...")
    donut_result = donut_engine.process_image(image)
    donut_json_str = json.dumps(donut_result, indent=2)
    
    final_output = f"--- Donut OCR (Structured) ---\n{donut_json_str}\n"

    # 2. GOT Enhancement (VLM Refinement)
    if use_enhancement:
        if got_engine is None:
            # Lazy load GOT if selected
            try:
                global got_ocr # Using global to keep it loaded
                if 'got_ocr' not in globals() or got_ocr is None:
                     # This is just a simulation of lazy loading.
                     # In real code, we'd initialize the class instance here.
                     pass 
                # For now, let's assume we proceed or fail gracefully
                final_output += "\n\n--- GOT-OCR 2.0 Enhancement ---\n(GOT Engine not fully loaded in this snippet to save RAM, uncomment in code)\n"
                # real call:
                # got_res = got_engine.enhance_text(image, donut_json_str)
                # final_output += got_res
            except Exception as e:
                final_output += f"\nError in Enhancement: {e}"
        else:
            print(f"Running GOT Enhancement...")
            got_res = got_engine.enhance_text(image, donut_json_str)
            final_output += f"\n\n--- GOT-OCR 2.0 Enhancement ---\n{got_res}"

    return final_output

def app_interface(files, enhance_chk):
    results = []
    if not files:
        return "No files uploaded."
        
    for f in files:
        file_name = os.path.basename(f.name)
        res = process_file(f, enhance_chk)
        results.append(f"### File: {file_name}\n\n{res}\n{'='*40}\n")
    
    return "\n".join(results)

# CSS for a "kickass" look
custom_css = """
body { background-color: #0b0f19; color: #e0e6ed; }
gradio-app { background: transparent; }
.container { max-width: 900px; margin: auto; padding: 20px; }
h1 { font-family: 'Orbitron', sans-serif; color: #00f2ff; text-align: center; font-size: 3em; text-shadow: 0 0 10px #00f2ff; }
.gr-button { background: linear-gradient(45deg, #00c6ff, #0072ff); border: none; color: white; font-weight: bold; transition: 0.3s; }
.gr-button:hover { transform: scale(1.05); box-shadow: 0 0 15px #00c6ff; }
.gr-box { background-color: #16202e; border: 1px solid #2d3748; border-radius: 10px; }
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.HTML("<h1>NEURAL SCAN <span style='font-size:0.5em; opacity:0.7'>v1.0</span></h1>")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload Scanned Docs/Images", file_count="multiple", file_types=["image", ".pdf"])
            enhance_chk = gr.Checkbox(label="Enable GOT-OCR 2.0 Enhancement (Requires GPU)", value=False)
            submit_btn = gr.Button("INITIALIZE SCAN", variant="primary")
        
        with gr.Column(scale=2):
            output_display = gr.Markdown(label="System Output", value="Waiting for input stream...")

    submit_btn.click(fn=app_interface, inputs=[file_input, enhance_chk], outputs=output_display)

if __name__ == "__main__":
    demo.launch()
