# Sistem Manajemen Insiden dan Remediasi Keamanan Otomatis pada Penyimpanan Cloud Amazon S3 🛡️☁️

Proyek arsitektur *cloud* ini mengimplementasikan sistem mitigasi komprehensif yang mengkombinasikan pertahanan proaktif di level data (pencegahan) dan pemulihan otomatis di level arsitektur (remediasi) secara *real-time* menggunakan pendekatan **Event-Driven Architecture (EDA)**[cite: 4].

## 👥 Tim Pengembang
* Dhio Rahmansyah (235150301111013)
* Akmal Ahmad Ghozali (235150300111006)
* Muhammad Irsyaddhia Fahlevi (235150307111001)
* Muhfi Fawwaz Rizqullah (235150307111009)

*(Universitas Brawijaya - Fakultas Ilmu Komputer - Program Studi Teknik Komputer)*[cite: 4]

---

## 🚀 Fitur Utama Sistem
1. **Keamanan Level Data (Pertahanan Preventif):** Menggunakan *S3 Bucket Policy* untuk memblokir secara instan setiap unggahan file terlarang (seperti `.png`) di pintu masuk paling depan[cite: 4].
2. **Pemantauan Aktif (Efficient Monitoring):** Terintegrasi dengan *S3 Event Notifications* dan *Amazon SNS* untuk mengirimkan log audit berupa notifikasi email secara *real-time* (jeda < 2 detik) hanya ketika file yang sah berhasil diunggah[cite: 4].
3. **Simulasi Ancaman (Breaker):** Skrip komputasi *serverless* AWS Lambda yang mensimulasikan kegagalan sistem/*human error* dengan membuka gembok S3 menjadi *Public* sekaligus memicu alarm darurat instan ke email administrator[cite: 4].
4. **Remediasi Otomatis (Guardian):** Fungsi Lambda taktis yang dipicu secara reaktif oleh *Amazon EventBridge* untuk seketika mengunci kembali status *bucket* menjadi *Private* dan menghapus kebijakan publik yang tidak sah[cite: 4].

---

## ⚙️ Alur Kerja Sistem (Workflow)
Sistem ini beroperasi dalam dua skenario pengamanan utama[cite: 4]:

### Skenario 1: Keamanan Level Data (Operasional Harian)
* **Pencegahan (*Deny*):** Saat pengguna mencoba mengunggah file terlarang (`.png`), *S3 Bucket Policy* bertindak sebagai penjaga gerbang yang secara instan memblokir akses (*Access Denied*) tanpa memicu komputasi lanjutan[cite: 4].
* **Pemantauan (*Allow & Notify*):** Pengguna mengunggah file sah (misal: `.txt`, `.jpeg`). S3 menerima file tersebut dan secara otomatis memicu *S3 Event Notifications* untuk menembakkan laporan ke Amazon SNS, yang kemudian diteruskan sebagai email ke administrator[cite: 4].

### Skenario 2: Keamanan Level Arsitektur (Simulasi Serangan & Remediasi)
* **Injeksi Celah & Peringatan Dini:** Skrip `S3-Security-Breaker` dieksekusi untuk menonaktifkan *Block Public Access* pada S3. Secara bersamaan, skrip ini mengirimkan *payload* peringatan darurat langsung ke Amazon SNS, menghasilkan email alarm seketika[cite: 4].
* **Remediasi Otomatis:** Skrip Lambda `S3-Auto-Guardian` dieksekusi untuk meremediasi celah, mengunci kembali status S3 menjadi *Private*, dan menghapus *policy* publik[cite: 4].

---

## 🏗️ Komponen Arsitektur AWS
Sistem ini terdiri dari lima komponen utama AWS yang saling terhubung[cite: 4]:
* **Amazon S3:** Berperan sebagai objek pengawasan (*resource target*) yang menyimpan data kelompok sekaligus garis pertahanan pertama[cite: 4].
* **AWS CloudTrail:** Bertindak sebagai pencatat log (*auditor*) yang merekam setiap aktivitas *API call*[cite: 4].
* **Amazon EventBridge:** Bertindak sebagai broker *event* (mata-mata) yang menyaring log spesifik dari CloudTrail berdasarkan *pattern* JSON[cite: 4].
* **AWS Lambda:** Berperan sebagai eksekutor (*Guardian*) yang dipicu untuk mengunci kembali S3 Bucket, dan eksekutor simulasi serangan (*Breaker*)[cite: 4].
* **Amazon SNS:** Bertindak sebagai pusat distribusi pesan (*messaging hub*) yang mengirimkan notifikasi email secara *real-time* kepada administrator[cite: 4].

---

## 📂 Struktur Direktori Repository

```text
.
├── src/
│   ├── breaker.py          # Skrip simulasi serangan & trigger email instan
│   └── guardian.py         # Skrip remediasi otomatis untuk S3
├── config/
│   ├── event-pattern.json  # Pattern JSON untuk filter EventBridge
│   ├── bucket-policy.json  # Kebijakan S3 untuk memblokir file .png
│   └── sns-policy.json     # Kebijakan gerbang izin akses SNS
└── README.md               # Dokumentasi utama proyek
