# Proyek Analisis Data — Bike Sharing Dataset

Repository ini menyimpan submission **Proyek Analisis Data Dicoding** menggunakan **Bike Sharing Dataset** beserta beberapa arsip submission web pada folder `dicoding-web`.

## Fokus Submission Analisis Data

Submission analisis data berada di root repository dan menggunakan data penyewaan sepeda periode 2011–2012.

Struktur utama:

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── hour.csv
├── data/
│   └── hour.csv
├── Proyek_Analisis_Data.ipynb
├── Advanced_Analysis.ipynb
├── day.csv
├── requirements.txt
├── url.txt
└── README.md
```

## Tahapan Analisis

Proyek mencakup proses analisis data dari:

1. Menentukan pertanyaan bisnis.
2. Gathering data.
3. Assessing data.
4. Cleaning data.
5. Exploratory Data Analysis (EDA).
6. Visualization & explanatory analysis.
7. Conclusion dan recommendation/action item.
8. **Advanced analysis tanpa machine learning** menggunakan manual clustering berbasis binning.

## Advanced Analysis

Notebook `Advanced_Analysis.ipynb` menambahkan teknik analisis lanjutan yang relevan untuk Bike Sharing Dataset.

Teknik yang digunakan adalah **manual clustering menggunakan binning berbasis kuantil (`pandas.qcut`)**. Data permintaan penyewaan per jam (`cnt`) dibagi menjadi tiga segmen:

- **Low Demand**
- **Medium Demand**
- **High Demand**

Tujuan segmentasi ini adalah membantu mengidentifikasi jam, musim, dan tipe hari yang lebih sering mengalami permintaan tinggi. Hasilnya dapat digunakan sebagai dasar action item seperti redistribusi sepeda, pengecekan kapasitas dock, dan peningkatan kesiapan operasional sebelum periode permintaan tinggi.

Teknik ini **tidak menggunakan algoritma machine learning** sehingga sesuai dengan ketentuan analisis lanjutan pada submission.

## Dashboard Streamlit

Dashboard menyajikan:

- Filter tanggal.
- Filter musim dan tipe hari.
- KPI total rental, rata-rata rental per jam, peak hour, dan proporsi High Demand.
- Analisis penyewaan bulanan berdasarkan hari kerja.
- Analisis penyewaan berdasarkan musim.
- Manual clustering Low/Medium/High Demand.
- Analisis High Demand berdasarkan jam.
- Analisis High Demand berdasarkan musim dan tipe hari.
- Actionable insight yang berubah mengikuti filter dashboard.

### Menjalankan Dashboard Secara Lokal

Pastikan Python sudah terpasang, kemudian jalankan:

```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka melalui browser lokal.

## Deployment

Tautan deployment Streamlit dicantumkan pada file `url.txt`.

## Catatan

Folder `dicoding-web` berisi kumpulan submission Web Development sebelumnya dan tidak menjadi bagian utama dari Proyek Analisis Data ini.
