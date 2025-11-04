
from datetime import datetime


def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip().split('|')

    paiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    suomalainenPaiva = paiva.strftime("%d.%m.%Y")
    aika = datetime.strptime(varaus[3], "%H:%M").time()
    suomalainenAika = aika.strftime("%H.%M")

    varausnumero = int(varaus[0])
    varaaja = str(varaus[1])
    tuntimaara = int(varaus[4])
    tuntihinta = float(varaus[5])
    kokonaishinta = tuntimaara * tuntihinta
    maksettu = varaus[6] == "True"
    kohde = str(varaus[7])
    puhelin = str(varaus[8])
    sahkoposti = str(varaus[9])

    varaustiedot = f"""
    Varausnumero: {varausnumero}
    Varaaja: {varaaja}
    Päivämäärä: {suomalainenPaiva}
    Aloitusaika: {suomalainenAika}
    Tuntimäärä: {tuntimaara}
    Tuntihinta: {tuntihinta} €
    Kokonaishinta: {kokonaishinta} €
    Maksettu: {"Kyllä" if maksettu else "Ei"}
    Kohde: {kohde}
    Puhelin: {puhelin}
    Sähköposti: {sahkoposti}
    """

    print(varaustiedot)

if __name__ == "__main__":
    main()