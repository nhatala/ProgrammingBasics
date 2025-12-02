# Copyright 2025 Niko Hätälä
# License: MIT

from calendar import month
from datetime import date, datetime, time, timezone
import sys
from typing import List, Dict
from pathlib import Path

def edit_data_types(meter_data: list) -> list:
    """Edits the types of the meter data"""
    meter_data_edited = []
    for data in meter_data:
        date_time = datetime.fromisoformat(data[0])
        consumption = float(data[1].replace(",", "."))
        production = float(data[2].replace(",", "."))
        average_temperature = float(data[3].replace(",", "."))
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

def validate_date_format(date_string: str) -> bool:
    """Validates if the date string is in the format dd.mm.yyyy."""
    try:
        datetime.strptime(date_string, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def finnish_month(month_number: int) -> str:
    """Returns the Finnish month name for the given month number."""
    months = {
        1: "tammikuu",
        2: "helmikuu",
        3: "maaliskuu",
        4: "huhtikuu",
        5: "toukokuu",
        6: "kesäkuu",
        7: "heinäkuu",
        8: "elokuu",
        9: "syyskuu",
        10: "lokakuu",
        11: "marraskuu",
        12: "joulukuu"
    }
    return months.get(month_number, "")

def main_menu():
    """Prints the main menu options."""
    print()
    print("      Raportointiohjelma")
    print("------------------------------")
    print("1 - Päiväkohtainen yhteenveto aikaväliltä")
    print("2 - Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
    print("3 - Vuoden 2025 kokonaisyhteenveto")
    print("4 - Lopeta ohjelma")

def secondary_menu():
    """Prints the secondary menu options."""
    print()
    print("      Mitä haluat tehdä seuraavaksi?")
    print("------------------------------------------")
    print("1 - Kirjoita raportti tiedostoon raportti.txt")
    print("2 - Luo uusi raportti")
    print("3 - Lopeta")

def daily_summary(meter_data: list, start_date: date, end_date: date) -> list[float, float, float, float, tuple, tuple, date, date]:
    """Generates a daily summary report for the given date range."""
    net_consumption = 0.0
    net_production = 0.0
    average_temperature = 0.0
    net_load = 0.0
    date_time = meter_data[0][0].date()
    highest_consumption = (date_time, 0.0, 0,0)
    lowest_consumption = (date_time, 9999999.0, 0.0)
    if start_date < date_time:
            start_date = date_time
            print(f"\nDatatiedoston alkupäivä: {finnish_date(start_date)}. Raportti aloitetaan tästä päivästä.")
    if end_date > meter_data[-1][0].date():
            end_date = meter_data[-1][0].date()
            print(f"\nDatatiedoston viimeinen päivä: {finnish_date(end_date)}. Raportti lopetetaan tähän päivään.")
    for line in meter_data:
        if line[0].date() >= start_date and line[0].date() <= end_date:
            net_consumption += line[1]
            net_production += line[2]
            average_temperature += line[3]
            net_load += line[2] - line[1]
            if line[1] > highest_consumption[1]:
                highest_consumption = (line[0], line[1], line[3])
            if line[1] < lowest_consumption[1]:
                lowest_consumption = (line[0], line[1], line[3])
        else:
            continue
    average_temperature = average_temperature / ((end_date - start_date).days + 1)
    return [net_consumption, net_production, average_temperature, net_load, highest_consumption, lowest_consumption, start_date, end_date]

def print_daily_summary(summary: list):
    """Print daily summary to the console."""
    print(f"\n\nRaportti aikaväliltä {finnish_date(summary[6])} - {finnish_date(summary[7])}:")
    print("-----------------------------------------")
    print("Kokonaiskulutus: ", round(summary[0], 2), " kWh")
    print("Kokonaistuotanto: ", round(summary[1], 2), " kWh")
    print("Keskilämpötila: ", round(summary[2], 2), " °C")
    print("Nettokuorma: ", round(summary[3], 2), " kWh")
    print("Korkein kulutus: ", round(summary[4][1], 2), " kWh / ", finnish_date(summary[4][0]), " / keskilämpötila:", round(summary[4][2], 2), " °C")
    print("Matalin kulutus: ", round(summary[5][1], 2), " kWh / ", finnish_date(summary[5][0]), " / keskilämpötila:", round(summary[5][2], 2), " °C")    

def write_daily_summary(summary: list):
    """Write daily summary to a file."""
    try:
        with open("raportti.txt", "x", encoding="utf-8") as report_file:
            report_file.write(f"\nRaportti aikaväliltä {finnish_date(summary[6])} - {finnish_date(summary[7])}:")
            report_file.write("----------------------------------------------\n")
            report_file.write(f"Kokonaiskulutus: {round(summary[0], 2)} kWh\n")
            report_file.write(f"Kokonaistuotanto: {round(summary[1], 2)} kWh\n")
            report_file.write(f"Keskilämpötila: {round(summary[2], 2)} °C\n")
            report_file.write(f"Nettokuorma: {round(summary[3], 2)} kWh\n")
            report_file.write(f"Korkein kulutus: {round(summary[4][1], 2)} kWh / {finnish_date(summary[4][0])} / keskilämpötila: {round(summary[4][2], 2)} °C\n")
            report_file.write(f"Matalin kulutus: {round(summary[5][1], 2)} kWh / {finnish_date(summary[5][0])} / keskilämpötila: {round(summary[5][2], 2)} °C\n")
    except FileExistsError:
        print("\nTiedosto raportti.txt on jo olemassa. Tyhjennetään ja kirjoitetaan uusi raportti.")
        with open("raportti.txt", "w", encoding="utf-8") as report_file:
            report_file.write(f"\nRaportti aikaväliltä {finnish_date(summary[6])} - {finnish_date(summary[7])}:")
            report_file.write("\n----------------------------------------------\n")
            report_file.write(f"Kokonaiskulutus: {round(summary[0], 2)} kWh\n")
            report_file.write(f"Kokonaistuotanto: {round(summary[1], 2)} kWh\n")
            report_file.write(f"Keskilämpötila: {round(summary[2], 2)} °C\n")
            report_file.write(f"Nettokuorma: {round(summary[3], 2)} kWh\n")
            report_file.write(f"Korkein kulutus: {round(summary[4][1], 2)} kWh / {finnish_date(summary[4][0])} / keskilämpötila: {round(summary[4][2], 2)} °C\n")
            report_file.write(f"Matalin kulutus: {round(summary[5][1], 2)} kWh / {finnish_date(summary[5][0])} / keskilämpötila: {round(summary[5][2], 2)} °C\n")
    print("\nRaportti kirjoitettu tiedostoon raportti.txt")

def monthly_summary(meter_data: list, month: int ) -> list[float, float, float, float, tuple, tuple]:
    """Generates a monthly summary report for the given month."""
    net_consumption = 0.0
    net_production = 0.0
    average_temperature = 0.0
    net_load = 0.0
    date_time = meter_data[0][0].date()
    highest_consumption = (date_time, 0.0, 0,0)
    lowest_consumption = (date_time, 9999999.0, 0.0)
    for line in meter_data:
        if line[0].month != month:
            continue
        else:
            net_consumption += line[1]
            net_production += line[2]
            average_temperature += line[3]
            net_load += line[2] - line[1]
            if line[1] > highest_consumption[1]:
                highest_consumption = (line[0], line[1], line[3])
            if line[1] < lowest_consumption[1]:
                lowest_consumption = (line[0], line[1], line[3])
    average_temperature = average_temperature / sum(1 for line in meter_data if line[0].month == month)
    return [net_consumption, net_production, average_temperature, net_load, highest_consumption, lowest_consumption]

def print_monthly_summary(summary: list, month: int):
    """Print monthly summary to the console."""
    print(f"\n\nRaportti kuukaudelta {finnish_month(month)}:")
    print("-----------------------------------------")
    print("Kokonaiskulutus: ", round(summary[0], 2), " kWh")
    print("Kokonaistuotanto: ", round(summary[1], 2), " kWh")
    print("Keskilämpötila: ", round(summary[2], 2), " °C")
    print("Nettokuorma: ", round(summary[3], 2), " kWh")
    print("Korkein kulutus: ", round(summary[4][1], 2), " kWh / ", finnish_date(summary[4][0]), " / keskilämpötila:", round(summary[4][2], 2), " °C")
    print("Matalin kulutus: ", round(summary[5][1], 2), " kWh / ", finnish_date(summary[5][0]), " / keskilämpötila:", round(summary[5][2], 2), " °C")

def write_monthly_summary(summary: list, month: int):
    """Write monthly summary to a file."""
    try:
        with open("raportti.txt", "x", encoding="utf-8") as report_file:
            report_file.write(f"\nRaportti kuukaudelta {finnish_month(month)}:")
            report_file.write("----------------------------------------------\n")
            report_file.write(f"Kokonaiskulutus: {round(summary[0], 2)} kWh\n")
            report_file.write(f"Kokonaistuotanto: {round(summary[1], 2)} kWh\n")
            report_file.write(f"Keskilämpötila: {round(summary[2], 2)} °C\n")
            report_file.write(f"Nettokuorma: {round(summary[3], 2)} kWh\n")
            report_file.write(f"Korkein kulutus: {round(summary[4][1], 2)} kWh / {finnish_date(summary[4][0])} / keskilämpötila: {round(summary[4][2], 2)} °C\n")
            report_file.write(f"Matalin kulutus: {round(summary[5][1], 2)} kWh / {finnish_date(summary[5][0])} / keskilämpötila: {round(summary[5][2], 2)} °C\n")
    except FileExistsError:
        print("\nTiedosto raportti.txt on jo olemassa. Tyhjennetään ja kirjoitetaan uusi raportti.")
        with open("raportti.txt", "w", encoding="utf-8") as report_file:
            report_file.write(f"\nRaportti kuukaudelta {finnish_month(month)}:")
            report_file.write("\n----------------------------------------------\n")
            report_file.write(f"Kokonaiskulutus: {round(summary[0], 2)} kWh\n")
            report_file.write(f"Kokonaistuotanto: {round(summary[1], 2)} kWh\n")
            report_file.write(f"Keskilämpötila: {round(summary[2], 2)} °C\n")
            report_file.write(f"Nettokuorma: {round(summary[3], 2)} kWh\n")
            report_file.write(f"Korkein kulutus: {round(summary[4][1], 2)} kWh / {finnish_date(summary[4][0])} / keskilämpötila: {round(summary[4][2], 2)} °C\n")
            report_file.write(f"Matalin kulutus: {round(summary[5][1], 2)} kWh / {finnish_date(summary[5][0])} / keskilämpötila: {round(summary[5][2], 2)} °C\n")
    print("\nRaportti kirjoitettu tiedostoon raportti.txt")

def print_yearly_summary(summary: list):
    """Print yearly summary to the console."""
    print(f"\n\nRaportti vuodelta 2025:")
    print("-----------------------------------------")
    print("Kokonaiskulutus: ", round(summary[0], 2), " kWh")
    print("Kokonaistuotanto: ", round(summary[1], 2), " kWh")
    print("Keskilämpötila: ", round(summary[2], 2), " °C")
    print("Nettokuorma: ", round(summary[3], 2), " kWh")
    print("Korkein kulutus: ", round(summary[4][1], 2), " kWh / ", finnish_date(summary[4][0]), " / keskilämpötila:", round(summary[4][2], 2), " °C")
    print("Matalin kulutus: ", round(summary[5][1], 2), " kWh / ", finnish_date(summary[5][0]), " / keskilämpötila:", round(summary[5][2], 2), " °C")

def write_yearly_summary(summary: list):
    """Write yearly summary to a file."""
    try:
        with open("raportti.txt", "x", encoding="utf-8") as report_file:
            report_file.write(f"\nRaportti vuodelta 2025:")
            report_file.write("----------------------------------------------\n")
            report_file.write(f"Kokonaiskulutus: {round(summary[0], 2)} kWh\n")
            report_file.write(f"Kokonaistuotanto: {round(summary[1], 2)} kWh\n")
            report_file.write(f"Keskilämpötila: {round(summary[2], 2)} °C\n")
            report_file.write(f"Nettokuorma: {round(summary[3], 2)} kWh\n")
            report_file.write(f"Korkein kulutus: {round(summary[4][1], 2)} kWh / {finnish_date(summary[4][0])} / keskilämpötila: {round(summary[4][2], 2)} °C\n")
            report_file.write(f"Matalin kulutus: {round(summary[5][1], 2)} kWh / {finnish_date(summary[5][0])} / keskilämpötila: {round(summary[5][2], 2)} °C\n")
    except FileExistsError:
        print("\nTiedosto raportti.txt on jo olemassa. Tyhjennetään ja kirjoitetaan uusi raportti.")
        with open("raportti.txt", "w", encoding="utf-8") as report_file:
            report_file.write(f"\nRaportti vuodelta 2025:")
            report_file.write("\n----------------------------------------------\n")
            report_file.write(f"Kokonaiskulutus: {round(summary[0], 2)} kWh\n")
            report_file.write(f"Kokonaistuotanto: {round(summary[1], 2)} kWh\n")
            report_file.write(f"Keskilämpötila: {round(summary[2], 2)} °C\n")
            report_file.write(f"Nettokuorma: {round(summary[3], 2)} kWh\n")
            report_file.write(f"Korkein kulutus: {round(summary[4][1], 2)} kWh / {finnish_date(summary[4][0])} / keskilämpötila: {round(summary[4][2], 2)} °C\n")
            report_file.write(f"Matalin kulutus: {round(summary[5][1], 2)} kWh / {finnish_date(summary[5][0])} / keskilämpötila: {round(summary[5][2], 2)} °C\n")
    print("\nRaportti kirjoitettu tiedostoon raportti.txt")

def main():
    """Main function to run the report maker program."""
    meter_data = read_meter_data("2025.csv")
    while True:
        main_menu()
        """Main program loop."""
        choice = input("\nSyötä valintasi: ")
        if choice == "1":
            """Do daily summary."""
            print("\nPäiväkohtainen yhteenveto aikaväliltä valittu.\n")
            input_start_date = input("Syötä alkupäivämäärä (pp.kk.vvvv): ")
            input_end_date = input("\nSyötä loppupäivämäärä (pp.kk.vvvv): ")
            if input_start_date == "" or input_end_date == "" or not validate_date_format(input_start_date) or not validate_date_format(input_end_date):
                print("\nVirheellinen päivämäärä, Pitää olla pp.kk.vvvv. Yritä uudelleen.")
                continue
            elif datetime.strptime(input_start_date, "%d.%m.%Y").date() > datetime.strptime(input_end_date, "%d.%m.%Y").date():
                print("\nAlkupäivämäärä ei voi olla loppupäivämäärää myöhemmin. Yritä uudelleen.")
                continue
            else:
                start_date = datetime.strptime(input_start_date, "%d.%m.%Y").date()
                end_date = datetime.strptime(input_end_date, "%d.%m.%Y").date()
                summary = daily_summary(meter_data, start_date, end_date)
                print_daily_summary(summary)
            secondary_menu()
            """Secondary options loop."""
            while True:
                secondary_choice = input("\nSyötä valintasi: ")
                if secondary_choice == "1":
                    write_daily_summary(summary)
                    break
                elif secondary_choice == "2":
                    break
                elif secondary_choice == "3":
                    print("\nLopetetaan ohjelma.\n")
                    sys.exit()
                else:
                    print("\nVirheellinen valinta. Yritä uudelleen.")
                    continue
        elif choice == "2":
            """Do monthly summary."""
            print("\nKuukausikohtainen yhteenveto yhdelle kuukaudelle valittu.\n")
            input_month = input("Syötä kuukauden numero (1-12): ")
            if not input_month.isdigit() or int(input_month) < 1 or int(input_month) > 12 or input_month == "":
                print("\nVirheellinen kuukauden numero. Yritä uudelleen.")
                continue
            else:
                month = int(input_month)
                summary = monthly_summary(meter_data, month)
                print_monthly_summary(summary, month)
            secondary_menu()
            """Secondary options loop."""
            while True:
                secondary_choice = input("\nSyötä valintasi: ")
                if secondary_choice == "1":
                    write_monthly_summary(summary, month)
                    break
                elif secondary_choice == "2":
                    break
                elif secondary_choice == "3":
                    print("\nLopetetaan ohjelma.\n")
                    sys.exit()
                else:
                    print("\nVirheellinen valinta. Yritä uudelleen.")
                    continue
        elif choice == "3":
            """Do yearly summary."""
            print("\nVuoden 2025 kokonaisyhteenveto valittu.\n")
            start_date = datetime.strptime("01.01.2025", "%d.%m.%Y").date()
            end_date = datetime.strptime("31.12.2025", "%d.%m.%Y").date()
            summary = daily_summary(meter_data, start_date, end_date)
            print_yearly_summary(summary)
            secondary_menu()
            """Secondary options loop."""
            while True:
                secondary_choice = input("\nSyötä valintasi: ")
                if secondary_choice == "1":
                    write_yearly_summary(summary)
                    break
                elif secondary_choice == "2":
                    break
                elif secondary_choice == "3":
                    print("\nLopetetaan ohjelma.\n")
                    sys.exit()
                else:
                    print("\nVirheellinen valinta. Yritä uudelleen.")
                    continue
        elif choice == "4":
            """Exit the program."""
            print("\nLopetetaan ohjelma.\n")
            sys.exit()
        else:
            print("\nVirheellinen valinta. Yritä uudelleen.")
            continue

if __name__ == "__main__":
    main()