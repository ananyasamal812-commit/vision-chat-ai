from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    BlipForQuestionAnswering
)
from PIL import Image

# Load models once
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

qa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
qa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")


def generate_caption(image: Image.Image):
    inputs = caption_processor(image, return_tensors="pt")
    output = caption_model.generate(**inputs)
    return caption_processor.decode(output[0], skip_special_tokens=True)


def answer_question(image: Image.Image, question: str):

    # 🔥 Add context
    caption = generate_caption(image)

    prompt = f"""
    Image description: {caption}
    Question: {question}
    Give a short and accurate answer:
    """

    inputs = qa_processor(images=image, text=prompt, return_tensors="pt")
    output = qa_model.generate(**inputs)

    return qa_processor.decode(output[0], skip_special_tokens=True)