# Disponibilità medico di base ULSS - Veneto

Controllo schedulato per verificare la disponibilità di specifici medici di base dell'ULSS (Veneto), con esecuzione tramite Github Actions e notifica tramite Bot Telegram

- Necessario sapere che medico si vuole controllare
- Recuperare il codice identificativo dei medici interessati
- Creare bot telegram e recuperare il token e il proprio chat_id
- Inserire nel secrets di github actions TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, MEDICOLIST
  - MEDICOLIST inserire gli id dei medici separati da virgole "," e senza spazi
- Settare l'orario di schedulazione
- Eseguire

Esempio mex di output:
"Mario Rossi  26/10/2024  posti liberi: 0 di 60"

Pagina dell'ULSS: 
https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri

``` mermaid
graph TD

Cercare_medici --> Ottenere_Id --> MEDICOLIST
Creare_bot_telegram --> Ottenere_Token_Bot_Telegram --> TELEGRAM_TOKEN
Creare_bot_telegram --> Ottenere_ChatId_Personale --> TELEGRAM_CHAT_ID

MEDICOLIST --> Github_Action_SECRETS
TELEGRAM_TOKEN --> Github_Action_SECRETS
TELEGRAM_CHAT_ID --> Github_Action_SECRETS

Github_Action_SECRETS --> Esecuzione
Settare_Schedulazione ---> Esecuzione
```

### Come ottenere il codice identificativo di un medico
- Aprire la pagina del medico dopo averlo [ricercato](https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri)
- Scorrere in basso fino alla fine della pagina in basso
- Fare ispeziona elemento del pulsante "STAMPA ORARIO" 
  - `Ctrl + Maiusc + C` e click sul pulsante "STAMPA ORARIO"
- Della riga selezionata `<a ...>` prendere `href="/delegate/StampaOrario?param=123456"`
  - Estrarre le 6 cifre poste alla fine di href, dopo "param="
  - Es: codice identificativo medico = "123456"
