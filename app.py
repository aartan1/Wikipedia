import streamlit as st
import chromadb
import requests
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_embedding_model()

def get_embedding(text):
    return model.encode(text).tolist()

def generate_answer(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2",  
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()["response"]

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="wikipedia_rag")

def determine_category(query):
    query_lower = query.lower()
    person_keywords = ["who", "person", "he", "she", "his", "her", "born", "discover", "famous"]
    place_keywords = ["where", "place", "located", "city", "country", "built", "used"]
    
    is_person = any(word in query_lower for word in person_keywords)
    is_place = any(word in query_lower for word in place_keywords)
    
    if is_person and not is_place:
        return {"type": "people"}
    elif is_place and not is_person:
        return {"type": "places"}
    else:
        return None

def retrieve_context(query):
    query_embedding = get_embedding(query)
    where_filter = determine_category(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where=where_filter
    )
    
    if not results["documents"][0]:
        return ""
    
    return "\n...\n".join(results["documents"][0])

st.title("Wikipedia RAG Assistant 🤖")
st.write("Ask me about 25 famous people and 25 famous places!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., Who is Albert Einstein and what is he known for?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching and thinking..."):
            context = retrieve_context(prompt)
            
            llm_prompt = f"""You are a helpful and detailed AI assistant. Based ONLY on the following context, provide a comprehensive and informative answer to the user's question. Extract the most important facts. Write at least 2-3 sentences.
If the answer is not contained in the context, you MUST say exactly "I don't know". Do not make up information.

Context:
{context}

Question: {prompt}
Detailed Answer:"""

            answer = generate_answer(llm_prompt)
            st.markdown(answer)
            
            with st.expander("Show retrieved context (Source)"):
                st.write(context if context else "No context found.")
            
    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()