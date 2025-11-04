
from datetime import datetime

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"


    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as file:
        for line in file:
            varaus = line.split("|")

            # Muutetaan tarvittavat tiedot oikeaan muotoon
            paiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
            suomalainenPaiva = paiva.strftime("%d.%m.%Y")
            aika = datetime.strptime(varaus[3], "%H:%M").time()
            suomalainenAika = aika.strftime("%H.%M")
            varausnumero = int(varaus[0])
            varaaja = str(varaus[1])
            tuntimaara = int(varaus[4])
            tuntihinta = round(float(varaus[5]), 2)
            kokonaishinta = round(tuntimaara * tuntihinta, 2)
            maksettu = varaus[6] == "True"
            kohde = str(varaus[7])
            puhelin = str(varaus[8])
            sahkoposti = str(varaus[9])
            loppumispaiva = suomalainenPaiva if aika.hour + tuntimaara < 24 else (paiva.replace(day=paiva.day + 1)).strftime("%d.%m.%Y")
            loppumisaika = f"{(aika.hour + tuntimaara) - 24}.{aika.minute:02d}" if aika.hour + tuntimaara >= 24 else f"{aika.hour + tuntimaara}.{aika.minute:02d}"

            # Muodostetaan varaustiedoista tulostettava merkkijono
            varaustiedot = f"""
            Varausnumero: {varausnumero}
            Varaaja: {varaaja}
            Päivämäärä: {suomalainenPaiva}
            Aloitusaika: {suomalainenAika}
            Loppumisaika: {loppumisaika}
            Loppumispäivä: {loppumispaiva}
            Tuntimäärä: {tuntimaara}
            Tuntihinta: {str(tuntihinta).replace('.', ',')} €
            Kokonaishinta: {str(kokonaishinta).replace('.', ',')} €
            Maksettu: {"Kyllä" if maksettu else "Ei"}
            Kohde: {kohde}
            Puhelin: {puhelin}
            Sähköposti: {sahkoposti}
            """

            # Tulostetaan varaustiedot
            print(varaustiedot)

        # Lasketaan ja tulostetaan kaikkien varausten yhteishinta
        yhteishinta = 0.0
        with open(varaukset, "r", encoding="utf-8") as file:
            for line in file:
                yhteishinta += round(int(line.split("|")[4]) * float(line.split("|")[5]), 2)

        print(f"Yhteishinta: {str(yhteishinta).replace('.', ',')} €")


if __name__ == "__main__":
    main()