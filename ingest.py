import wikipedia
import os
import time

wikipedia.set_lang("en")

# Zorunlu liste + 15 ekstra (Toplam 25 kişi)
people = [
    # Zorunlu Liste
    "Albert Einstein", "Marie Curie", "Leonardo da Vinci",
    "William Shakespeare", "Ada Lovelace", "Nikola Tesla",
    "Lionel Messi", "Cristiano Ronaldo", "Taylor Swift", "Frida Kahlo",
    # Ekstralar
    "Isaac Newton", "Galileo Galilei", "Nelson Mandela", "Martin Luther King Jr.",
    "Abraham Lincoln", "Cleopatra", "Julius Caesar", "Mahatma Gandhi",
    "Winston Churchill", "Charles Darwin", "Stephen Hawking", "Marilyn Monroe",
    "Wolfgang Amadeus Mozart", "Vincent van Gogh", "Alexander the Great"
]

# Zorunlu liste + 15 ekstra (Toplam 25 yer)
places = [
    # Zorunlu Liste
    "Eiffel Tower", "Great Wall of China", "Taj Mahal",
    "Grand Canyon", "Machu Picchu", "Colosseum",
    "Hagia Sophia", "Statue of Liberty", "Pyramids of Giza", "Mount Everest",
    # Ekstralar
    "Stonehenge", "Petra", "Niagara Falls", "Mount Fuji", 
    "Acropolis of Athens", "Burj Khalifa", "Angkor Wat", 
    "Sydney Opera House", "Louvre Museum", "Golden Gate Bridge",
    "Chichen Itza", "Alhambra", "Mount Kilimanjaro", "Big Ben", "Yellowstone National Park"
]

def fetch_and_save(entities, category):
    folder_path = f"data/{category}"
    os.makedirs(folder_path, exist_ok=True)

    for entity in entities:
        filename = f"{folder_path}/{entity.replace(' ', '_')}.txt"
        
        if os.path.exists(filename):
            print(f"Zaten mevcut, atlanıyor: {entity}")
            continue
            
        try:
            print(f"İndiriliyor: {entity}...")
            page = wikipedia.page(entity, auto_suggest=False)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(page.content)
            time.sleep(1) # IP engeli yememek için
        except Exception as e:
            print(f"Hata ({entity}): {e}")

print("--- Wikipedia'dan Veri Çekme Başlıyor ---")
fetch_and_save(people, "people")
fetch_and_save(places, "places")
print("--- Tüm Veriler Başarıyla İndirildi! ---")