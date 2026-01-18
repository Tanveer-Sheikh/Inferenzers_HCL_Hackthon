import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import re
import json

class DonutOCR:
    """
    Handles Optical Character Recognition using the Donut model.
    Default model: naver-clova-ix/donut-base-finetuned-cord-v2 (Receipts/Invoices focus)
    """
    def __init__(self, model_name="naver-clova-ix/donut-base-finetuned-cord-v2", device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading Donut model: {model_name} on {self.device}...")
        
        self.processor = DonutProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    def process_image(self, image_path_or_pil):
        """
        Runs the image through Donut and returns the extracted JSON/Text.
        """
        if isinstance(image_path_or_pil, str):
            image = Image.open(image_path_or_pil).convert("RGB")
        else:
            image = image_path_or_pil.convert("RGB")

        # Prepare input
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(pass_device_here_later_fix_this) # Small fix in logic below
        pixel_values = pixel_values.to(self.device)

        # Generate output
        task_prompt = "<s_cord-v2>" # Specific prompt for CORD dataset; change if using different model
        decoder_input_ids = self.processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
        decoder_input_ids = decoder_input_ids.to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                pixel_values,
                decoder_input_ids=decoder_input_ids,
                max_length=self.model.decoder.config.max_position_embeddings,
                early_stopping=True,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True,
                num_beams=1,
                bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
                return_dict_in_generate=True,
            )

        # Decode output
        sequence = self.processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(self.processor.tokenizer.pad_token, "")
        sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
        
        # Convert to JSON if possible
        return self.processor.token2json(sequence)

if __name__ == "__main__":
    # Test stub
    ocr = DonutOCR()
    print("Donut OCR initialized successfully.")
