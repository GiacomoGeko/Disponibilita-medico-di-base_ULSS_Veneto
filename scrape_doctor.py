import os
import re

import regex
import requests
from bs4 import BeautifulSoup

site_url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=dettaglio&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_dmcreg="


risposta = requests.get(url)

if risposta.status_code == 200:

    soup = BeautifulSoup(risposta.text, 'html.parser')
    header = ""
    try:
        header = soup.table.tr.find_all('th')
        # text_head = header[0].text
        body_tr = soup.table.tbody.find_all('tr')

        body_posti = body_tr[0].find_all('td')

        doct_name = soup.find(id='tab01').strong.text
        reg_analysis_date = re.compile(r'\d\d/\d\d/\d\d\d\d')
        # reg_test = re.compile(r'[a-z]+')
        data_analisi = reg_analysis_date.findall(header[0].text)
        if data_analisi[0] == None:
            raise ValueError("data non trovata")

        finale = doct_name + " - " + data_analisi[0] + " - Posti liberi: " + body_posti[1].text

        print(finale)

        # print("data ricerca: " + data_analisi[0])
        # res_str = res.prettify()
        # print(text_head)
    except Exception as err:
        print(repr(err))


#    os.remove("output_test.txt")

    # with open("output_test.html", "w", encoding="utf-8") as outp:
    #     outp.write(header)
    #     print("Salvato nel file.")