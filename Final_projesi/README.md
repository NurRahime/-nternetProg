# Ziyaretçi Kayıt Sistemi Tasarımı

Bu proje, ziyaretçi kayıt sistemi için tasarlanmış bir web arayüzüdür.

## Tasarım Özellikleri

- Modern ve responsive tasarım
- Bootstrap 5 framework kullanımı
- Bootstrap Icons entegrasyonu
- Kullanıcı dostu arayüz
- Ziyaretçi kayıt kartları ile listeleme
- İstatistik kartları(toplam ziyaretçi, son kayıtlar vb.)
- Ziyaretçi bilgileri için detaylı form alanları

## Sayfalar

### Dashboard
- Kullanıcı karşılama ve genel bilgiler
- Toplam ziyaretçi sayısı
- Son eklenen ziyaretçilerin
- Özel istatistik kartları

### Ziyaretçi Ekleme
- Kayıtlı ziyaretçilerin taplosu
- Başlık, kategori ve içerik alanları
- Geri dön ve kaydet butonları 

### Ziyaretçi Yönetimi
- Kayıtlı kullanıcıların listesi
- Kullanıcı ekleme, güncelleme ve silme

## Kullanılan Teknolojiler

- HTML5
- Python 3
- Flask  Framework
- flask-login
- flask-SQLAlchemy
- SQLite
- CSS3
- Bootstrap 5
- Bootstrap Icons
- Jinja2 Template Engine

## Proje Yapısı

```
FirstWeek/
├── templates/
│   ├── base.html
│   ├── dashboard.html
|   ├── dashboardbase.html
|   ├── index.html
│   ├── ziyaretci_ekleme.html
│   ├── ziyaretci_guncelleme.html
│   ├── ziyaretci_liste.html
│   ├── kullanicilar.html
│   ├── kullanici_guncelle.html
│   ├── login.html
│   └── register.html
├── static/
│   ├── base.css/
│   ├── dashboardbase.css/
|   └──index.css
├── app.py
├── alldb.json
├── alldbjson.py
├── README.MD
├── users.json
├── users.py
├── ziyaretci.py
├── requirements.txt 
Instance
└── database.db
final_version.md

```

## Tasarım Özellikleri

### Renkler
- Primary: Mavi (#0d6efd)
- Success: Yeşil (#198754)
- Info: Açık Mavi (#0dcaf0)
- Danger:Kırmızı (#dc3545)

### Responsive Tasarım
- Mobil cihazlara uyumlu
- Tablet ve masaüstü için optimize edilmiş görünüm
- Grid sistemi ile esnek yerleşim

### Kartlar ve Listeler
- Gölgeli tasarım
- Hover efektleri
- İkon entegrasyonu
- Badge'ler ile kategori gösterimi 