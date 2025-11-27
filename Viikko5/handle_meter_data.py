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

def consumption_per_hour(meter_data: list) -> list:
    """Calculates consumption for every phase per hour, and returns a list of floats."""    
    consumption_p1 = meter_data[1]
    consumption_p2 = meter_data[2]
    consumption_p3 = meter_data[3]
    return [consumption_p1, consumption_p2, consumption_p3]

def production_per_hour(meter_data: list) -> list:
    """Calculates production for every phase per hour, and returns a list of floats."""
    production_p1 = meter_data[4]
    production_p2 = meter_data[5]
    production_p3 = meter_data[6]
    return [production_p1, production_p2, production_p3]

def main() -> None:
    """Main function to handle meter data."""
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
        finnish_day = finnish_day_name(currentDate.strftime("%A"))
        date_str = currentDate.strftime("%d.%m.%Y")
        if line is lastline:
            consumption_per_day[0] += consumption_per_hour(line)[0]
            consumption_per_day[1] += consumption_per_hour(line)[1]
            consumption_per_day[2] += consumption_per_hour(line)[2]
            production_per_day[0] += production_per_hour(line)[0]
            production_per_day[1] += production_per_hour(line)[1]
            production_per_day[2] += production_per_hour(line)[2]
            print(f"{finnish_day}\t{date_str}\t{consumption_per_day[0]:.2f}\t{consumption_per_day[1]:.2f}\t{consumption_per_day[2]:.2f}\t\t{production_per_day[0]:.2f}\t{production_per_day[1]:.2f}\t{production_per_day[2]:.2f}")
        elif line[0].date() == currentDate:
            consumption_per_day[0] += consumption_per_hour(line)[0]
            consumption_per_day[1] += consumption_per_hour(line)[1]
            consumption_per_day[2] += consumption_per_hour(line)[2]
            production_per_day[0] += production_per_hour(line)[0]
            production_per_day[1] += production_per_hour(line)[1]
            production_per_day[2] += production_per_hour(line)[2]
        elif finnish_day == "Tiistai" or finnish_day == "Torstai":
            print(f"{finnish_day}\t\t{date_str}\t{consumption_per_day[0]:.2f}\t{consumption_per_day[1]:.2f}\t{consumption_per_day[2]:.2f}\t\t{production_per_day[0]:.2f}\t{production_per_day[1]:.2f}\t{production_per_day[2]:.2f}")
            currentDate = line[0].date() 
            consumption_per_day = [0.0, 0.0, 0.0]
            production_per_day = [0.0, 0.0, 0.0]
        else:
            print(f"{finnish_day}\t{date_str}\t{consumption_per_day[0]:.2f}\t{consumption_per_day[1]:.2f}\t{consumption_per_day[2]:.2f}\t\t{production_per_day[0]:.2f}\t{production_per_day[1]:.2f}\t{production_per_day[2]:.2f}")
            currentDate = line[0].date() 
            consumption_per_day = [0.0, 0.0, 0.0]
            production_per_day = [0.0, 0.0, 0.0]
            

if __name__ == "__main__":
    main()