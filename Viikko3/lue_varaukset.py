"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def main():

    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varaukset, "r", encoding="utf-8") as f:
        for line in f:
            varaus = line.split("|")

            # Kutsutaan funktioita ja palautetaan arvot
            def hae_varausnumero(varaus):
                varausnumero = int(varaus[0])
                return varausnumero

            def hae_varaaja(varaus):
                varaaja = varaus[1]
                return varaaja

            def hae_paiva(varaus):
                paiva_str = varaus[2]
                paiva = datetime.strptime(paiva_str, "%Y-%m-%d")
                return paiva.strftime("%d.%m.%Y")

            def hae_aloitusaika(varaus):
                aloitusaika = varaus[3]
                return aloitusaika.replace(":", ".")
            
            def hae_tuntimaara(varaus):
                tuntimaara = int(varaus[4])
                return tuntimaara

            def hae_tuntihinta(varaus):
                tuntihinta = float(varaus[5])
                return f"{tuntihinta:.2f} €".replace(".", ",")

            def laske_kokonaishinta(varaus):
                tuntimaara = int(varaus[4])
                tuntihinta = float(varaus[5])
                kokonaishinta = tuntimaara * tuntihinta
                return f"{kokonaishinta:.2f} €".replace(".", ",")
                
            def hae_maksettu(varaus):
                maksettu_str = varaus[6]
                maksettu = maksettu_str.lower() == "true"
                return "Kyllä" if maksettu else "Ei"
            
            def hae_kohde(varaus):
                kohde = varaus[7]
                return kohde
            
            def hae_puhelin(varaus):
                puhelin = varaus[8]
                return puhelin
            
            def hae_sahkoposti(varaus):
                sahkoposti = varaus[9]
                return sahkoposti

            def tulosta_varaus(varaus):
                varaukset = f""" 
                Varausnumero: {hae_varausnumero(varaus)}
                Varaaja: {hae_varaaja(varaus)}
                Päivämäärä: {hae_paiva(varaus)}
                Aloitusaika: {hae_aloitusaika(varaus)}
                Tuntimäärä: {hae_tuntimaara(varaus)}
                Tuntihinta: {hae_tuntihinta(varaus)}
                Kokonaishinta: {laske_kokonaishinta(varaus)}
                Maksettu: {hae_maksettu(varaus)}
                Kohde: {hae_kohde(varaus)}
                Puhelin: {hae_puhelin(varaus)}
                Sähköposti: {hae_sahkoposti(varaus)}
                """
                return varaukset
    
            print(tulosta_varaus(varaus))

if __name__ == "__main__":
    main()