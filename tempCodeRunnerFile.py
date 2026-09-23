class Pemain:
    total_pemain = 0
    __base_rating = 50

    def __init__(self, nama: str, rating_awal: int):
        if rating_awal <= 0:
            rating_awal = 10
        self.nama = nama
        self.__rating = rating_awal + Pemain.__base_rating
        Pemain.total_pemain += 1

    def __str__(self):
        return f"Nama: {self.nama}\nRating: {self.__rating}"

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value: int):
        self.__rating = max(0, self.__rating + value)

    @classmethod
    def ubah_base_rating(cls, value):
        cls.__base_rating = max(0, cls.__base_rating + value)


class RosterSlot:
    def __init__(self, pemain: Pemain, jumlah_main: int):
        self.pemain = pemain
        self.__jumlah_main = jumlah_main

    def __str__(self):
        return f"{self.pemain.__str__()}\nJumlah Main: {self.__jumlah_main}"

    @property
    def jumlah_main(self):
        return self.__jumlah_main

    @jumlah_main.setter
    def jumlah_main(self, value: int):
        self.__jumlah_main = max(0, self.__jumlah_main + value)


class Tim:
    max_slot = 5

    def __init__(self, nama_tim):
        self.nama_tim = nama_tim
        self.__slot = Tim.max_slot
        self.daftar_roster = []

    def tambah_roster(self, roster: RosterSlot):
        if roster in self.daftar_roster:
            pos = self.daftar_roster.index(roster)
            self.daftar_roster[pos].jumlah_main += roster.jumlah_main
        elif len(self.daftar_roster) < self.__slot:
            self.daftar_roster.append(roster)
        else:
            print("Maaf, Roster Tim Penuh")

    def hapus_pemain_nonaktif(self):
        self.daftar_roster = [r for r in self.daftar_roster if r.jumlah_main > 0]

    def tampilkan_roster(self):
        for r in self.daftar_roster:
            print(r)


class Tournament:
    def __init__(self, nama_tournament):
        if not self.validasi_nama(nama_tournament):
            raise ValueError("Nama tournament tidak boleh mengandung angka")
        self.nama_tournament = nama_tournament
        self.__hadiah = 0
        self.daftar_tim = []

    @property
    def hadiah(self):
        return self.__hadiah

    @hadiah.setter
    def hadiah(self, value: int):
        self.__hadiah = max(0, self.__hadiah + value)

    def daftarkan_tim(self, tim: Tim):
        self.daftar_tim.append(tim)
        print(f"{tim.nama_tim} berhasil didaftarkan ke {self.nama_tournament}")

    @staticmethod
    def validasi_nama(nama: str):
        return isinstance(nama, str) and nama.replace(" ", "").isalpha()


if __name__ == "__main__":
    print("UJI CLASS METHOD")
    Pemain.ubah_base_rating(20)
    print("Class method berhasil dipanggil")

    print("\nUJI OBJEK")
    pemain1 = Pemain("Reza", 30)
    pemain2 = Pemain("Dinda", 25)

    roster1 = RosterSlot(pemain1, 3)
    roster2 = RosterSlot(pemain2, 2)

    tim1 = Tim("Skyfall Esports")
    turnamen1 = Tournament("PMSC Scrim Week")

    print("\nUJI INSTANCE METHOD")
    print("Roster Sebelum:\n")
    tim1.tampilkan_roster()

    tim1.tambah_roster(roster1)
    tim1.tambah_roster(roster2)
    print("Roster Sesudah:")
    tim1.tampilkan_roster()
    print()

    turnamen1.daftarkan_tim(tim1)

    print("\nUJI SETTER")
    pemain1.rating = 15
    roster1.jumlah_main = 2
    turnamen1.hadiah = 500000
    print(f"Rating {pemain1.nama} (Valid): {pemain1.rating}")
    print(f"Jumlah Main {pemain1.nama} (Valid): {roster1.jumlah_main}")
    print(f"Hadiah {turnamen1.nama_tournament} (Valid): {turnamen1.hadiah}")

    pemain1.rating = -1000
    roster1.jumlah_main = -10
    turnamen1.hadiah = -1000000
    print(f"Rating {pemain1.nama} (Tidak Valid -1000): {pemain1.rating} (Tertahan di 0)")
    print(f"Jumlah Main {pemain1.nama} (Tidak Valid -10): {roster1.jumlah_main} (Tertahan di 0)")
    print(f"Hadiah {turnamen1.nama_tournament} (Tidak Valid -1000000): {turnamen1.hadiah} (Tertahan di 0)")

    print("\nUJI HAPUS PEMAIN NONAKTIF (INSTANCE METHOD)")
    print("Roster Sebelum Dihapus:\n")
    tim1.tampilkan_roster()

    tim1.hapus_pemain_nonaktif()

    print("\nRoster Sesudah Dihapus:")
    tim1.tampilkan_roster()

    print("\nUJI STATIC METHOD")
    uji_nama = Tournament.validasi_nama("PMSC Grand Final")
    print(f"Hasil static method untuk 'PMSC Grand Final': {uji_nama}")

    print("Uji coba membuat tournament dengan angka (Scrim123)...")
    try:
        turnamen_error = Tournament("Scrim123")
    except ValueError as e:
        print(f"Error tertangkap: {e}")