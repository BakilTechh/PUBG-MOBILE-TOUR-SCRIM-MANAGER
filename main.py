# SISTEM MANAJEMEN SCRIM / TOURNAMENT PUBG MOBILE 
class JadwalScrim:
    """Class tambahan untuk mendemonstrasikan Komposisi pada class Scrim"""
    def __init__(self, hari, jam):
        self.hari = hari
        self.jam = jam

    def tampilkan_info(self):
        print(f"Hari: {self.hari}, Jam: {self.jam}")


# --- SUPERCLASS ---
class Peserta:
    total_terdaftar = 0
    kategori_game = "PUBG MOBILE"

    def __init__(self, nama):
        if not self.validasi_nama(nama):
            raise ValueError("Nama tidak boleh mengandung angka")
        self._nama = nama
        Peserta.total_terdaftar += 1

    @staticmethod
    def validasi_nama(nama):
        return isinstance(nama, str) and not any(char.isdigit() for char in nama)

    def tampilkan_info(self):
        print(f"Nama: {self._nama}")

    def tampilkan_aksi(self):
        print(f"Peserta {self._nama} bersiap di lobi.")


# --- SUBCLASS 1 ---
class Pemain(Peserta):
    def __init__(self, nama, role, poin_awal=0):
        super().__init__(nama)
        self.role = role
        self.__poin_performa = max(0, poin_awal)

    @property
    def poin_performa(self):
        return self.__poin_performa

    @poin_performa.setter
    def poin_performa(self, nilai):
        # Nilai negatif akan tertahan di 0 (tidak mencetak error/ditolak)
        self.__poin_performa = max(0, nilai)

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f"Role: {self.role}")
        print(f"Poin: {self.__poin_performa}")

    def bertanding(self, poin_tambahan):
        """Menambah poin pemain layaknya mengkonsumsi item."""
        self.poin_performa = self.__poin_performa + poin_tambahan
        print(f"Pemain {self._nama} mencetak kill, dan mendapatkan {poin_tambahan} poin")

    def tampilkan_aksi(self):
        """Override: Perilaku spesifik untuk pemain."""
        print(f"Pemain {self._nama} ({self.role}) sedang bertanding di arena")
        
    @classmethod
    def dari_dict(cls, data: dict):
        """Factory method: membuat objek Pemain langsung dari dictionary data pendaftaran."""
        return cls(data["nama"], data["role"], data.get("poin", 0))


# --- SUBCLASS 2 ---
class Squad(Peserta):
    
    kapasitas_maksimal = 5
    def __init__(self, nama):
        super().__init__(nama)
        self.__dana_operasional = 0
        self.anggota = []

    @property
    def dana_operasional(self):
        return self.__dana_operasional

    @dana_operasional.setter
    def dana_operasional(self, nilai):
        self.__dana_operasional = max(0, nilai)

    def rekrut_pemain(self, pemain: Pemain):
        if len(self.anggota) >= Squad.kapasitas_maksimal:
            print(f"[GAGAL] Squad {self._nama} sudah mencapai kapasitas maksimal.")
            return
        self.anggota.append(pemain)

    def hapus_pemain_poin_kosong(self):
        self.anggota = [p for p in self.anggota if p.poin_performa > 0]

    def tampilkan_isi(self):
        for p in self.anggota:
            p.tampilkan_info()

    def tampilkan_aksi(self):
        """Override: Perilaku spesifik untuk squad."""
        print(f"Menurunkan Squad {self._nama} ke arena")


# --- CLASS UTAMA 3 ---
class Scrim:
    def __init__(self, judul):
        self.judul = judul
        self.jadwal = JadwalScrim("Minggu", "19.00")
        self.squad_unggulan = None                   

    def pegang_squad(self, squad: Squad):
        self.squad_unggulan = squad
        print(f"{self.judul} memegang: {squad._nama}")

    def lepas_squad(self):
        self.squad_unggulan = None
        print("Tidak ada squad yang dipegang")


