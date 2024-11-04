import os
import re
import requests
from bs4 import BeautifulSoup

site_url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=dettaglio&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_dmcreg="

# Per splittare i dati presi da github repository secrets 'MEDICOLIST'
doct_list_string = os.environ['DOCTORS_LIST']
doct_list = doct_list_string.split(',')

def check_errors():
    if nome_medico == '':
        if current_doct == '':
            raise ValueError("medico non inserito")
        else:
            raise ValueError(f"'{current_doct}' medico non trovato")
    if len(data_analisi) == 0:
        raise ValueError(f"{nome_medico} data non trovata")
    if numero_posti == '':
        raise ValueError(f"{nome_medico} valori posti non trovati")

stringa_finale= ""

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

            check_errors()

            giorno_lettura = data_analisi[0]

            stringa_medico = " ∙ " + nome_medico + "\t- " + giorno_lettura + "\t- Posti liberi: " + numero_posti + "\n\n"

            stringa_finale += stringa_medico


        except Exception as err:
            print(err)

print(stringa_finale)
