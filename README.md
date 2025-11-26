# Sistem Pendukung Keputusan Beasiswa Mahasiswa

Metode: **Klasifikasi (Decision Tree)**  
Framework Web: **Streamlit**

## Struktur File
- `app.py` : Kode utama aplikasi Streamlit
- `data_beasiswa.csv` : Dataset beasiswa (data sintetis)
- `requirements.txt` : Daftar library yang dibutuhkan

## Cara Menjalankan di Lokal

1. Buat dan aktifkan virtual environment (opsional tapi disarankan)
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

## Cara Deploy ke Streamlit Cloud

1. Buat repo baru di GitHub, upload semua file (`app.py`, `data_beasiswa.csv`, `requirements.txt`).
2. Buka https://share.streamlit.io dan login.
3. Pilih repo GitHub tadi dan file utama `app.py`.
4. Deploy, lalu salin URL aplikasi untuk dikumpulkan ke dosen.