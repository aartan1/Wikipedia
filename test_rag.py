import chromadb
import requests
import time
from sentence_transformers import SentenceTransformer

print("⚙️ Test ortamı hazırlanıyor ve modeller yükleniyor...\n")

# 1. Modelleri ve Veritabanını Yükle
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="wikipedia_rag")

# 2. Yardımcı Fonksiyonlar (app.py'deki mantığın aynısı, arayüzsüz hali)
def get_embedding(text):
    return embed_model.encode(text).tolist()

def determine_category(query):
    query_lower = query.lower()
    person_keywords = ["who", "person", "he", "she", "his", "her", "born", "discover", "famous"]
    place_keywords = ["where", "place", "located", "city", "country", "built", "used"]
    
    is_person = any(word in query_lower for word in person_keywords)
    is_place = any(word in query_lower for word in place_keywords)
    
    if is_person and not is_place: return {"type": "people"}
    elif is_place and not is_person: return {"type": "places"}
    else: return None

def retrieve_context(query):
    query_embedding = get_embedding(query)
    where_filter = determine_category(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where=where_filter
    )
    if not results["documents"][0]: return ""
    return "\n...\n".join(results["documents"][0])

def generate_answer(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2", # GTX 1650'ye uygun 3B modelimiz
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()["response"]

# 3. TEST SORULARI
test_queries = [
    "What is Marie Curie famous for discovering?",
    "Where is the Great Wall of China located and why is it important?",
    "Who is the president of Mars?"  # Halüsinasyon testi (Cevabı veritabanında yok)
]

print("🚀 OTOMATİK TEST BAŞLIYOR...\n" + "="*50)

# 4. Test Döngüsü
for i, query in enumerate(test_queries, 1):
    print(f"Soru {i}: {query}")
    
    start_time = time.time()
    
    # Adım 1: Bağlamı Bul
    context = retrieve_context(query)
    
    # Adım 2: Llama'ya Gönder (Kesin Kurallı Prompt)
    llm_prompt = f"""You are a helpful and detailed AI assistant. Based ONLY on the following context, provide a comprehensive and informative answer to the user's question. Extract the most important facts. Write at least 2-3 sentences.
If the answer is not contained in the context, you MUST say exactly "I don't know". Do not make up information.

Context:
{context}

Question: {query}
Detailed Answer:"""
    
    answer = generate_answer(llm_prompt)
    end_time = time.time()
    
    # Sonuçları Raporla
    print(f"Cevap: {answer}")
    print(f"⏱️ Yanıt Süresi: {end_time - start_time:.2f} saniye")
    print("-" * 50)

print("\n✅ TEST TAMAMLANDI!")