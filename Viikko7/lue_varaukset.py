# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.


# Käytin olioita, koska ne helpottavat datan käsittelyä ja tarjoavat selkeän rakenteen varauksille.
# En koe että sanakirjatkaan sen huonompia tässä varsinaisesti olisi, mutta halusin harjoitella olioiden käyttöä tulevaisuutta varten.
# On todella paljon helpommin luettavaa ilman listoja, koska kaikilla varauksen osilla on selkeät nimet.
# Myös kaikki funktiot ja metodit ovat selkeitä ja helposti ymmärrettäviä.

from datetime import datetime

def edit_reservation(reservations: list[str]) -> object:
    """Edits data types and generates a Reservation object from a list of reservation details."""
    return Reservation(
        reservation_id=int(reservations[0]),
        name = reservations[1],
        email = reservations[2],
        phone = reservations[3],
        reservation_date = datetime.strptime(reservations[4], "%Y-%m-%d").date(),
        reservation_time = datetime.strptime(reservations[5], "%H:%M").time(),
        reservation_duration = int(reservations[6]),
        price = float(reservations[7]),
        reservation_confirmed = reservations[8].lower() == "true",
        reserved_room = reservations[9],
        reservation_created = datetime.strptime(reservations[10], "%Y-%m-%d %H:%M:%S")
    )

def get_reservations(reservationfile: str) -> list[object]:
    """Reads reservations from a file and returns a list of Reservation objects."""
    reservations = []
    with open(reservationfile, "r", encoding="utf-8") as f:
        for reservation in f:
            reservation = reservation.strip()
            reservation_details = reservation.split('|')
            reservations.append(edit_reservation(reservation_details))
    return reservations

class Reservation:
    """A class to represent a reservation."""
    def __init__(self, reservation_id: int, name: str, email: str, phone: str, reservation_date: datetime.date,
                 reservation_time: datetime.time, reservation_duration: int, price: float, reservation_confirmed: bool,
                 reserved_room: str, reservation_created: datetime):
        self.reservation_id = reservation_id
        self.name = name
        self.email = email
        self.phone = phone
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.reservation_duration = reservation_duration
        self.price = price
        self.reservation_confirmed = reservation_confirmed
        self.reserved_room = reserved_room
        self.reservation_created = reservation_created
        
    def long_reservation(self) -> bool:
        """Checks if the reservation duration is 3 hours or more."""
        return self.reservation_duration >= 3
    
    def confirmed(self) -> bool:
        """Returns the confirmation status of the reservation."""
        return self.reservation_confirmed
    
    def total_price(self) -> float:
        """Calculates the total price of the reservation."""
        return self.reservation_duration * self.price

def confirmed_reservations(reservations: list[Reservation]) -> None:
    for reservation in reservations:
        if reservation.confirmed():
            print(f"- {reservation.name}, {reservation.reserved_room}, {reservation.reservation_date.strftime('%d.%m.%Y')} klo {reservation.reservation_time.strftime('%H.%M')}")
    print()

def long_reservations(reservations: list[Reservation]) -> None:
    for reservation in reservations:
        if reservation.long_reservation():
            print(f"- {reservation.name}, {reservation.reservation_date.strftime('%d.%m.%Y')} klo {reservation.reservation_time.strftime('%H.%M')}, kesto {reservation.reservation_duration} h, {reservation.reserved_room}")
    print()

def reservation_confirmation_status(reservations: list[Reservation]) -> None:
    for reservation in reservations:
        if reservation.confirmed():
            print(f"{reservation.name} → Vahvistettu")
        else:
            print(f"{reservation.name} → EI vahvistettu")
    print()

def number_of_reservations(reservations: list[Reservation]) -> None:
    confirmed_reservations = 0
    unconfirmed_reservations = 0
    for reservation in reservations:
        if reservation.confirmed():
            confirmed_reservations += 1
        else:
            unconfirmed_reservations += 1
    print(f"- Vahvistettuja varauksia: {confirmed_reservations} kpl")
    print(f"- Ei-vahvistettuja varauksia: {unconfirmed_reservations} kpl")
    print()

def total_revenue(reservations: list[Reservation]) -> None:
    total_revenue = 0
    for reservation in reservations:
        if reservation.confirmed():
            total_revenue += reservation.total_price()
    print("Vahvistettujen varausten kokonaistulot:", f"{total_revenue:.2f}".replace('.', ','), "€")
    print()

def main():
    Reservations = get_reservations("varaukset.txt")
    print("1) Vahvistetut varaukset")
    confirmed_reservations(Reservations)
    print("2) Pitkät varaukset (≥ 3 h)")
    long_reservations(Reservations)
    print("3) Varausten vahvistusstatus")
    reservation_confirmation_status(Reservations)
    print("4) Yhteenveto vahvistuksista")
    number_of_reservations(Reservations)
    print("5) Vahvistettujen varausten kokonaistulot")
    total_revenue(Reservations)

if __name__ == "__main__":
    main()