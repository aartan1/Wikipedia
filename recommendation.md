# Architectural Recommendations & Trade-offs

This document outlines the technical decisions made during the development of the Local Wikipedia RAG Assistant and provides recommendations for deploying a similar system in a production environment.

## 1. Architectural Decisions and Trade-offs

### 1.1 Single Vector Store vs. Multiple Vector Stores
*   **Decision:** We opted for **Option B** (One vector store with metadata filtering) rather than separating people and places into different databases.
*   **Trade-off:** 
    *   *Pros:* Simplifies the architecture. It allows for "mixed" queries (e.g., "Compare Albert Einstein and the Eiffel Tower") without needing complex cross-database search logic.
    *   *Cons:* Requires an intent-classification step before querying to apply the correct metadata filters, adding slight overhead to the retrieval pipeline.

### 1.2 Embedding Model Selection
*   **Decision:** We transitioned from `nomic-embed-text` (via Ollama) to `all-MiniLM-L6-v2` (via `sentence-transformers`).
*   **Trade-off:**
    *   While Ollama provides a unified API, `sentence-transformers` allows for direct, in-memory batch processing using PyTorch. This significantly reduced the database ingestion time from hours to seconds on standard hardware, leveraging local GPU/CPU optimizations much more effectively.

### 1.3 Strict Prompting for Hallucination Prevention
*   **Decision:** The LLM is heavily constrained by the prompt to output exactly "I don't know" if the context lacks the answer.
*   **Trade-off:** This successfully eliminates hallucinations (as proven by the "President of Mars" test), but it makes the model overly rigid. The model sacrifices conversational fluidity for absolute factual accuracy.

## 2. Recommendations for Production Deployment

If this system were to be scaled for production use, the following improvements should be implemented:

1.  **Advanced Intent Classification:** Replace the simple keyword-based routing (e.g., looking for "who" or "where") with a lightweight zero-shot classification model. This would improve the accuracy of metadata filtering for complex user queries.
2.  **Semantic Chunking:** Instead of fixed-size character chunking (1000 chars), implement semantic chunking (e.g., splitting by paragraphs or natural sentence boundaries) using libraries like NLTK or SpaCy. This ensures that context isn't arbitrarily cut off mid-sentence.
3.  **Streaming Responses:** Implement server-sent events (SSE) in the Streamlit UI to stream the LLM's response token-by-token. This drastically reduces the perceived latency for the user.
4.  **Re-ranking:** Implement a cross-encoder model to re-rank the retrieved chunks before sending them to the LLM. This ensures the most relevant context is prioritized in the prompt window.