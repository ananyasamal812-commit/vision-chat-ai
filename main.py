from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from model import generate_caption, answer_question
import io
import uuid
from datetime import datetime
from pymongo import MongoClient

# 👇 ADD THIS HERE
from pymongo import MongoClient

# 👇 MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["visionchat"]
collection = db["chats"]

app = FastAPI()
# BLIP models
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    BlipForQuestionAnswering
)

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD MODELS ----------------
print("Loading models... please wait")

# Caption model
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# QA model
qa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
qa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

print("Models loaded successfully!")

# ---------------- ANALYZE (Caption) ----------------
@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    inputs = caption_processor(image, return_tensors="pt")
    output = caption_model.generate(**inputs)

    caption = caption_processor.decode(output[0], skip_special_tokens=True)

    return {"description": caption}


# ---------------- CHAT (Q&A) ----------------

@app.post("/chat")
async def chat_with_image(
    file: UploadFile = File(...),
    question: str = Form(...),
    session_id: str = Form(None)
):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    # ✅ Create session if not exists
    if not session_id:
        session_id = str(uuid.uuid4())

    # ✅ Get AI answer
    answer = answer_question(image, question)

    # 🔥 SAVE USER MESSAGE
    collection.insert_one({
        "session_id": session_id,
        "role": "user",
        "text": question,
        "timestamp": datetime.now()
    })

    # 🔥 SAVE AI RESPONSE
    collection.insert_one({
        "session_id": session_id,
        "role": "ai",
        "text": answer,
        "timestamp": datetime.now()
    })

    return {
        "answer": answer,
        "session_id": session_id
    }

    @app.get("/history/{session_id}")
    async def get_history(session_id: str):
     chats = list(collection.find({"session_id": session_id}, {"_id": 0}))
    return chats

    return {"answer": answer}

    @app.get("/sessions")
    def get_sessions():
     sessions = collection.distinct("session_id")
    return {"sessions": sessions}


    @app.get("/chat/{session_id}")
    def get_chat(session_id: str):
     chats = list(collection.find({"session_id": session_id}, {"_id": 0}))
    return {"messages": chats}