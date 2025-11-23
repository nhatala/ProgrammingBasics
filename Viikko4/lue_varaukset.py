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
from importlib.metadata import requires

def muunna_varaustiedot(varaus: list) -> list:
    """Muuntaa varauksen tiedot oikeisiin tietotyyppeihin."""
    muutettuvaraus = []
    muutettuvaraus.append(int(varaus[0]))
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
    """Hakee varaukset tiedostosta ja muuntaa ne oikeisiin tietotyyppeihin."""
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
    """Tulostaa vahvistetut varaukset."""
    for varaus in varaukset[1:]:
        if varaus[8] == True:
            print(f"- {varaus[1]}, {varaus[9]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}")

    print("\n2) Pitkät varaukset (≥ 3 h)")
    """Tulostaa pitkät varaukset (kesto vähintään 3 tuntia)."""
    for varaus in varaukset[1:]:
        if varaus[6] >= 3:
            print(f"- {varaus[1]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}, kesto {varaus[6]} h, {varaus[9]}")

    print("\n3) Varausten vahvistusstatus")
    """Tulostaa varausten vahvistusstatuksen."""
    for varaus in varaukset[1:]:
        if varaus[8] == True:
            print(f"{varaus[1]} -> Vahvistettu")
        else:
            print(f"{varaus[1]} -> Ei vahvistettu")

    print("\n4) Yhteenveto vahvistuksista")
    """Tulostaa yhteenvedon varausten vahvistusstatuksesta."""
    for varaus in varaukset[1:]:
        Vahvistettu = sum(1 for v in varaukset[1:] if v[8] == True)
        Ei_vahvistettu = sum(1 for v in varaukset[1:] if v[8] == False)
    print(f"- Vahvistettuja varauksia: {Vahvistettu} kpl")
    print(f"- Ei vahvistettuja varauksia: {Ei_vahvistettu} kpl")  

    print("\n5) Vahvistettujen varausten kokonaistulot")
    """Laskee vahvistettujen varausten kokonaistulot."""
    for varaus in varaukset[1:]:
        kokonaistulot = sum(v[7]*v[6] for v in varaukset[1:] if v[8] == True)
    print(f"Vahvistettujen varausten kokonaistulot: {kokonaistulot:.2f}".replace('.', ',') + " €")

    print("\nKallein varaus:")
    """Etsii ja tulostaa kalleimman vahvistetun varauksen tiedot."""
    def kokonaishinta(varauksenKesto, hinta):
            """Laskee varauksen kokonaishinnan."""
            kokonaishinta = varauksenKesto * hinta
            return kokonaishinta
    
    def kallein_varaus(varaukset):
        kallein = None
        korkein_hinta = 0
        for varaus in varaukset:
            if varaus[8] == True:
                yhteishinta = kokonaishinta(varaus[6], varaus[7])
                if yhteishinta > korkein_hinta:
                    korkein_hinta = yhteishinta
                    kallein = varaus
        return kallein

    kalleinvaraus = kallein_varaus(varaukset[1:])
    print(f"- Nimi: {kalleinvaraus[1]}")
    print(f"- Varattu tila: {kalleinvaraus[9]}")
    print(f"- Päivä: {kalleinvaraus[4].strftime('%d.%m.%Y')}")
    print(f"- Kellonaika: {kalleinvaraus[5].strftime('%H.%M')}")
    print(f"- Kesto: {kalleinvaraus[6]} h")
    print(f"- Kokonaishinta: {kokonaishinta(kalleinvaraus[6], kalleinvaraus[7]):.2f} €".replace('.', ','))   
          
    print("\nVarausten määrä päivittäin:")
    """Laskee varausten määrän päivittäin."""
    for varaus in varaukset[1:]:
        """Laskee varausten määrän päivittäin."""
        paivittain = {}
        for varaus in varaukset[1:]:
            pvm = varaus[4].strftime('%d.%m.%Y')
            if pvm in paivittain:
                paivittain[pvm] += 1
            else:
                paivittain[pvm] = 1
    for pvm, maara in paivittain.items():
        print(f"- {pvm}: {maara} kpl")

    def tilahaku(haetut_tilat):
        """Hakee varaukset käyttäjän syötteen perusteella"""
        for varaus in varaukset[1:]:
            if varaus[9] == haettu_tila:
                haetut_varaukset.append(varaus)
        return(haetut_varaukset)
    haetut_varaukset = []
    haettu_tila = input("\nAnna tilan nimi: ")
    tilahaku(haettu_tila)
    if len(haetut_varaukset) == 0:
        print("Tiloja ei löytynyt. Tarkista, että kirjoitit tilan nimen oikein.")
    else:
        print(f"Varaukset tilaan '{haettu_tila}':")
        for varaus in haetut_varaukset:
            print(f"- {varaus[1]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}, kesto {varaus[6]} h")

    def hae_tulevat(tulevat):
        """Hakee tulevat varaukset käyttäjän antamasta päivämäärästä eteenpäin"""
        for varaus in varaukset[1:]:
            if varaus[4] > tulevienpvm:
                tulevat_varaukset.append(varaus)
        return tulevat_varaukset
    
    tulevat_varaukset = []
    tulevienpvm = input("\nAnna päivämäärä (pp.kk.vvvv): ")
    tarkista_muoto = tulevienpvm.split('.')
    if len(tarkista_muoto) != 3:
        input_format_invalid = True
        print("Virheellinen päivämäärän muoto. Käytä muotoa pp.kk.vvvv")
        return
    tulevienpvm = datetime.strptime(tulevienpvm, '%d.%m.%Y').date()
    hae_tulevat(tulevienpvm)
    if len(tulevat_varaukset) == 0:
        print("Varauksia ei löytynyt. Tarkistathan, että kirjoitit päivämäärän oikeassa muodossa.")
    else:
        for varaus in tulevat_varaukset:
            print(f"- {varaus[1]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}, {varaus[9]}")

    vahvistetutVaraukset = []
    for varaus in varaukset[1:]:
        """Tarkistaa ja tallentaa vahvistetut varaukset erilliseen listaan."""
        if varaus[8] == True:
            vahvistetutVaraukset.append(varaus)
    varaustenKeskimKesto = sum(v[6] for v in vahvistetutVaraukset) / len(vahvistetutVaraukset)
    print(f"\nVahvistettujen varausten keskimääräinen kesto: {varaustenKeskimKesto:.2f}".replace('.', ',') + " h")


if __name__ == "__main__":
    main()