import os
import re
import requests
from bs4 import BeautifulSoup


def check_errors(nome_medico, current_doct, data_analisi, numero_posti):
    if nome_medico == '':
        if current_doct == '':
            raise ValueError("medico non inserito")
        else:
            raise ValueError(f"'{current_doct}' medico non trovato")
    if len(data_analisi) == 0:
        raise ValueError(f"{nome_medico} data non trovata")
    if numero_posti == '':
        raise ValueError(f"{nome_medico} valori posti non trovati")


def scraping(site_url, doct_list):
    stringa_finale = ""

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

                check_errors(nome_medico, current_doct, data_analisi, numero_posti)

                giorno_lettura = data_analisi[0]

                stringa_medico = " ∙ " + nome_medico + "\t- " + giorno_lettura + "\t- Posti liberi: " + numero_posti + "\n\n"

                stringa_finale += stringa_medico


            except Exception as err:
                print(err)

    print(stringa_finale)
