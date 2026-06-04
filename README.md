# AWS S3 Auto-Remediation System using Event-Driven Architecture

Proyek ini merupakan sistem mitigasi dan remediasi keamanan otomatis (*auto-remediation*) pada penyimpanan cloud Amazon S3 berbasis *Event-Driven Architecture*. Sistem ini dirancang untuk mendeteksi celah keamanan berupa pengubahan akses *bucket* S3 menjadi publik secara tidak sah (akibat *human error* atau serangan) dan secara otomatis mengunci kembali *bucket* tersebut menjadi *private* dalam hitungan detik.

## 👥 Anggota Kelompok
* **Dhio Rahmansyah** - Teknik Komputer, Fakultas Ilmu Komputer, Universitas Brawijaya
* 
* 

---

## 🏗️ Arsitektur Sistem

Sistem ini menggunakan pendekatan *serverless* dan *event-driven* dengan alur kerja sebagai berikut:
1. **Pemicu Ancaman:** Entitas (skrip `S3-Security-Breaker`) mengubah konfigurasi S3 Bucket menjadi *Public* atau menyuntikkan *public bucket policy*.
2. **Pencatatan Aktivitas:** AWS CloudTrail menangkap aktivitas *API Call* tersebut (`PutBucketPolicy` / `PutPublicAccessBlock`).
3. **Penyaringan Event:** Amazon EventBridge Rule menyaring log dari CloudTrail menggunakan pola JSON spesifik.
4. **Eksekusi Remediasi:** AWS Lambda (`S3-Auto-Guardian`) dipicu oleh EventBridge untuk mengeksekusi kode pemulihan (mengaktifkan *Block Public Access* dan menghapus policy publik).

[S3 Bucket] ──(Aktivitas Publik)──> [AWS CloudTrail]
│
(Log Event API)
▼
[AWS Lambda Guardian] <──(Trigger)── [Amazon EventBridge Rule]


---

## 📁 Struktur Repositori

```text
├── config/
│   └── event-pattern.json     # Konfigurasi JSON Pattern untuk Amazon EventBridge
├── src/
│   ├── breaker.py             # Source code Lambda Simulator Penyerang
│   └── guardian.py            # Source code Lambda Agen Penyelamat (Remediasi)
└── README.md                  # Dokumentasi Utama Proyek
🛠️ Komponen & Kode Sumber
1. Lambda Security Breaker (src/breaker.py)
Skrip Python (Boto3) yang mensimulasikan kelalaian admin dengan mematikan fitur Block Public Access dan membuka akses read ke publik pada bucket target.

2. Lambda Auto Guardian (src/guardian.py)
Skrip Python (Boto3) yang berfungsi sebagai agen penyelamat. Skrip ini akan menghapus bucket policy publik dan menyalakan kembali seluruh fitur perlindungan Block Public Access.

3. EventBridge Event Pattern (config/event-pattern.json)
Konfigurasi filter JSON yang ditanamkan pada Amazon EventBridge untuk mendeteksi perubahan konfigurasi keamanan pada S3:

JSON
{
  "source": ["aws.s3"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["s3.amazonaws.com"],
    "eventName": ["PutBucketPolicy", "PutBucketAcl", "PutPublicAccessBlock"]
  }
}
🧪 Skenario Pengujian & Demo
Sistem ini mendukung dua mekanisme pengujian fungsionalitas:

A. Pengujian End-to-End Otomatis
Jalankan fungsi Lambda S3-Security-Breaker melalui tombol Test.

Periksa tab Permissions pada S3 Bucket, status akan berubah menjadi Public (Merah).

Tunggu log aktivitas diproses oleh AWS CloudTrail (mengalami jeda/latency sekitar 5-15 menit pada arsitektur pencatatan log default AWS).

Sistem EventBridge akan memicu S3-Auto-Guardian secara otomatis untuk mengembalikan status bucket menjadi Private.

B. Pengujian Instan (Manual Invocation)
Skenario ini digunakan untuk keperluan demonstrasi fungsionalitas logika kode secara cepat guna menghindari jeda waktu pengiriman log AWS CloudTrail:

Jalankan fungsi Lambda S3-Security-Breaker untuk membuka celah keamanan (S3 menjadi Public).

Eksekusi langsung fungsi Lambda S3-Auto-Guardian menggunakan tombol Test di konsol AWS Lambda.

Status S3 Bucket akan langsung pulih menjadi Private secara instan (< 1 detik).
