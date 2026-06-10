import pandas as pd

data = {
    "Nama Kantor": [
        "KPPN Jakarta 1", "KPPN Jakarta 1", "KPPN Jakarta 1",
        "KPPN Jakarta 2", "KPPN Jakarta 2", "KPPN Jakarta 2",
        "KPPN Bandung", "KPPN Bandung", "KPPN Bandung", "KPPN Bandung",
        "KPPN Surabaya", "KPPN Surabaya", "KPPN Surabaya",
    ],
    "Nama Lengkap": [
        "Andi Pratama", "Budi Santoso", "Citra Dewi",
        "Dedi Hermawan", "Eka Putri", "Fajar Nugroho",
        "Gita Amelia", "Hadi Wijaya", "Indah Permata", "Joko Susilo",
        "Kartika Sari", "Lutfi Hakim", "Maya Anggraini",
    ],
    "Pegawai V": [
        "Sudah", "Sudah", "Belum",
        "Sudah", "Belum", "Belum",
        "Sudah", "Sudah", "Sudah", "Belum",
        "Belum", "Belum", "Belum",
    ],
    "Pegawai X": [
        "Sudah", "Belum", "Belum",
        "Sudah", "Sudah", "Belum",
        "Belum", "Belum", "Sudah", "Belum",
        "Sudah", "Belum", "Belum",
    ],
}

df = pd.DataFrame(data)
df.to_excel("/Users/wildansalam/Desktop/monitoring-aktivasi/sample_data.xlsx", index=False)
print("Sample Excel created: sample_data.xlsx")
