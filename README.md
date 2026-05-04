# Local Wikipedia RAG Assistant 🤖

This project is a fully local, offline Retrieval-Augmented Generation (RAG) system built as a ChatGPT-style assistant. It ingests data from Wikipedia, stores it in a local vector database, and uses a local Large Language Model (LLM) to answer user queries about famous people and places without any external APIs.

## 🚀 Architecture & Tech Stack

*   **Language:** Python 3
*   **Local LLM:** Llama 3.2 (3B parameters) via Ollama
*   **Embeddings:** `all-MiniLM-L6-v2` via `sentence-transformers` (Optimized for local CPU/GPU batch processing)
*   **Vector Store:** ChromaDB (Persistent local storage)
*   **UI:** Streamlit
*   **Data Source:** Wikipedia API (25 Famous People & 25 Famous Places)

## ⚙️ Setup & Installation

**1. Clone the repository and navigate to the project directory:**
```bash
git clone <your-github-repo-url>
cd <your-repo-folder>
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate  
# For Mac/Linux:
source venv/bin/activate
```

**3. Install the required Python dependencies:**
```bash
pip install wikipedia chromadb sentence-transformers torch streamlit requests
```

**4. Install Ollama and the Local LLM:**
*   Download and install [Ollama](https://ollama.com/).
*   Open your terminal and pull the required model:
```bash
ollama pull llama3.2
```

## 🛠️ How to Run the System

To build the database and start the chat interface, run the following scripts in order:

**Step 1: Ingest Data (`ingest.py`)**
Fetches 50 Wikipedia articles (25 people, 25 places) and saves them locally as `.txt` files.
```bash
python ingest.py
```

**Step 2: Create the Vector Database (`store.py`)**
Chunks the text files, generates embeddings using `sentence-transformers`, and stores them in ChromaDB.
```bash
python store.py
```

**Step 3: Launch the Chat Interface (`app.py`)**
Starts the Streamlit web application.
```bash
streamlit run app.py
```

## 🧪 Example Queries to Try

You can test the system with the following queries:

*   **Person Query:** "What is Marie Curie famous for discovering?"
*   **Place Query:** "Where is the Great Wall of China located and why is it important?"
*   **Anti-Hallucination Test (Failure Case):** "Who is the president of Mars?" *(The system is strictly prompt-engineered to reply "I don't know" to prevent hallucination).*

## 📁 Repository Structure
*   `ingest.py`: Script to fetch Wikipedia data.
*   `store.py`: Script to chunk data and build the ChromaDB vector store.
*   `app.py`: Streamlit application and LLM integration.
*   `product_prd.md`: Product Requirements Document.
*   `recommendation.md`: Architectural decisions and production recommendations.