import os
import re

import regex
import requests
from bs4 import BeautifulSoup

site_url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=dettaglio&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_dmcreg="

# Per splittare i dati presi da github repository secrets 'MEDICOTEST'
doct_list = os.environ['DOCTORS_LIST'].split(',')

# Stampa i codici medici per verifica
print("Codici medici:", doct_list)  # Stampa qui

# vecchio:
# doct_list = ["**", "***", "****"]

for current_doct in doct_list:

    url = site_url + current_doct

    risposta = requests.get(url)

    if risposta.status_code == 200:

        soup = BeautifulSoup(risposta.text, 'html.parser')

        try:

            body_tr = soup.table.tbody.find_all('tr')
            body_posti = body_tr[0].find_all('td')
            numero_posti = body_posti[1].text

            nome_medico = soup.find(id='tab01').strong.text

            reg_analysis_date = re.compile(r'\d\d/\d\d/\d\d\d\d')
            header = soup.table.tr.find_all('th')
            data_analisi = reg_analysis_date.findall(header[0].text)
            giorno_lettura = data_analisi[0]

            if data_analisi[0] == None:
                raise ValueError("data non trovata")

            stringa_finale = nome_medico + "\t\t\t- " + giorno_lettura + "\t\t\t- Posti liberi: " + numero_posti

            print(stringa_finale)


        except Exception as err:
            print(repr(err))

    #    os.remove("output_test.txt")

    # with open("output_test.html", "w", encoding="utf-8") as outp:
    #     outp.write(header)
    #     print("Salvato nel file.")
