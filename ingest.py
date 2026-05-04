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
            
        success = False
        retries = 3 # Hata alırsak 3 kere daha deneyeceğiz
        
        for attempt in range(retries):
            try:
                # İlk denemede auto_suggest=False, başarısız olursa True ile esneklik sağla
                suggest = False if attempt == 0 else True 
                
                print(f"İndiriliyor: {entity}" + (f" (Deneme {attempt + 1})" if attempt > 0 else "...") )
                page = wikipedia.page(entity, auto_suggest=suggest)
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(page.content)
                    
                time.sleep(1.5) # IP engeli yememek için süreyi çok az artırdık
                success = True
                break # Başarılı olduysa deneme döngüsünden çık
                
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"Çoklu anlam bulundu ({entity}). İlk seçenek indiriliyor: {e.options[0]}")
                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(page.content)
                    time.sleep(1.5)
                    success = True
                    break
                except Exception as inner_e:
                    print(f"Alt seçenek de indirilemedi ({entity}): {inner_e}")
                    break # Çoklu anlamda da hata verirse zorlama, diğer kelimeye geç
                    
            except wikipedia.exceptions.PageError:
                print(f"Hata ({entity}): Wikipedia'da böyle bir sayfa bulunamadı!")
                break # Sayfa gerçekten yoksa tekrar denemeye gerek yok
                
            except Exception as e:
                # API limitine takıldıysak veya JSON parse hatası aldıysak
                if attempt < retries - 1:
                    print(f"Uyarı ({entity}): API hatası alındı. 3 saniye beklenip tekrar denenecek...")
                    time.sleep(3) # Hata alınca API'yi rahatlatmak için daha uzun bekle
                else:
                    print(f"Bilinmeyen Hata ({entity}): {e}")
        
        if not success:
            print(f"!!! {entity} atlandı.")


print("--- Wikipedia'dan Veri Çekme Başlıyor ---")
fetch_and_save(people, "people")
fetch_and_save(places, "places")
print("--- Tüm Veriler Başarıyla İndirildi! ---")