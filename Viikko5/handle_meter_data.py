# Copyright 2025 Niko Hätälä
# License: MIT

from datetime import date, datetime
from typing import List, Dict
    
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

def daily_net_consumption(meter_data: list[float]) -> float:
    """Calculates the net consumption (consumption - production) for every phase per hour"""
    consumption_all_phases = 0.0
    production_all_phases = 0.0
    net_consumption = 0.0
    consumption_all_phases = meter_data[1] + meter_data[2] + meter_data[3]
    production_all_phases = meter_data[4] + meter_data[5] + meter_data[6]
    net_consumption = consumption_all_phases - production_all_phases
    return net_consumption

def main_menu():
    """Prints the main menu options."""
    print()
    print("Sähkönkulutuksen ja -tuotannon käsittelyohjelma")
    print("1 - Näytä päivittäinen sähkönkulutus ja -tuotanto vaiheittain")
    print("2 - Näytä päivittäinen nettokulutus (kulutus - tuotanto)")
    print("3 - Näytä yhteenveto viikon kulutuksesta ja tuotannosta vaiheittain")
    print("4 - Suorita kaikki edellä mainitut toiminnot")
    print("5 - Lopeta ohjelma")
    print()

def main() -> None:
    """Main function to handle meter data."""

    """main_menu()
    menu_option1 = False
    menu_option2 = False
    menu_option3 = False
    menu_option4 = False    
    input_value = input("Valitse jokin yllä olevista vaihtoehdoista painamalla vastaavaa numeroa: ")
    if input_value == "5":
        print("Ohjelma suljetaan.")
        main()
    elif input_value == "1":
        menu_option1 = True
    elif input_value == "2":
        menu_option2 = True
    elif input_value == "3":
        menu_option3 = True
    elif input_value == "4":
        menu_option4 = True
    else:
        print("Virheellinen valinta, yritä uudelleen.")
        main_menu()"""

    #if menu_option1 == True or menu_option4 == True:
        print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
        print()
        print("Päivä\t\tPvm\t\tKulutus [kWh]\t\t\tTuotanto [kWh]")
        print("\t\t(pp.kk.vvvv)\tv1\tv2\tv3\t\tv1\tv2\tv3")
        print("-----------------------------------------------------------------------------------")
        
        meter_data = read_meter_data("viikko42.csv")
        """Calculate total consumption and production per day and print the results."""
        consumption_per_day = [0.0, 0.0, 0.0]
        production_per_day = [0.0, 0.0, 0.0]
        currentDate = meter_data[0][0].date()
        lastline = meter_data[-1]
        for line in meter_data:
            """Iterate through meter data - calculate and print daily totals."""
            finnish_day = finnish_day_name(currentDate.strftime("%A"))
            date_str = currentDate.strftime("%d.%m.%Y")
            if line is lastline:
                consumption_per_day[0] += consumption_per_hour(line)[0]
                consumption_per_day[1] += consumption_per_hour(line)[1]
                consumption_per_day[2] += consumption_per_hour(line)[2]
                production_per_day[0] += production_per_hour(line)[0]
                production_per_day[1] += production_per_hour(line)[1]
                production_per_day[2] += production_per_hour(line)[2]
                print(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
            elif line[0].date() == currentDate:
                consumption_per_day[0] += consumption_per_hour(line)[0]
                consumption_per_day[1] += consumption_per_hour(line)[1]
                consumption_per_day[2] += consumption_per_hour(line)[2]
                production_per_day[0] += production_per_hour(line)[0]
                production_per_day[1] += production_per_hour(line)[1]
                production_per_day[2] += production_per_hour(line)[2]
            elif finnish_day == "Tiistai" or finnish_day == "Torstai":
                print(finnish_day + "\t\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
                currentDate = line[0].date() 
                consumption_per_day = [0.0, 0.0, 0.0]
                production_per_day = [0.0, 0.0, 0.0]
            else:
                print(finnish_day + "\t" + date_str + "\t" + str(round(consumption_per_day[0], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[1], 2)).replace('.', ',') + "\t" + str(round(consumption_per_day[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_day[0], 2)).replace('.', ',') + "\t" + str(round(production_per_day[1], 2)).replace('.', ',') + "\t" + str(round(production_per_day[2], 2)).replace('.', ','))
                currentDate = line[0].date() 
                consumption_per_day = [0.0, 0.0, 0.0]
                production_per_day = [0.0, 0.0, 0.0]

    #if menu_option2 is True or menu_option4 is True:
        print()        
        print("Päivittäinen nettokulutus (kulutus - tuotanto, kWh)")
        print("-----------------------------------------------------------------------------------")
        net_consumption = 0.0
        least_energy = daily_net_consumption(meter_data[0])
        currentDate = meter_data[0][0].date()
        lastline = meter_data[-1]
        best_day = finnish_day
        for line in meter_data:
            """Iterate through meter data - calculate net consumption, check best day and print net consumption."""
            finnish_day = finnish_day_name(currentDate.strftime("%A"))
            date_str = currentDate.strftime("%d.%m.%Y")
            if line is lastline and net_consumption < least_energy:
                net_consumption += daily_net_consumption(line)
                print(finnish_day + "\t" + date_str + "\t" + str(round(net_consumption, 2)).replace('.', ','))
                least_energy = net_consumption
                best_day = finnish_day
            elif line is lastline:
                net_consumption += daily_net_consumption(line)
                print(finnish_day + "\t" + date_str + "\t" + str(round(net_consumption, 2)).replace('.', ','))
            elif line[0].date() == currentDate:
                net_consumption += daily_net_consumption(line)
            elif finnish_day == "Tiistai" or finnish_day == "Torstai" and net_consumption < least_energy:
                print(finnish_day + "\t\t" + date_str + "\t" + str(round(net_consumption, 2)).replace('.', ','))
                least_energy = net_consumption
                best_day = finnish_day
                currentDate = line[0].date() 
                net_consumption = 0.0
            elif finnish_day == "Tiistai" or finnish_day == "Torstai":
                print(finnish_day + "\t\t" + date_str + "\t" + str(round(net_consumption, 2)).replace('.', ','))
                currentDate = line[0].date() 
                net_consumption = 0.0
            elif net_consumption < least_energy:
                print(finnish_day + "\t" + date_str + "\t" + str(round(net_consumption, 2)).replace('.', ','))
                least_energy = net_consumption
                best_day = finnish_day
                currentDate = line[0].date() 
                net_consumption = 0.0
            else:
                print(finnish_day + "\t" + date_str + "\t" + str(round(net_consumption, 2)).replace('.', ','))
                currentDate = line[0].date() 
                net_consumption = 0.0

        """Print the best day based on net consumption."""
        print()
        print("- Viikon paras päivä nettokulutuksen perusteella: " + best_day + " -")

    #if menu_option3 is True or menu_option4 is True:
        print()
        print("Yhteenveto viikon kulutuksesta ja tuotannosta vaiheittain")
        print("-----------------------------------------------------------------------------------")

        consumption_per_week = [0.0, 0.0, 0.0]
        production_per_week = [0.0, 0.0, 0.0]
        for line in meter_data:
            """Calculate total consumption and production for every phase for the week."""
            consumption_per_week[0] += consumption_per_hour(line)[0]
            consumption_per_week[1] += consumption_per_hour(line)[1]
            consumption_per_week[2] += consumption_per_hour(line)[2]
            production_per_week[0] += production_per_hour(line)[0]
            production_per_week[1] += production_per_hour(line)[1]
            production_per_week[2] += production_per_hour(line)[2]
        print("Vaihe\tKulutus [kWh]\tTuotanto [kWh]")
        print("1\t" + str(round(consumption_per_week[0], 2)).replace('.', ',') + "\t\t" + str(round(production_per_week[0], 2)).replace('.', ','))
        print("2\t" + str(round(consumption_per_week[1], 2)).replace('.', ',') + "\t\t" + str(round(production_per_week[1], 2)).replace('.', ','))
        print("3\t" + str(round(consumption_per_week[2], 2)).replace('.', ',') + "\t\t" + str(round(production_per_week[2], 2)).replace('.', ','))

if __name__ == "__main__":
    main()