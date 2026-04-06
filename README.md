# 🚀 VisionChat AI

A full-stack AI application that allows users to:

- Upload images 🖼️
- Generate captions 🧠
- Ask questions about images 💬
- Store chat history 📂 (MongoDB)

---

## 🛠 Tech Stack

Frontend:
- React.js
- CSS

Backend:
- FastAPI

AI Models:
- BLIP(Image Captioning + VQA)

Database:
- MongoDB

---

## ⚡ Features

- Image Captioning
- Visual Question Answering (VQA)
- Chat history (session-based)
- Responsive design

---

## 🧠 How it Works

1. Upload an image
2. AI generates caption using BLIP model
3. Ask questions about the image
4. AI responds using Visual Question Answering
5. Chat is stored in MongoDB


## ▶️ Run Locally

### 🔹 1. Clone the repository

```bash
git clone https://github.com/ananyasamal812-commit/vision-chat-ai.git
cd vision-chat-ai
```
### 🔹 2. Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
### 🔹 3. Run Frontend

```bash
cd frontend
npm install
npm start
```


