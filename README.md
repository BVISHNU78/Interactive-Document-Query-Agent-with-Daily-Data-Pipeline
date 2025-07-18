# Interactive-Document-Query-Agent-with-Daily-Data-Pipeline
This project is a fully async, agent-powered RAG (Retrieval-Augmented Generation) system. Users can chat with a local LLM (like Qwen or Mistral via Ollama), which responds using **tool calls** that retrieve live, daily-updated federal document data from a local **MySQL** database.

---
DEPLOYED
##https://interactive-document-query-agent-with-daily-data-pipeline-lcho.streamlit.app/
## 🔍 Features

- ⚡ **Async Python backend** using `FastAPI`, `aiohttp`, and `aiomysql`
- 🧠 **Local LLM agent** with function/tool calling support (via Ollama)
- 📅 **Daily-updated MySQL pipeline** fetching data from the [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1/)
- 🔒 Only safe `SELECT` SQL queries — no destructive commands
- 💬 Simple UI (Streamlit) to interact with the agent
- 🚫 No vector DBs, no scraping, no OpenAI API — 100% local

---

## 📦 Technologies Used

| Component        | Tech                          |
|------------------|-------------------------------|
| LLM Inference    | [Ollama](https://ollama.com/) |
| Backend API      | FastAPI                       |
| Data Fetching    | aiohttp, asyncio              |
| Database         | MySQL (via aiomysql)          |
| UI               | Streamlit                     |
| Config           | Python `dotenv`               |

---

## 🚀 Getting Started

### 1. 🔧 Install dependencies
```bash
pip install -r requirements.txt
2. 📁 Configure environment
Create a .env file:

env
Copy
Edit
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=fed_registry
BASE_URL=http://localhost:11434/v1
3. 🏗️ Create MySQL table
sql
Copy
Edit
CREATE TABLE documents (
  document_number VARCHAR(255) PRIMARY KEY,
  title TEXT,
  publication_date DATE,
  agency_names TEXT,
  summary TEXT
);
4. 📥 Run data pipeline
bash
Copy
Edit
python fetch.py
This fetches latest Federal Register documents and stores them in MySQL.

5. 🤖 Start the agent server
bash
Copy
Edit
uvicorn main:app --reload
6. 🖥️ Access the UI
Visit http://127.0.0.1:8000 or use gui.py (Streamlit).

💬 Example Queries to Ask
"Summarize the 5 most recent documents"

"What executive orders were issued last month?"

"List documents mentioning health or pandemic"

"Show latest Sunshine Act Meetings"

📁 Project Structure
plaintext
Copy
Edit
├── app.py              # Agent and LLM logic
├── tools.py            # Tool functions and definitions
├── fetch.py            # Data pipeline from API → MySQL
├── main.py             # FastAPI app
├── gui.py              # Streamlit frontend 
├── .env                # Configuration file
📌 Notes
LLMs like Qwen sometimes hallucinate SQL column names. This project includes guardrails to prevent invalid queries.

Only SELECT queries are allowed via tools.

Avoid querying non-existent columns like topic or created_date.

