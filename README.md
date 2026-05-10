# ⚡ AI Multi-Agent Research Copilot

An AI-powered research copilot that intelligently searches across multiple sources like Arxiv, Tavily, and Firecrawl, then generates concise AI summaries using Groq LLMs.

Built with a modular multi-agent architecture using FastAPI and Streamlit.

---

## 🚀 Features

* 🔍 Multi-source AI retrieval system
* 🧠 Intelligent tool routing
* 📚 Research paper search with Arxiv
* 🌐 Web search using Tavily API
* 🔥 Firecrawl integration for advanced scraping/search
* ⚡ FastAPI backend with streaming responses
* 🤖 LLM-powered summarization using Groq
* 🎨 Clean Streamlit frontend
* 🧩 Modular and scalable tool architecture

---

## 🏗️ Architecture

```text
User Query
   ↓
Tool Router
   ↓
Selected Tool
   ↓
Retriever APIs
(Arxiv / Tavily / Firecrawl)
   ↓
Structured Results
   ↓
Groq LLM Summarizer
   ↓
FastAPI Response
   ↓
Streamlit Frontend
```

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* Python
* StreamingResponse

### AI / LLM

* Groq API
* Llama 3.3 70B
* Multi-Agent Retrieval Pipeline

### APIs

* Arxiv API
* Tavily API
* Firecrawl API

### Frontend

* Streamlit

---

## 📂 Project Structure

```bash
AI-MultiAgent-Copilot/
│
├── tools/
│   ├── arxiv_tools.py
│   ├── tavily_tools.py
│   ├── firecrawl_tool.py
│   ├── tool_manager.py
│   ├── tool_router.py
│   ├── llm_summarizer.py
│   └── formatter.py
│
├── Website/
│   └── backend.py
│
├── app.py
├── requirements.txt
└── .env
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <your-repo-url>
cd AI-MultiAgent-Copilot
```

### Create Environment

```bash
conda create -n yourenv python=3.10
conda activate yourenv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
FIRECRAWL_API_KEY=your_key
```

---

## ▶️ Run Backend

```bash
uvicorn Website.backend:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

## 🎨 Run Frontend

```bash
streamlit run app.py
```

---

## 📡 API Endpoints

### Normal Search

```http
GET /search?query=latest ai research
```

### Streaming Search

```http
GET /search-stream?query=latest ai agents
```

---

## 🧠 Example Query

```text
Latest AI research papers on autonomous agents
```

The system:

* selects the best retrieval tool
* fetches relevant sources
* summarizes insights using Groq LLMs
* streams results in real time

---

## 🚀 Future Improvements

* Async parallel tool execution
* Vector database memory
* Real AI agent tool calling
* Conversation memory
* Token streaming
* Research report generation
* LangSmith observability
* Docker deployment

---

## 👨‍💻 Author

Built by Ibrahim Hajuri
AI/ML Engineer
