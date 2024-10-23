import requests
from bs4 import BeautifulSoup

# URL del sito da cui fare scraping
url = 'http://quotes.toscrape.com/'

# Effettua una richiesta GET
response = requests.get(url)

# Controlla che la richiesta abbia avuto successo
if response.status_code == 200:
    # Analizza il contenuto della pagina
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trova la prima citazione (la classe specifica 'text' contiene le citazioni)
    citazione = soup.find('span', class_='text').text
    
    # Trova il nome dell'autore (la classe specifica 'author' contiene i nomi)
    autore = soup.find('small', class_='author').text
    
    # Stampa la citazione trovata
    print(f"Citazione trovata: {citazione}")
    print(f"Autore: {autore}")
    
    # Scrivi la citazione e l'autore in un file
    with open("citazione.txt", "w") as f:
        f.write(f"Citazione trovata: {citazione}\n")
        f.write(f"Autore: {autore}\n")
        print("Citazione e autore salvati nel file.")  # Messaggio di conferma

else:
    print(f"Errore nella richiesta: {response.status_code}")
