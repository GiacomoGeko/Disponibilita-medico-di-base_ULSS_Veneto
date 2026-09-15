import requests
from bs4 import BeautifulSoup
import re
import folium

url = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=2&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=ricerca"

def inputMedData():
    data = {
        "provincia": "",
        "comune": "",
        "nome": "",
        "cognome": "",
        "indirizzoMedico": "",
        "tipologia": "",
        "indirizzo": "",
        "distanza": ""
    }

    # Campi obbligatori
    while not data["provincia"]:
        data["provincia"] = input("Inserisci il codice provincia (BL, PD, RO, TV, VE, VI, VR): ").strip().upper()
        if not data["provincia"]:
            print("⚠️  Il campo 'provincia' è obbligatorio.")

    while not data["comune"]:
        data["comune"] = input("Inserisci il nome del comune (es. Venezia): ").strip()
        if not data["comune"]:
            print("⚠️  Il campo 'comune' è obbligatorio.")

    # Campi facoltativi
    data["nome"] = input("Nome: ").strip()
    data["cognome"] = input("Cognome: ").strip()
    data["indirizzoMedico"] = input("Indirizzo del medico: ").strip()
    data["tipologia"] = input("Tipologia (MMG o PLS): ").strip().upper()
    data["indirizzo"] = input("Indirizzo (lascia vuoto se non applicabile): ").strip()

    # Se l'indirizzo è stato inserito, chiedi la distanza
    if data["indirizzo"]:
        while True:
            distanza = input("Distanza (1 = <1km, 2 = 1<x<5km, 3 = >5km): ").strip()
            if distanza in ("1", "2", "3"):
                data["distanza"] = distanza
                break
            else:
                print("⚠️  Inserisci un valore valido: 1, 2 o 3.")
    else:
        data["distanza"] = ""

    return data

def estrai_luoghi(input):
    # prendo la stringa di testo che contiene tutti i medici filtrati
    match = re.search(r"<luoghi>(.*?)</luoghi>", input, re.DOTALL)
    return match.group(1) if match else None


#inserire i dati
data = {
    "provincia": "VE",  #inserire il codice della provincia: BL PD RO TV VE VI VR
    "comune": "VENEZIA",  # inserire nome del comune: Venezia

    # Aggiungi altri parametri specificati nel form
    "nome": "",
    "cognome": "",
    "indirizzoMedico": "",  # indirizzo del medico
    "tipologia": "",  # medico medicina generale o pediatra: MMG o PLS
    "indirizzo": "",  # indirizzo a cui si applica la distanza
    "distanza": "1",  # <1km o 1<x<5 o >5km : 1 o 2 o 3

}

if data["indirizzo"] == "":
    data["distanza"] = ""  #Se non esiste un indirizzo specificato annullo anche il valore distanza dall'indirizzo


def ricerca_medico_data(data):
    # Effettuo la richiesta
    response = requests.post(url, data=data)

    if response.status_code == 200:
        output_html = BeautifulSoup(response.text, 'html.parser')

        # Filtro con BeautifulSoup
        form_script = output_html.div.find(class_='form-container').decode_contents()
        stringa_luoghi = estrai_luoghi(form_script)

        if stringa_luoghi is not None:

            # Parsing dei luoghi
            luoghi = BeautifulSoup(stringa_luoghi, 'html.parser')

            # Mantengo il tuo result con gli ID
            result = [tag.get_text(strip=True) for tag in luoghi.find_all("id")]

            result_name = [
                f'{luogo.find("id").get_text(strip=True)} - {luogo.find("titolo").get_text(strip=True)} <br/>'
                for luogo in luoghi.find_all("luogo")
            ]

            # ==========================================
            # CREAZIONE MAPPA
            # ==========================================

            import folium
            from folium.plugins import MarkerCluster

            medici = []

            for luogo in luoghi.find_all("luogo"):
                id_medico = luogo.find("id").get_text(strip=True)
                nome = luogo.find("titolo").get_text(strip=True)
                descrizione = luogo.find("descrizione").get_text(" ", strip=True)

                lat = float(luogo.find("lat").get_text(strip=True))
                lng = float(luogo.find("lng").get_text(strip=True))

                medici.append({
                    "id": id_medico,
                    "nome": nome,
                    "descrizione": descrizione,
                    "lat": lat,
                    "lng": lng
                })

            # Calcolo il centro della mappa
            lat_centro = sum(medico["lat"] for medico in medici) / len(medici)
            lng_centro = sum(medico["lng"] for medico in medici) / len(medici)

            # Creo la mappa OpenStreetMap
            mappa = folium.Map(
                location=[lat_centro, lng_centro],
                zoom_start=13,
                tiles="CartoDB Voyager"
            )

            # Raggruppamento dei marker vicini
            marker_cluster = MarkerCluster().add_to(mappa)

            # Aggiungo i medici alla mappa
            for medico in medici:
                popup_html = f"""
                <div style="min-width: 200px;">
                    <b>{medico["id"]}</b><br>
                    <strong>{medico["nome"]}</strong><br><br>
                    {medico["descrizione"]}
                </div>
                """

                folium.Marker(
                    location=[medico["lat"], medico["lng"]],
                    popup=folium.Popup(popup_html, max_width=350),
                    tooltip=f'{medico["id"]} - {medico["nome"]}'
                ).add_to(marker_cluster)

            # Salvo la mappa
            mappa.save("mappa_medici.html")

            # ==========================================
            # OUTPUT
            # ==========================================

            with open("scriptoutput.html", "w", encoding="utf-8") as o:
                print(result_name, file=o)
                print(len(result_name), file=o)
                print("\nMappa salvata in: mappa_medici.html", file=o)

            print("\nID Medici trovati:\n")
            print(result)
            print(len(result))
            print("\nMappa salvata in: mappa_medici.html")

        else:
            with open("scriptoutput.html", "w", encoding="utf-8") as o:
                print("nessun medico", file=o)

            print("nessun medico")

    else:
        print("Errore:", response.status_code)
