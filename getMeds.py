import requests

url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=ricerca"

#inserire i dati
data = {
    "provinciaChangeEvent": "VE",  #inserire il codice della provincia: BL PD RO TV VE VI VR
    "comune": "VENEZIA",        # inserire nome del comune: Venezia
    # Aggiungi altri parametri specificati nel form
}

# Effettuo la richiesta
response = requests.post(url, data=data)


if response.status_code == 200:
    print(f"Risultato : \n")
    print(response.text)  # HTML della pagina con risultati
else:
    print("Errore:", response.status_code)
