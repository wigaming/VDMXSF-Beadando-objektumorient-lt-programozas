import time

loctime = time.localtime(time.time())

from datetime import datetime


# Definiálunk egy Room osztályt, amely tartalmazza a szoba számát és árát.
class Room:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar


# Az OneBedRoom osztály az Room osztályból származik és beállítja az árat 10000-re.
class OneBedRoom(Room):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 10000)


# A TwoBedRoom osztály az Room osztályból származik és beállítja az árat 15000-re.
class TwoBedRoom(Room):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 15000)


# A Hotel osztály létrehozása, amely tartalmazza a szálloda nevét és a szobákat.
class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    # Új szoba hozzáadása a szállodához.
    def new_room(self, room):
        self.rooms.append(room)


# Definiálunk egy Booking osztályt, amely tartalmazza a foglalás szobáját és dátumát.
class Booking:
    def __init__(self, room, date):
        self.room = room
        self.date = date


# A BookingManager osztály létrehozása, amely kezeli a foglalásokat a szállodában.
class BookingManager:
    def __init__(self, hotel):
        self.hotel = hotel
        self.bookings = []

    # Foglalás létrehozása egy adott szobára és dátumra.
    def booking(self, room_number, date):
        for room in self.hotel.rooms:
            if room.szobaszam == room_number:
                # Ellenőrzés, hogy a megadott szoba és dátumhoz van-e már foglalás
                if not self.check_booking(room, date):
                    return None
                booking = Booking(room, date)
                self.bookings.append(booking)
                return room.ar
        return None

    # Foglalás törlése az adott sorszám alapján.
    def cancel(self, booking_number):
        booking_index = booking_number - 1
        if 0 <= booking_index < len(self.bookings):
            booking = self.bookings[booking_index]
            self.bookings.remove(booking)
            print("A foglalás sikeresen törölve.")
        else:
            print("Érvénytelen foglalás sorszám.")

    # A foglalások listázása.
    def list_bookings(self):
        for i, booking in enumerate(self.bookings):
            print(f"Foglalás {i + 1}: Szoba: {booking.room.szobaszam}, Dátum: {booking.date.strftime('%Y-%m-%d')}")

    # Ellenőrzi, hogy egy adott szobára és dátumra már van-e foglalás.
    def check_booking(self, room, date):
        for booking in self.bookings:
            if booking.room == room and booking.date.date() == date.date():
                return False
        return True


# Szálloda létrehozása és szobák hozzáadása.
def fill_data():
    hotel = Hotel("Példa Szálloda")
    hotel.new_room(OneBedRoom("101"))
    hotel.new_room(OneBedRoom("201"))
    hotel.new_room(TwoBedRoom("202"))
    return hotel


# Fő függvény, amely inicializálja a szállodát és a foglaláskezelőt, majd kezeli a felhasználói interakciót.
def main():
    hotel = fill_data()
    booking_manager = BookingManager(hotel)

    # Példa foglalások hozzáadása
    booking_manager.booking("101", datetime(2024, 5, 15))
    booking_manager.booking("201", datetime(2024, 5, 17))
    booking_manager.booking("202", datetime(2024, 5, 19))
    booking_manager.booking("101", datetime(2024, 5, 20))
    booking_manager.booking("202", datetime(2024, 5, 21))

    # Felhasználói interakció kezelése
    while True:
        print("\nVálassz egy műveletet:")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        choice = input("Művelet sorszáma: ")

        if choice == "1":
            room_number = input("Add meg a foglalni kívánt szoba számát: ")
            current_time = datetime.now()
            print("A legkorábban foglalható dátum: ", current_time.date())
            date_str = input("Add meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date >= current_time:
                    price = booking_manager.booking(room_number, date)
                    if price:
                        print(f"A foglalás sikeres. Ár: {price} Ft.")
                    else:
                        print("Nincs elérhető időpont a megadott szobához és dátumhoz.")
                else:
                    print("A foglalás csak jövőbeli dátumra lehetséges.")
            except ValueError:
                print("Érvénytelen dátum formátum.")
        elif choice == "2":
            booking_number = int(input("Add meg a lemondani kívánt foglalás sorszámát: "))
            booking_manager.cancel(booking_number)
        elif choice == "3":
            print("Foglalások:")
            booking_manager.list_bookings()
        elif choice == "4":
            break
        else:
            print("Érvénytelen művelet.")


# Fő függvény meghívása
if __name__ == "__main__":
    main()
