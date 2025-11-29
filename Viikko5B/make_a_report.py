# Copyright 2025 Niko Hätälä
# License: MIT

from datetime import date, datetime
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
    print()

def write_new_report(weekly_data: str, report_file: str) -> None:
    """Adds weekly data to report file."""
    if Path(weekly_data + ".csv").is_file():
        weekly_data = weekly_data + ".csv"
        weekly_data = read_meter_data(weekly_data)
        try:
            with open(report_file, "x", encoding="utf-8") as file:
                daily_consumption_and_production(weekly_data, report_file)
        except FileExistsError:
            print("Raporttitiedosto on jo olemassa, kirjoitetaan päälle.")
            with open(report_file, "w", encoding="utf-8") as file:
                daily_consumption_and_production(weekly_data, report_file)
    else:                       
        print("Viikon datatiedostoa ei löydy.")    

def add_to_report(weekly_data: str, report_file: str) -> None:
    """Adds weekly data to report file.""" 

    try:
        with open(report_file, "x", encoding="utf-8") as file:
            daily_consumption_and_production(weekly_data, report_file)
    except FileExistsError:
        print("Raporttitiedosto on jo olemassa, kirjoitetaan päälle.")
        with open(report_file, "a", encoding="utf-8") as file:
            daily_consumption_and_production(weekly_data, report_file)

def erase_report(report_file: str) -> None:
    """Erases the report file if it exists."""
    if Path("Viikko5B/" + report_file).is_file():
        with open(report_file, "w", encoding="utf-8") as file:
            file.write("")
            print("Raporttitiedosto tyhjennetty.")
    else:
        print("Raporttitiedostoa ei löydy.")

def delete_report(report_file: str) -> None:
    """Deletes the report file if it exists."""
    if Path("Viikko5B/" + report_file).is_file():
        Path("Viikko5B/" + report_file).unlink()
        print("Raporttitiedosto poistettu.")
    else:
        print("Raporttitiedostoa ei löydy.")

def confirmation_prompt() -> bool:
    """Asks for user confirmation to proceed."""
    confirmation = input("Haluatko varmasti jatkaa? (k/e): ")
    if confirmation != "k":
        return False
    return True

def daily_consumption_and_production(meter_datafile: list, report_file: str) -> None:
    """Writes daily consumption and production data to file."""
    report_file.write("Luonti/muokkauspäivä: " + finnish_date(date.today()) + "\n")
    report_file.write("\n")
    report_file.write("Viikon" + "(" + Path(meter_datafile).name + ") sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
    report_file.write("\n")
    report_file.write("Päivä\t\tPvm\t\tKulutus [kWh]\t\t\tTuotanto [kWh]")
    report_file.write("\n")
    report_file.write("\t\t(pp.kk.vvvv)\tv1\tv2\tv3\t\tv1\tv2\tv3")
    report_file.write("\n")
    report_file.write("-----------------------------------------------------------------------------------")
    report_file.write("\n")        
    consumption_per_day = [0.0, 0.0, 0.0]
    production_per_day = [0.0, 0.0, 0.0]
    currentDate = meter_datafile[0][0].date()
    lastline = meter_datafile[-1]
    for line in meter_datafile:
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
        report_file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
    elif line[0].date() == currentDate:
        consumption_per_day[0] += consumption_per_hour(line)[0]
        consumption_per_day[1] += consumption_per_hour(line)[1]
        consumption_per_day[2] += consumption_per_hour(line)[2]
        production_per_day[0] += production_per_hour(line)[0]
        production_per_day[1] += production_per_hour(line)[1]
        production_per_day[2] += production_per_hour(line)[2]
    elif finnish_day == "Tiistai" or finnish_day == "Torstai":
        report_file.write(finnish_day + "\t\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
        currentDate = line[0].date() 
        consumption_per_day = [0.0, 0.0, 0.0]
        production_per_day = [0.0, 0.0, 0.0]
    else:
        report_file.write(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
        currentDate = line[0].date() 
        consumption_per_day = [0.0, 0.0, 0.0]
        production_per_day = [0.0, 0.0, 0.0]

def main() -> None:
    """Main function to execute the report generation."""

    main_menu()
    report_file_name = input("Syötä käsiteltävän raporttitiedoston nimi tai jätä tyhjäksi (oletus: yhteenveto.txt): ")
    if not report_file_name:
        report_file_name = "yhteenveto.txt"
    input_value = int(input("Valitse toiminto syöttämällä numero: "))
    print()
    while input_value != 0:
        if input_value == 9:
            print("Ohjelma lopetettu.")
            break
        elif input_value == 1:
            weekly_data = input("Anna lisättävän viikon tiedostonimi (muodossa viikkoXX): ")
            if Path("Viikko5B/" + weekly_data + ".csv").is_file():
                weekly_data = weekly_data + ".csv"
                weekly_data = read_meter_data(weekly_data)
                add_to_report(weekly_data)
                print("Viikon tiedot lisätty raporttiin.")
            else:
                print("Viikon datatiedostoa ei löydy.")
            input_value = 0
            main()
        elif input_value == 2:
            weekly_data = input("Anna lisättävän viikon tiedostonimi (muodossa viikkoXX): ")
            if confirmation_prompt() == False:
                print("Tyhjennys- ja lisäystoiminto peruutettu.")
                input_value = 0
                main()
            elif Path("Viikko5B/" + weekly_data + ".csv").is_file():
                weekly_data = weekly_data + ".csv"
                weekly_data = read_meter_data(weekly_data)
                erase_report(report_file_name)
                add_to_report(weekly_data)
                print("Viikon tiedot lisätty raporttiin.")
            else:
                print("Viikon datatiedostoa ei löydy.")
            write_new_report(weekly_data, report_file_name)
            input_value = 0
            main()
        elif input_value == 3:
            if confirmation_prompt() == False:
                print("Uuden raportin luonti peruutettu.")
                input_value = 0
                main()
            for week in range(1, 53):
                week_str = str(week).zfill(2)
                weekly_file = "Viikko5B/viikko" + week_str + ".csv"
                if Path(weekly_file).is_file():
                    add_to_report("Viikko5B/viikko" + week_str + ".csv", report_file_name)
                else:
                    continue
            print("Uusi raportti luotu kaikista viikoista (Tyhjät viikot ohitettu.")
            input_value = 0
            main()
        elif input_value == 4:
            if Path("Viikko5B/" + report_file_name).is_file():
                with open("Viikko5B/" + report_file_name, "r", encoding="utf-8") as file:
                    print(file.read())
            else:
                print("Raporttitiedostoa ei löydy.")
            input_value = 0
            main()
        elif input_value == 5:
            if confirmation_prompt() == False:
                print("Poistotoiminto peruutettu.")
                input_value = 0
                main()
            else:
                delete_report(report_file_name)
                input_value = 0
                main()
        
    if __name__ == "__main__":
        main()