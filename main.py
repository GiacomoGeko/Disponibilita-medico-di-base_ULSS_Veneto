import os
import scrape_doctor

if __name__ == '__main__':


    site_url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=dettaglio&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_dmcreg="

    #Se faccio girare su GITHUB:
    # doct_list_string = os.environ['DOCTORS_LIST']

    #Manual
    doct_list_string = "006134,006777,008534"
    doct_list = doct_list_string.split(',')

    #Altro...

    #Avvio scraping:
    scrape_doctor.scraping(site_url, doct_list )