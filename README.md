# Scheduled-Action-Test

Controllo programmato per verificare la disponibilità di specifici medici di base dell'ULSS (Veneto), con notifica tramite Bot Telegram

- Necessario sapere che medico si vuole controllare
- Recuperare il codice identificativo dei medici interessati
- Creare bot telegram e recuperare il token e il proprio chat_id
- Inserire nel secrets di github actions TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, MEDICOTEST
  - MEDICOTEST (nome da cambiare) inserire gli id dei medici separati da virgole ","
- Settare l'orario di schedulazione
- Eseguire

Esempio mex di output:
"Mario Rossi  26/10/2024  posti liberi: 0 di 60"


``` mermaid
graph TD

Cercare_medici --> Ottenere_Id --> MEDICOTEST
Creare_bot_telegram --> Ottenere_Token_Bot_Telegram --> TELEGRAM_TOKEN
Creare_bot_telegram --> Ottenere_ChatId_Personale --> TELEGRAM_CHAT_ID

MEDICOTEST --> Github_Action_SECRETS
TELEGRAM_TOKEN --> Github_Action_SECRETS
TELEGRAM_CHAT_ID --> Github_Action_SECRETS

Forkare_codice --> Github_Action_SECRETS
Forkare_codice --> Settare_Schedulazione

Settare_Schedulazione --> Esecuzione
Github_Action_SECRETS --> Esecuzione
```