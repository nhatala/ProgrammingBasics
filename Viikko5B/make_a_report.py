# Copyright 2025 Niko Hätälä
# License: MIT

from datetime import date, datetime
import sys
from typing import List, Dict
from pathlib import Path

def edit_data_types(meter_data: list) -> list:
    """Edits the types of the meter data and changes power values from Wh to kWh."""
    meter_data_edited = []
    for meter_data in meter_data:
        date_time = datetime.strptime((meter_data[0]), "%Y-%m-%dT%H:%M:%S")
        phase1_consumption = float(meter_data[1]) / 1000
        phase2_consumption = float(meter_data[2]) / 1000
        phase3_consumption = float(meter_data[3]) / 1000
        production_phase1 = float(meter_data[4]) / 1000
        production_phase2 = float(meter_data[5]) / 1000
        production_phase3 = float(meter_data[6]) / 1000
        meter_data_edited.append([date_time, phase1_consumption, phase2_consumption, phase3_consumption, production_phase1, production_phase2, production_phase3])
    return meter_data_edited

def read_meter_data(meter_datafile: str) -> list:
    """Reads meter data, changes types and returns a new list with edited types."""
    meter_data = []
    with open(meter_datafile, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(";")
            if line[0] == "Aika":
                continue
            else:
                meter_data.append(line)
    meter_data = edit_data_types(meter_data)
    return meter_data

def finnish_day_name(english_day_name: str) -> str:
    """Converts English day names to Finnish."""
    days = {
        "Monday": "Maanantai",
        "Tuesday": "Tiistai",
        "Wednesday": "Keskiviikko",
        "Thursday": "Torstai",
        "Friday": "Perjantai",
        "Saturday": "Lauantai",
        "Sunday": "Sunnuntai"
    }
    return days.get(english_day_name, english_day_name)

def finnish_date(date_obj: date) -> str:
    """Formats date object to Finnish date format dd.mm.yyyy."""
    return date_obj.strftime("%d.%m.%Y")

def consumption_per_hour(meter_data: list[float]) -> list[float]:
    """Reads consumption for every phase per hour."""    
    consumption_p1 = meter_data[1]
    consumption_p2 = meter_data[2]
    consumption_p3 = meter_data[3]
    return [consumption_p1, consumption_p2, consumption_p3]

def production_per_hour(meter_data: list[float]) -> list[float]:
    """Reads production for every phase per hour."""
    production_p1 = meter_data[4]
    production_p2 = meter_data[5]
    production_p3 = meter_data[6]
    return [production_p1, production_p2, production_p3]

def main_menu():
    """Prints the main menu options."""
    print()
    print("----- Raportointiohjelma -----")
    print("*Valinnat tarkistavat olemassaolevan tiedoston ja luovat uuden tiedoston tarvittaessa*")
    print("------------------------------")
    print("1 - Lisää halutun viikon tiedot nykyiseen tiedostoon")
    print("2 - Tyhjennä ja lisää halutun viikon tiedot uuteen tiedostoon")
    print("3 - Luo uusi raportti kaikkien viikkojen tiedoista")
    print("4 - Näytä nykyisen raporttitiedoston tiedot")
    print("5 - Poista raporttitiedosto")
    print("9 - Lopeta ohjelma")

def erase_report(report_file: str) -> None:
    """Erases the report file if it exists."""
    if Path(report_file).is_file():
        with open(Path(report_file), "w", encoding="utf-8") as file:
            file.write("")
            print("\n**Raporttitiedosto tyhjennetty.**")
    else:
        print("\n**Raporttitiedostoa ei löydy.**")

def delete_report(report_file: str) -> None:
    """Deletes the report file if it exists."""
    if Path(report_file).is_file():
        Path(report_file).unlink()
        print("\n**Raporttitiedosto poistettu.**")
    else:
        print("\n**Raporttitiedostoa ei löydy.**")

def confirmation_prompt() -> bool:
    """Asks for user confirmation to proceed."""
    confirmation = input("\nHaluatko varmasti jatkaa? (k/e): ")
    if confirmation != "k":
        return False
    return True

def write_new_report(weekly_data: str, report_file: str) -> None:
    """Adds weekly data to report file."""
    weekly_data = read_meter_data(weekly_data)
    try:
        with open(Path(report_file), "x", encoding="utf-8") as file:
            file.write("Raportin luonti-/muokkauspäivä: " + finnish_date(date.today()) + "\n")
            file.write("\n")
            file.write("Viikon sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
            file.write("Päivä\t\tPvm\t\t\tKulutus [kWh]\t\t\tTuotanto [kWh]")
            file.write("\n")
            file.write("\t\t\t(pp.kk.vvvv)\tv1\tv2\tv3\t\tv1\tv2\tv3")
            file.write("\n")
            file.write("-----------------------------------------------------------------------------------")
            file.write("\n")        
            consumption_per_day = [0.0, 0.0, 0.0]
            production_per_day = [0.0, 0.0, 0.0]
            currentDate = weekly_data[0][0].date()
            lastline = weekly_data[-1]
            for line in weekly_data:
                """Iterate through meter data - calculate and write daily totals on report."""
                finnish_day = finnish_day_name(currentDate.strftime("%A"))
                date_str = currentDate.strftime("%d.%m.%Y")
                if line is lastline:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                    file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
                elif line[0].date() == currentDate:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                elif finnish_day == "Tiistai" or finnish_day == "Torstai":
                    file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
                    currentDate = line[0].date() 
                    consumption_per_day = [0.0, 0.0, 0.0]
                    production_per_day = [0.0, 0.0, 0.0]
                else:
                    file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
                    production_per_day = [0.0, 0.0, 0.0]
    except FileExistsError:
        print("\n**Raporttitiedosto on jo olemassa, kirjoitetaan päälle.**")
        with open(Path(report_file), "w", encoding="utf-8") as file:
            file.write("Raportin luonti-/muokkauspäivä: " + finnish_date(date.today()) + "\n")
            file.write("\n")
            file.write("Viikon sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
            file.write("Päivä\t\tPvm\t\t\t\tKulutus [kWh]\t\t\tTuotanto [kWh]")
            file.write("\n")
            file.write("\t\t\t(pp.kk.vvvv)\tv1\t\tv2\t\tv3\t\tv1\tv2\tv3")
            file.write("\n")
            file.write("-----------------------------------------------------------------------------------")
            file.write("\n")        
            consumption_per_day = [0.0, 0.0, 0.0]
            production_per_day = [0.0, 0.0, 0.0]
            currentDate = weekly_data[0][0].date()
            lastline = weekly_data[-1]
            for line in weekly_data:
                """Iterate through meter data - calculate and write daily totals on report."""
                finnish_day = finnish_day_name(currentDate.strftime("%A"))
                date_str = currentDate.strftime("%d.%m.%Y")
                if line is lastline:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                    file.write(finnish_day + "\t" + date_str + "\t\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                elif line[0].date() == currentDate:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                elif finnish_day == "Tiistai" or finnish_day == "Torstai":
                    file.write(finnish_day + "\t\t" + date_str + "\t\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                    currentDate = line[0].date() 
                    consumption_per_day = [0.0, 0.0, 0.0]
                    production_per_day = [0.0, 0.0, 0.0]
                else:
                    file.write(finnish_day + "\t" + date_str + "\t\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                    currentDate = line[0].date() 
                    consumption_per_day = [0.0, 0.0, 0.0]
                    production_per_day = [0.0, 0.0, 0.0]

def add_to_report(weekly_data: str, report_file: str) -> None:
    """Writes daily consumption and production data to file."""
    weekly_data = read_meter_data(weekly_data)
    try:
        with open(Path(report_file), "x", encoding="utf-8") as file:
            file.write("Luonti/muokkauspäivä: " + finnish_date(date.today()))
            file.write("\n")
            file.write("Viikon sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
            file.write("\n")
            file.write("Päivä\t\tPvm\t\t\tKulutus [kWh]\t\t\tTuotanto [kWh]")
            file.write("\n")
            file.write("\t\t\t(pp.kk.vvvv)\tv1\tv2\tv3\t\tv1\tv2\tv3")
            file.write("\n")
            file.write("-----------------------------------------------------------------------------------")
            file.write("\n")        
            consumption_per_day = [0.0, 0.0, 0.0]
            production_per_day = [0.0, 0.0, 0.0]
            currentDate = weekly_data[0][0].date()
            lastline = weekly_data[-1]
            for line in weekly_data:
                """Iterate through meter data - calculate and write daily totals on report."""
                finnish_day = finnish_day_name(currentDate.strftime("%A"))
                date_str = currentDate.strftime("%d.%m.%Y")
                if line is lastline:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                    file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                elif line[0].date() == currentDate:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                elif finnish_day == "Tiistai" or finnish_day == "Torstai":
                    file.write(finnish_day + "\t\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                    currentDate = line[0].date() 
                    consumption_per_day = [0.0, 0.0, 0.0]
                    production_per_day = [0.0, 0.0, 0.0]
                else:
                    file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                    currentDate = line[0].date() 
                    consumption_per_day = [0.0, 0.0, 0.0]
                    production_per_day = [0.0, 0.0, 0.0]
    except FileExistsError:
        print("\n**Raporttitiedosto on jo olemassa, lisätään tiedot.**")
        with open(Path(report_file), "a", encoding="utf-8") as file:
            file.write("Luonti/muokkauspäivä: " + finnish_date(date.today()) + "\n")
            file.write("\n")
            file.write("Viikon sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
            file.write("\n")
            file.write("Päivä\t\tPvm\t\t\tKulutus [kWh]\t\t\tTuotanto [kWh]")
            file.write("\n")
            file.write("\t\t\t(pp.kk.vvvv)\tv1\tv2\tv3\t\tv1\tv2\tv3")
            file.write("\n")
            file.write("-----------------------------------------------------------------------------------")
            file.write("\n")        
            consumption_per_day = [0.0, 0.0, 0.0]
            production_per_day = [0.0, 0.0, 0.0]
            currentDate = weekly_data[0][0].date()
            lastline = weekly_data[-1]
            for line in weekly_data:
                """Iterate through meter data - calculate and write daily totals on report."""
                finnish_day = finnish_day_name(currentDate.strftime("%A"))
                date_str = currentDate.strftime("%d.%m.%Y")
                if line is lastline:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                    file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                elif line[0].date() == currentDate:
                    consumption_per_day[0] += consumption_per_hour(line)[0]
                    consumption_per_day[1] += consumption_per_hour(line)[1]
                    consumption_per_day[2] += consumption_per_hour(line)[2]
                    production_per_day[0] += production_per_hour(line)[0]
                    production_per_day[1] += production_per_hour(line)[1]
                    production_per_day[2] += production_per_hour(line)[2]
                elif finnish_day == "Tiistai" or finnish_day == "Torstai":
                    file.write(finnish_day + "\t\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                    currentDate = line[0].date() 
                    consumption_per_day = [0.0, 0.0, 0.0]
                    production_per_day = [0.0, 0.0, 0.0]
                else:
                    file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ',') + "\n")
                    currentDate = line[0].date() 
                    consumption_per_day = [0.0, 0.0, 0.0]
                    production_per_day = [0.0, 0.0, 0.0]

def main():
    """Main function to execute the report generation."""

    main_menu()
    report_file_name = input("\nSyötä käsiteltävän raporttitiedoston nimi tai jätä tyhjäksi (oletus: yhteenveto.txt) - lopeta syöttämällä 9: ")
    if report_file_name == "9":
        print("\n**Ohjelma lopetettu.**\n")
        sys.exit()
    elif report_file_name.endswith(".txt") == False and report_file_name != "":
        print("\n**Raporttitiedoston nimen tulee päättyä .txt**\n")
        main()
    else:
        if not report_file_name:
            report_file_name = "yhteenveto.txt"
    input_value = input("\nValitse toiminto syöttämällä numero: ")
    if input_value in ["1", "2", "3", "4", "5", "9"]:
        input_value = int(input_value)
        while input_value != 0:
            if input_value == 9:
                print("\n**Ohjelma lopetettu.**\n")
                input_value = 0
                sys.exit()
            elif input_value == 1:
                weekly_data = input("\nAnna lisättävän viikon tiedostonimi (muodossa viikkoXX) - lopeta syöttämällä 9: ")
                if weekly_data == "9":
                    print("\n**Toiminto peruutettu.**\n")
                    input_value = 0
                    sys.exit()
                elif Path(weekly_data + ".csv").is_file():
                    weekly_data = weekly_data + ".csv"
                    add_to_report(weekly_data, report_file_name)
                    print("\n**Viikon tiedot lisätty raporttiin.**\n")
                else:
                    print("\n**Viikon datatiedostoa ei löydy.**")
                input_value = 0
                sys.exit()
            elif input_value == 2:
                weekly_data = input("\nAnna halutun viikon tiedostonimi (muodossa viikkoXX) - lopeta syöttämällä 9: ")
                if weekly_data == "9": 
                    print("\n**Toiminto peruutettu.**\n")
                    input_value = 0
                    sys.exit()
                elif confirmation_prompt() == False:
                    print("\n**Toiminto peruutettu.**\n")
                    input_value = 0
                    sys.exit()
                elif Path(weekly_data + ".csv").is_file():
                    weekly_data = weekly_data + ".csv"
                    write_new_report(weekly_data, report_file_name)
                    print("\n**Viikon tiedot lisätty raporttiin.**\n")
                else:
                    print("\n**Viikon datatiedostoa ei löydy.**\n")
                input_value = 0
                sys.exit()
            elif input_value == 3:
                if confirmation_prompt() == False:
                    print("\n**Uuden raportin luonti peruutettu.**\n")
                    input_value = 0
                    sys.exit()
                else:
                    erase_report(report_file_name)
                    for week in range(1, 53):
                        week_str = str(week).zfill(2)
                        weekly_file = "viikko" + week_str + ".csv"
                        if Path(weekly_file).is_file():
                            add_to_report("viikko" + week_str + ".csv", report_file_name)
                        else:
                            pass
                print("\n**Uusi raportti luotu kaikista viikoista (Tyhjät viikot ohitettu).**\n")
                input_value = 0
                sys.exit()
            elif input_value == 4:
                if Path(report_file_name).is_file():
                    with open(Path(report_file_name), "r", encoding="utf-8") as file:
                        print(file.read())
                else:
                    print("\n**Raporttitiedostoa ei löydy.**\n")
                input_value = 0
                sys.exit()
            elif input_value == 5:
                if confirmation_prompt() == False:
                    print("\n**Poistotoiminto peruutettu.**\n")
                    input_value = 0
                    sys.exit()
                else:
                    delete_report(report_file_name)
                    input_value = 0
                    sys.exit()
    else:
        print("\n**Virheellinen valinta, yritä uudelleen.**\n")
        input_value = 0
        sys.exit()

if __name__ == "__main__":
    main()