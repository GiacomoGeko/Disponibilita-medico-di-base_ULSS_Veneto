import os

import getMeds
import scrape_doctor


def menu():
    print("---MENU---\n\n\t1. Ricercare medici\n\n\t2. Registra medico/i")
    res = input()
    return res

def startup_main():

    doct_list_string = ""
    res_menu = menu()

    if res_menu == '1':
        med_data = getMeds.inputMedData()
        # for medd in med_data:
        getMeds.ricerca_medico_data(med_data)


    elif res_menu == '2':
        print("Inserisci gli Id dei medici\nseparate da virgola, senza spazi\n-->  ")
        doct_list_string = input()

        if doct_list_string == "":
            doct_list_string = "006134,006777,008534"


    site_url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=dettaglio&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_dmcreg="

    #Se faccio girare su GITHUB:
    # doct_list_string = os.environ['DOCTORS_LIST']

    #Manual
    doct_list = doct_list_string.split(',')

    #Altro...

    #Avvio scraping:
    scrape_doctor.scraping(site_url, doct_list )

if __name__ == '__main__':

    startup_main()