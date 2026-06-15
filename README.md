# Sistem Manajemen Insiden dan Remediasi Keamanan Otomatis pada Penyimpanan Cloud Amazon S3 cloud

Proyek arsitektur *cloud* ini mengimplementasikan sistem mitigasi komprehensif yang mengombinasikan pertahanan proaktif di level data (pencegahan) dan pemulihan otomatis di level arsitektur (remediasi) secara *real-time* menggunakan pendekatan **Event-Driven Architecture (EDA)**.

## 👥 Tim Pengembang
* Dhio Rahmansyah (235150301111013)
* Akmal Ahmad Ghozali (235150300111006)
* Muhammad Irsyaddhia Fahlevi (235150307111001)
* Muhfi Fawwaz Rizqullah (235150307111009)

*(Universitas Brawijaya - Fakultas Ilmu Komputer - Teknik Komputer)*

---

## 🚀 Fitur Utama Sistem
1. **Keamanan Level Data (Pertahanan Preventif):** Menggunakan *S3 Bucket Policy* untuk memblokir secara instan setiap unggahan file terlarang (seperti `.png`) di pintu masuk paling depan.
2. **Pemantauan Aktif (Efficient Monitoring):** Terintegrasi dengan *S3 Event Notifications* dan *Amazon SNS* untuk mengirimkan log audit berupa notifikasi email secara *real-time* hanya ketika file yang sah berhasil diunggah.
3. **Simulasi Ancaman (Breaker):** Skrip komputasi *serverless* AWS Lambda yang mensimulasikan kegagalan sistem/*human error* dengan membuka gembok S3 menjadi *Public* sekaligus memicu alarm darurat instan ke email administrator.
4. **Remediasi Otomatis (Guardian):** Fungsi Lambda taktis yang dipicu secara reaktif oleh *Amazon EventBridge* untuk seketika mengunci kembali status *bucket* menjadi *Private* dan menghapus kebijakan publik yang tidak sah.

---

## 🏗️ Komponen Arsitektur AWS
* **Amazon S3:** Tempat penyimpanan utama sekaligus garis pertahanan pertama (*Bucket Policy*).
* **AWS CloudTrail:** Pencatat log audit operasional *API Call*.
* **Amazon EventBridge:** Broker penyaring *event* berdasarkan *pattern* JSON.
* **AWS Lambda:** Eksekutor komputasi untuk fungsi `S3-Security-Breaker` & `S3-Auto-Guardian`.
* **Amazon SNS:** Pusat distribusi pesan (*messaging hub*) untuk pengiriman notifikasi email.

---

## 📂 Struktur Direktori Repository
├── src/
│   ├── breaker.py          # Skrip simulasi serangan & trigger email instan via SNS
│   └── guardian.py         # Skrip remediasi otomatis untuk mengunci kembali S3
├── config/
│   ├── event-pattern.json  # Pattern JSON untuk filter EventBridge
│   ├── bucket-policy.json  # Kebijakan S3 untuk memblokir file .png
│   └── sns-policy.json     # Kebijakan izin akses S3 ke Amazon SNS
└── README.md               # Dokumentasi utama proyek
