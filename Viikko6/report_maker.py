# Copyright 2025 Niko Hätälä
# License: MIT

from datetime import date, datetime, time, timezone
import sys
from typing import List, Dict
from pathlib import Path

def edit_data_types(meter_data: list) -> list:
    """Edits the types of the meter data"""
    meter_data_edited = []
    for data in meter_data:
        date_time = datetime.fromisoformat(data[0])
        consumption = float(data[1])
        production = float(data[2])
        average_temperature = float(data[3])
        meter_data_edited.append([date_time, consumption, production, average_temperature])
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

def finnish_month_name(english_month_name: str) -> str:
    """Converts English month names to Finnish."""
    months = {
        "January": "Tammikuu",
        "February": "Helmikuu",
        "March": "Maaliskuu",
        "April": "Huhtikuu",
        "May": "Toukokuu",
        "June": "Kesäkuu",
        "July": "Heinäkuu",
        "August": "Elokuu",
        "September": "Syyskuu",
        "October": "Lokakuu",
        "November": "Marraskuu",
        "December": "Joulukuu"
    }
    return months.get(english_month_name, english_month_name)

def finnish_date(date_obj: date) -> str:
    """Formats date object to Finnish date format dd.mm.yyyy."""
    return date_obj.strftime("%d.%m.%Y")

def main_menu():
    """Prints the main menu options."""
    print()
    print("----- Raportointiohjelma -----")
    print("------------------------------")
    print("1 - Päiväkohtainen yhteenveto aikaväliltä")
    print("2 - Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
    print("3 - Vuoden 2025 kokonaisyhteenveto")
    print("4 - Lopeta ohjelma")

def daily_summary(meter_data: list, start_date: date, end_date: date) -> list[float, float, float, float, tuple, tuple, date, date]:
    """Generates a daily summary report for the given date range."""
    net_consumption = [0.0]
    net_production = [0.0]
    average_temperature = [0.0]
    net_load = [0.0]
    date_time = meter_data[0][0].date()
    highest_consumption = (date_time, 0.0, 0,0)
    lowest_consumption = (date_time, 9999999.0, 0.0)
    if start_date < date_time.date():
            start_date = date_time.date()
            print(f"\n Datatiedoston alkupäivä: {finnish_date(start_date)}. Aloitetaan raportti tästä päivästä.\n")
    if end_date > meter_data[-1][0].date():
            end_date = meter_data[-1][0].date()
            print(f"\n Datatiedoston loppupäivä: {finnish_date(end_date)}. Lopetetaan raportti tähän päivään.\n")
    for line in meter_data:
        if line[0].date() >= start_date and line[0].date() <= end_date:
            net_consumption += line[1]
            net_production += line[2]
            average_temperature += line[3]
            net_load += line[2] - line[1]
            if line[1] > highest_consumption[1]:
                highest_consumption = (date_time.date(), line[1], line[3])
            if line[1] < lowest_consumption[1]:
                lowest_consumption = (date_time.date(), line[1], line[3])
        else:
            continue
    average_temperature = average_temperature / ((end_date - start_date).days + 1)
    return [net_consumption, net_production, average_temperature, net_load, highest_consumption, lowest_consumption, start_date, end_date]
    

def secondary_menu():
    """Prints the secondary menu options."""
    print()
    print("----- Mitä haluat tehdä seuraavaksi? -----")
    print("------------------------------------------")
    print("1 - Kirjoita raportti tiedostoon raportti.txt")
    print("2 - Luo uusi raportti")
    print("3 - Lopeta")


def main():
    """Main function to run the report maker program."""
    main_menu()
    """Main menu loop."""
    meter_data = read_meter_data("2025.csv")
    while True:
        choice = input("\nSyötä valintasi: ")
        if choice == "1":
            print("\nPäiväkohtainen yhteenveto aikaväliltä valittu.\n")
            input_start_date = input("Syötä alkupäivämäärä (pp.kk.vvvv): ")
            input_end_date = input("\nSyötä loppupäivämäärä (pp.kk.vvvv): ")
            if not format ("%d.%m.%Y" in input_start_date and "%d.%m.%Y" in input_end_date) or input_start_date == "" or input_end_date == "":
                print("\nVirheellinen päivämäärä, Pitää olla pp.kk.vvvv. Yritä uudelleen.")
                continue
            elif datetime.strptime(input_start_date, "%d.%m.%Y").date() > datetime.strptime(input_end_date, "%d.%m.%Y").date():
                print("\nAlkupäivämäärä ei voi olla loppupäivämäärää myöhemmin. Yritä uudelleen.")
                continue
            else:
                start_date = datetime.strptime(input_start_date, "%d.%m.%Y").date()
                end_date = datetime.strptime(input_end_date, "%d.%m.%Y").date()
                summary = daily_summary(meter_data, start_date, end_date)
                print(f"\nRaportti aikaväliltä {finnish_date(summary[6])} - {finnish_date(summary[7])}:\n")
                print("Kokonaiskulutus (kWh): ", (round(summary[0], 2)))
                print("Kokonaistuotanto (kWh): ", (round(summary[1], 2)))
                print("Keskilämpötila (°C): ", round(summary[2], 2))
                print("Nettokuorma (kWh): ", round(summary[3], 2))
                print("Korkein kulutus (kWh): ", round(summary[4][1], 2), "päivänä", finnish_date(summary[4][0]), "keskilämpötila:", round(summary[4][2], 2), "°C")
                print("Matalin kulutus (kWh): ", round(summary[5][1], 2), "päivänä", finnish_date(summary[5][0]), "keskilämpötila:", round(summary[5][2], 2), "°C\n")
        elif choice == "2":
            print("\nKuukausikohtainen yhteenveto yhdelle kuukaudelle valittu.\n")
            # Call the function for monthly summary here
        elif choice == "3":
            print("\nVuoden 2025 kokonaisyhteenveto valittu.\n")
            # Call the function for yearly summary here
        elif choice == "4":
            print("\nLopetetaan ohjelma.\n")
            sys.exit()
        else:
            print("\nVirheellinen valinta. Yritä uudelleen.")
            continue
    


if __name__ == "__main__":
    main()