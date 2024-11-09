import requests
from bs4 import BeautifulSoup
import re

url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=ricerca"


def estrai_luoghi(input):
    # prendo la stringa di testo che contiene tutti i medici filtrati
    match = re.search(r"<luoghi>(.*?)</luoghi>", input, re.DOTALL)
    return match.group(1) if match else None

#inserire i dati
data = {
    "provincia": "VE",  #inserire il codice della provincia: BL PD RO TV VE VI VR
    "comune": "VENEZIA",        # inserire nome del comune: Venezia

    # Aggiungi altri parametri specificati nel form
    "nome": "",
    "cognome": "",
    "indirizzoMedico": "",      # indirizzo del medico
    "tipologia": "",         # medico medicina generale o pediatra: MMG o PLS
    "indirizzo": "",            # indirizzo a cui si applica la distanza
    #"distanza": "1",             # <1km o 1<x<5 o >5km : 1 o 2 o 3
    #DISTANZA DA RIVEDERE perché non è questo il nome del parametro

}

# Effettuo la richiesta
response = requests.post(url, data=data)

if response.status_code == 200:
    output_html = BeautifulSoup(response.text, 'html.parser')

    # filtro con beautiful soup
    form_script = output_html.div.find(class_='form-container').decode_contents()
    stringa_luoghi = estrai_luoghi(form_script)
    luoghi = BeautifulSoup(stringa_luoghi, 'html.parser')
    result = [tag.get_text() for tag in luoghi.find_all("id")]

    with open("scriptoutput.html","w", encoding="utf-8") as o:
        print(result, file=o)

else:
    print("Errore:", response.status_code)
