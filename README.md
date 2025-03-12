# Uludağ Projesi

Bu proje, belirli bir web sitesinden veri çekmek ve işlemek için geliştirilmiştir.

## 📌 Kullanım

1. **Bağımlılıkları yükleyin:**
   ```bash
   ## Gereksinimler

Bu proje için aşağıdaki Python kütüphanelerine ihtiyacınız var:

- `requests`
- `bs4` (BeautifulSoup)

Eğer sisteminizde yüklü değilse, aşağıdaki komutlarla yükleyebilirsiniz:

   ```bash
   pip install requests bs4
   ```

2. **Proje dosyalarını çalıştırın:**
   ```bash
   python manager_uludags.py
   ```

## 🚀 Özellikler
- Web kazıma (scraping) yeteneği
- HTML verisi işleme
- JSON formatında çıktı alma

## 📂 Proje Yapısı
```
/uludag_project
│── manager_uludags.py  # Ana yönetici dosyası
│── parser.py           # HTML verisi işleyen modül
│── scrpy.py            # Web kazıma işlemlerini yöneten modül
│── search.py           # Aramada kullanılıcak kelimeleri içerecek olan modül
│── requirements.txt    # Gerekli kütüphaneler listesi
│── README.md           # Bu dosya
```

- Uludağ Projesi, belirli bir forumdan veri çekerek, üniversiteler hakkında bilgi toplamayı amaçlayan bir web scraping uygulamasıdır. Requests ve BeautifulSoup kütüphanelerini kullanarak sayfalardan veri alır, işler ve anlamlı bir formatta saklar.


## 📜 Lisans
Bu proje MIT lisansı ile lisanslanmıştır.


