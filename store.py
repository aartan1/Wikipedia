import os
import chromadb
from sentence_transformers import SentenceTransformer
import time

print("Embedding modeli yükleniyor...")
model = SentenceTransformer('all-MiniLM-L6-v2') 

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="wikipedia_rag")

def process_folder(category):
    folder_path = f"data/{category}"
    if not os.path.exists(folder_path): 
        return
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            entity_name = filename.replace(".txt", "").replace("_", " ")
            filepath = os.path.join(folder_path, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            print(f"İşleniyor: {entity_name} ({category})")
            chunks = chunk_text(content)
            
            embeddings = model.encode(chunks).tolist() 
            
            ids = [f"{entity_name}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"type": category, "entity": entity_name} for _ in range(len(chunks))] 
            
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )

print("--- Veriler Parçalanıp ChromaDB'ye Ekleniyor ---")
total_start = time.time()
process_folder("people")
process_folder("places")
print(f"--- İşlem {time.time() - total_start:.2f} saniyede tamamlandı! ---")