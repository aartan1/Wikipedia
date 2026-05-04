# Product Requirements Document (PRD): Local Wikipedia RAG Assistant

## 1. Product Overview
The Local Wikipedia RAG Assistant is a ChatGPT-style conversational interface that answers user questions about historical figures and famous landmarks. The core value proposition is data privacy and local execution: the system relies entirely on offline, locally hosted models and databases without transmitting data to external APIs.

## 2. Target Audience
*   Students and researchers needing quick, offline factual summaries.
*   Privacy-conscious users who do not want their queries sent to third-party cloud LLMs.
*   Educators demonstrating the capabilities of Retrieval-Augmented Generation (RAG).

## 3. Core Features & Requirements

### 3.1 Data Ingestion (The Knowledge Base)
*   **Requirement:** The system must automatically fetch Wikipedia articles for a predefined list of minimum 20 famous people and 20 famous places.
*   **Implementation:** The system currently fetches 25 people and 25 places using the `wikipedia` Python library, saving the raw text locally.

### 3.2 Chunking and Embedding
*   **Requirement:** Documents must be split into manageable chunks and converted into vector embeddings using a local model.
*   **Implementation:** 
    *   **Chunking Strategy:** Fixed-size chunks of 1000 characters with an overlap of 200 characters to maintain context across boundaries.
    *   **Embedding Model:** `all-MiniLM-L6-v2` via `sentence-transformers`. This was chosen over Ollama's nomic-embed for faster batch processing and better compatibility with local GPU architectures.

### 3.3 Storage and Retrieval
*   **Requirement:** Embeddings must be stored in a local vector database. The system must retrieve relevant chunks based on user queries.
*   **Implementation:** 
    *   **Database:** ChromaDB (Persistent).
    *   **Design Choice (Option B):** A single vector store is used with metadata filtering (`type: people` or `type: places`). This allows for more flexible querying and easier maintenance compared to managing multiple databases.
    *   **Retrieval Logic:** The system uses keyword heuristics (e.g., "who", "he", "where", "city") to determine the intent and applies metadata filters before performing the vector search, returning the top 3 most relevant chunks.

### 3.4 Answer Generation
*   **Requirement:** Use a local LLM to generate an answer grounded ONLY in the retrieved context. It must avoid hallucinations.
*   **Implementation:** 
    *   **LLM:** Llama 3.2 (3B) running locally via Ollama.
    *   **Guardrails:** Strict prompt engineering is applied. If the retrieved context does not contain the answer, the LLM is instructed to reply explicitly with "I don't know."

### 3.5 User Interface
*   **Requirement:** A chat-style interface.
*   **Implementation:** Built with Streamlit, providing a clean chat history, input field, and an expandable section to view the retrieved context (source citation).