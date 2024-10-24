import os
import re

import regex
import requests
from bs4 import BeautifulSoup

url = "******"

risposta = requests.get(url)

if risposta.status_code == 200:

    soup = BeautifulSoup(risposta.text, 'html.parser')
    header = ""
    try:
        header = soup.table.tr.find_all('th')
        # text_head = header[0].text
        reg_analisis_date = re.compile(r'\d\d/\d\d/\d\d\d\d')
        # reg_test = re.compile(r'[a-z]+')
        data_analisi = reg_analisis_date.findall(header[0].text)
        if data_analisi[0] == None:
            raise ValueError("data non trovata")

        print("data ricerca: " + data_analisi[0])
        # res_str = res.prettify()
        # print(text_head)
    except Exception as err:
        print(repr(err))


#    os.remove("output_test.txt")

    # with open("output_test.html", "w", encoding="utf-8") as outp:
    #     outp.write(header)
    #     print("Salvato nel file.")