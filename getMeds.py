import requests
from bs4 import BeautifulSoup
import re

url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=ricerca"


def estrai_luoghi(input):
    match = re.search(r"<luoghi>(.*?)</luoghi>", input, re.DOTALL)
    return match.group(1) if match else None

#inserire i dati
data = {
    "provincia": "TV",  #inserire il codice della provincia: BL PD RO TV VE VI VR
    "comune": "ASOLO",        # inserire nome del comune: Venezia
    # Aggiungi altri parametri specificati nel form
}

# Effettuo la richiesta
response = requests.post(url, data=data)


if response.status_code == 200:
    print(f"Risultato : \n")
    print(response.text)  # HTML della pagina con risultati

    outputhtml = BeautifulSoup(response.text, 'html.parser')

    with open("outputFiltroComune.html","w", encoding="utf-8") as o:
        print(outputhtml, file=o)

    onlyscript = outputhtml.div.find(class_='form-container')

    jutext = onlyscript.decode_contents()

    solo_luoghi = estrai_luoghi(jutext)
    soupsoup =  BeautifulSoup(solo_luoghi, 'html.parser')

    # res = soupsoup.find_all("luogo")
    res = soupsoup.find_all("id")

    with open("scriptoutput.html","w", encoding="utf-8") as o:
        print(res, file=o)

else:
    print("Errore:", response.status_code)
