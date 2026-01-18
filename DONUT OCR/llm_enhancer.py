import torch
from transformers import AutoModel, AutoTokenizer
from PIL import Image

class GOTEnhancer:
    """
    Uses the GOT-OCR 2.0 model (General OCR Theory) as a VLM to refine/enhance text.
    Model repo: stepfun-ai/GOT-OCR2.0
    """
    def __init__(self, model_name="stepfun-ai/GOT-OCR2.0", device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading GOT-OCR 2.0 model: {model_name} on {self.device}...")
        
        # GOT-OCR 2.0 typically requires trust_remote_code=True
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            model_name, 
            trust_remote_code=True, 
            low_cpu_mem_usage=True, 
            device_map=self.device, 
            use_safetensors=True, 
            pad_token_id=self.tokenizer.eos_token_id
        )
        self.model = self.model.eval()
        if self.device == "cuda":
            self.model = self.model.half() # Use FP16 for speed on GPU

    def enhance_text(self, image_path_or_pil, previous_ocr_text):
        """
        Uses GOT to 're-read' the image specifically looking to verify/correct the provided text.
        """
        if isinstance(image_path_or_pil, str):
            image_path = image_path_or_pil
        else:
            # GOT implementation often expects a file path for its internal processor, 
            # or we need to pass the PIL image directly if the model supports it.
            # For safety in this 'file creation' phase, we assume the model's `chat` API handles paths best.
            # If strictly in-memory, we might need a temp file. Here we assume paths are passed often.
            image_path = "temp_got_input.jpg"
            image_path_or_pil.save(image_path)
        
        # Prompt engineering for "Enhancement".
        # Since GOT is fundamentally an OCR model, asking it to "correct" might be tricky.
        # Strategy: We ask it to output the text in plain format, then validte.
        # OR: We use a specific prompt format if supported.
        # Below is a standard "OCR this" call mixed with the expectation.
        
        # For this prototype, we will use GOT to generate a "high quality" reading
        # and assume it is the "enhanced" version compared to Donut's specialized JSON output.
        # We can also append the specific prompt:
        
        query = "OCR: " # Standard GOT prompt trigger
        
        # Note: True "Language Enhancement" (Text-to-Text) is not GOT's strength. 
        # It is an Image-to-Text model.
        # We will use it to provide a 'Ground Truth' textual representation to compare/merge.
        
        with torch.no_grad():
             # The model.chat signature depends on the specific implementation in remote code
             # Standard pattern for LVLMs:
            res = self.model.chat(self.tokenizer, image_path, ocr_type='ocr')

        return res

if __name__ == "__main__":
    enhancer = GOTEnhancer()
    print("GOT-OCR 2.0 Enhancer initialized.")
