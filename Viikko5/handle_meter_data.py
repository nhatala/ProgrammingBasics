# Copyright 2025 Niko Hätälä
# License: MIT

from datetime import datetime
from typing import List, Dict

def edit_data_types(meter_data: list) -> list:
    """Edits the types of the meter data."""
    meter_data_edited = []
    for row in meter_data:
        if row[0] == "Date and time":
            meter_data_edited.append(row)
        else:
            date_time = datetime.strptime(row[0].split("T")[0], "%Y-%m-%d %H:%M:%S")
            phase1_consumption = int(row[1])
            phase2_consumption = int(row[2])
            phase3_consumption = int(row[3])
            production_phase1 = int(row[4])
            production_phase2 = int(row[5])
            production_phase3 = int(row[6])
            meter_data_edited.append([date_time, phase1_consumption, phase2_consumption, phase3_consumption, production_phase1, production_phase2, production_phase3])
    return meter_data_edited

def read_meter_data(meter_datafile: str) -> list:
    """Reads meter data, changes types and returns a new list with edited types."""
    meter_data = []
    meter_data.append(["Date and time", "Phase 1 consumption Wh", "Phase 2 consumption Wh", "Phase 3 consumption Wh", "Production phase 1 Wh", "Production phase 2 Wh", "Production phase 3 Wh"])
    with open(meter_datafile, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(";")
            meter_data.append(line)
    meter_data = edit_data_types(meter_data)
    return meter_data


def main():
    """Main function to handle meter data."""
    meter_datafile = "viikko43.csv"
    meter_data = read_meter_data(meter_datafile)
    print(meter_data)


    if __name__ == "__main__":
        main()