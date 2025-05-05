# 📡 Portfolio Bot Backend

This is the backend API for the **Portfolio Bot**, built with **FastAPI**, designed to handle user queries using a custom Retrieval-Augmented Generation (RAG) pipeline powered by LLMs.

---

## 🚀 Features

- ✅ FastAPI-powered REST API
- 🤖 Loads custom Vector Store and LLM Chain
- 🧠 Handles dynamic chat queries
- 🔁 Supports vector store rebuild via endpoint
- ⚙️ Ready for deployment on Render

---

## 🍀 UV

build with [UV ](https://docs.astral.sh/uv/)
An extremely fast Python package and project manager, written in Rust.

---

## 🌐 Deployment (Render.com)


Build Command:
```
pip install -r requirements.txt
```

Start Command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 📃 License

This project is licensed under the [MIT License](./LICENSE).
