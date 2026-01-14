# 📊 Dashboard Penjualan UMKM (Streamlit)

Aplikasi **Dashboard Penjualan UMKM** berbasis web yang dibuat menggunakan **Python & Streamlit** untuk membantu pelaku usaha menganalisis data penjualan dengan cepat, visual, dan profesional.

Aplikasi ini mendukung **upload data CSV/Excel**, menampilkan **grafik interaktif**, serta menyediakan fitur **export laporan ke Excel dan PDF lengkap dengan logo UMKM**.

---

## 🚀 Fitur Utama

✅ Upload data penjualan (CSV / Excel)
✅ Validasi otomatis kolom data
✅ Ringkasan total penjualan (Rp)
✅ Grafik penjualan harian (tren waktu)
✅ Grafik penjualan per cabang
✅ Grafik penjualan per kasir
✅ Distribusi penjualan per produk (pie chart)
✅ Pilihan tema warna laporan (Biru, Hijau, Merah)
✅ Export laporan ke **Excel** (multi-sheet)
✅ Export laporan ke **PDF profesional** + logo UMKM

---

## 🛠️ Teknologi yang Digunakan

* **Python**
* **Streamlit** – Web dashboard
* **Pandas** – Pengolahan data
* **Matplotlib** – Visualisasi grafik
* **FPDF** – Generate laporan PDF
* **OpenPyXL** – Export Excel

---

## 📂 Struktur Project

```text
dashboard-penjualan/
│
├── app.py              # File utama aplikasi
├── requirements.txt    # Dependency untuk deploy
└── README.md           # Dokumentasi project
```

---

## 📊 Format Data yang Didukung

File CSV / Excel **WAJIB** memiliki kolom berikut:

| Nama Kolom | Keterangan        |
| ---------- | ----------------- |
| Tanggal    | Tanggal transaksi |
| Produk     | Nama produk       |
| Jumlah     | Jumlah terjual    |
| Harga      | Harga satuan      |
| Kasir      | Nama kasir        |
| Cabang     | Nama cabang       |

---

## ▶️ Cara Menjalankan Secara Lokal

1. Clone repository ini

```bash
git clone https://github.com/username/dashboard-penjualan.git
cd dashboard-penjualan
```

2. Install dependency

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi

```bash
streamlit run app.py
```

4. Buka browser otomatis atau akses:

```
http://localhost:8501
```

---

## ☁️ Deploy ke Streamlit Cloud

1. Upload project ke GitHub (repository **public**)
2. Masuk ke [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Klik **New App**
4. Pilih repository
5. File utama: `app.py`
6. Klik **Deploy**

Aplikasi akan online 24 jam 🚀

---

## 💼 Cocok Digunakan Untuk

* UMKM / Toko Retail
* Rumah Makan / Cafe
* Laporan Penjualan Harian & Bulanan
* Dashboard internal bisnis
* Portfolio **AI / Python Developer**

---

## 👨‍💻 Tentang Developer

**Beni Siswanto**
AI & Python Developer (Junior)

✔️ Berpengalaman membangun aplikasi web berbasis data
✔️ Terbiasa deploy aplikasi ke cloud (24 jam online)
✔️ Fokus solusi sederhana, stabil, dan siap digunakan UMKM

---

## 📌 Catatan

* Data **tidak disimpan di server** (aman & privat)
* Semua proses dilakukan secara real-time
* Cocok untuk penggunaan non-transaksi (analitik & laporan)

---

✨ *Project ini dibuat sebagai bagian dari portfolio freelance dan pengembangan skill Python & AI.*