# PENGUJIAN PROGRAM
if __name__ == "__main__":
    
    squad_btr = Squad("Bigetron Alpha")
    pemain_ryzen = Pemain("Ryzen", "Rusher", 0)
    pemain_zuxxy = Pemain("Zuxxy", "IGL", 50)
    scrim_malam = Scrim("Scrim Malam Mingguan")

    print("UJI METHOD OVERRIDING")
    print("UJI CLASS METHOD")
    pemain_dari_data = Pemain.dari_dict({"nama": "Rosemary", "role": "Sniper", "poin": 40})
    print(f"Pemain berhasil dibuat lewat class method: {pemain_dari_data._nama}")

    print("\nUJI METHOD OVERRIDING")
    squad_btr.tampilkan_aksi()
    squad_btr.tampilkan_aksi()
    pemain_ryzen.bertanding(50)
    print(f"Poin {pemain_ryzen._nama} setelah bertanding: {pemain_ryzen.poin_performa}")

    print("\nUJI INSTANCE METHOD")
    print("Daftar Anggota Sebelum:\n")
    squad_btr.tampilkan_isi()

    squad_btr.rekrut_pemain(pemain_ryzen)
    print("Daftar Anggota Sesudah:")
    squad_btr.tampilkan_isi()
    print()

    squad_btr.rekrut_pemain(pemain_zuxxy)
    print(f"Daftar Anggota Sesudah Ditambah Lagi ({pemain_zuxxy._nama}, formasi digabung):")
    squad_btr.tampilkan_isi()
    print()

    print("UJI ASOSIASI")
    scrim_malam.pegang_squad(squad_btr)
    squad_btr.tampilkan_aksi()
    scrim_malam.lepas_squad()

    print("\nUJI AGREGASI (Squad dihapus, Pemain tetap ada)")
    pemain_microboy = Pemain("Microboy", "Support", 30)
    squad_sementara = Squad("Evos Reborn")
    squad_sementara.rekrut_pemain(pemain_microboy)
    print("Squad berisi:")
    squad_sementara.tampilkan_isi()

    del squad_sementara
    print("\nSquad dihapus. Pemain Microboy masih ada:")
    pemain_microboy.tampilkan_info()

    print("\nUJI KOMPOSISI (Scrim dihapus, Jadwal ikut hilang)")
    scrim_kampus = Scrim("Scrim Kampus")
    print(f"Jadwal milik {scrim_kampus.judul}:")
    scrim_kampus.jadwal.tampilkan_info()

    del scrim_kampus
    print("\nScrim dihapus, Jadwal nya  juga akan ikut hilang ")

    print("\nUJI SETTER")
    squad_btr.dana_operasional = 100
    pemain_ryzen.poin_performa = 6
    print(f"Dana Operasional {squad_btr._nama} (Valid): {squad_btr.dana_operasional}")
    print(f"Poin Performa {pemain_ryzen._nama} (Valid): {pemain_ryzen.poin_performa}")

    squad_btr.dana_operasional = -500
    pemain_ryzen.poin_performa = -10
    print(f"Dana Operasional {squad_btr._nama} (Tidak Valid -500): {squad_btr.dana_operasional} (Tertahan di 0)")
    print(f"Poin Performa {pemain_ryzen._nama} (Tidak Valid -10): {pemain_ryzen.poin_performa} (Tertahan di 0)")

    print("\nUJI HAPUS ITEM (INSTANCE METHOD)")
    pemain_ryzen.poin_performa = 0
    print("Daftar Anggota Sebelum Dihapus:")
    squad_btr.tampilkan_isi()

    squad_btr.hapus_pemain_poin_kosong()

    print("\nDaftar Anggota Sesudah Dihapus:")
    squad_btr.tampilkan_isi()

    print("\nUJI STATIC METHOD")
    uji_nama = Peserta.validasi_nama("Kairi")
    print(f"Hasil static method untuk 'Kairi': {uji_nama}")

    print("Uji coba membuat peserta dengan angka (Kairikumar)...")
    try:
        pemain_error = Pemain("Kairikumar", "Support")
    except ValueError as e:
        print(f"Error tertangkap: {e}")