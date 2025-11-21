"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 11 saraketta -> Lista -> Alkiot 0-10
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    muutettuvaraus = []
    # Ensimmäisen alkion = varaus[0] muunnos
    muutettuvaraus.append(int(varaus[0]))
    # Ja tästä jatkuu
    muutettuvaraus.append(str(varaus[1]))
    muutettuvaraus.append(str(varaus[2]))
    muutettuvaraus.append(str(varaus[3]))
    muutettuvaraus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettuvaraus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettuvaraus.append(int(varaus[6]))
    muutettuvaraus.append(float(varaus[7]))
    muutettuvaraus.append(varaus[8] == "True")
    muutettuvaraus.append(str(varaus[9]))
    muutettuvaraus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettuvaraus

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def main():
    
    varaukset = hae_varaukset("varaukset.txt")

    print("1) Vahvistetut varaukset")

    for varaus in varaukset[1:]:
        if varaus[8] == True:
            print(f"- {varaus[1]}, {varaus[9]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}")
        #print(" | ".join(str(x) for x in varaus))
        #tietotyypit = [type(x).__name__ for x in varaus]
        #print(" | ".join(tietotyypit))

    print("\n2) Pitkät varaukset (≥ 3 h)")

    for varaus in varaukset[1:]:
        if varaus[6] >= 3:
            print(f"- {varaus[1]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}, kesto {varaus[6]} h, {varaus[9]}")

    print("\n3) Varausten vahvistusstatus")

    for varaus in varaukset[1:]:
        if varaus[8] == True:
            print(f"{varaus[1]} -> Vahvistettu")
        else:
            print(f"{varaus[1]} -> Ei vahvistettu")

    print("\n4) Yhteenveto vahvistuksista")

    for varaus in varaukset[1:]:
        Vahvistettu = sum(1 for v in varaukset[1:] if v[8] == True)
        Ei_vahvistettu = sum(1 for v in varaukset[1:] if v[8] == False)
    print(f"- Vahvistettuja varauksia: {Vahvistettu} kpl")
    print(f"- Ei vahvistettuja varauksia: {Ei_vahvistettu} kpl")  

    print("\n5) Vahvistettujen varausten kokonaistulot")

    for varaus in varaukset[1:]:
        kokonaistulot = sum(v[7]*v[6] for v in varaukset[1:] if v[8] == True)
    print(f"Vahvistettujen varausten kokonaistulot: {kokonaistulot:.2f}".replace('.', ',') + " €")

if __name__ == "__main__":
    main()