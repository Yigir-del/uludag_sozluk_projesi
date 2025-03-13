import requests
from bs4 import BeautifulSoup
import parser

class Scraper:
    def __init__(self,cookies = ""):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Safari/537.36"
        }
        if cookies == "":
            self.cookies = {
                "theme": "light",
                "punteriz501": "2503111825231140",
                "PHPSESSID": "b7bm9a7qnfn8m854rsds4fbroi",
                "iab_goole_ads": "49958ea193ed6ccc722e53aef9f3d0a9",
            }
        else:
            self.cookies = cookies
        self.response = []
        self.session_ = requests.Session()
        self.num = 0  # Sayfa numarasını None olarak başlatıyoruz
        self.this_page_isempty = False

    def post_url(self, url, data):
        try:
            # Giriş sayfasını al
            get_page = self.session_.get(url=url, headers=self.headers)
            if get_page.status_code != 200:
                print(f"[HATA] Login sayfası çekilemedi. Hata kodu: {get_page.status_code}")
                return False

            # Token'ı al
            html_icerigi = BeautifulSoup(get_page.content, "html.parser")
            token_input = html_icerigi.find("input", {"name": "__RequestVerificationToken"})

            if token_input:
                token = token_input.get("value")
                self.payload = {
                    "username": data["username"],
                    "password": data["password"],
                    "__RequestVerificationToken": token,
                }
            else:
                print("[UYARI] Token bulunamadı, ancak devam ediliyor...")
                self.payload = {
                    "username": data["username"],
                    "password": data["password"],
                }

            # POST işlemi
            post_page = self.session_.post(url=url, headers=self.headers, data=self.payload)

            # Hata kodlarını detaylı kontrol et
            if post_page.status_code == 403:
                print("[HATA] Yetkisiz giriş (403 Forbidden). Çerezler veya kullanıcı bilgileri hatalı olabilir.")
                return False
            elif post_page.status_code == 401:
                print("[HATA] Yetkilendirme başarısız (401 Unauthorized). Kullanıcı adı veya şifre yanlış olabilir.")
                return False
            elif post_page.status_code == 500:
                print("[HATA] Sunucu hatası (500 Internal Server Error). Site tarafında bir problem olabilir.")
                return False
            elif post_page.status_code != 200:
                print(f"[HATA] Giriş başarısız. HTTP Hata Kodu: {post_page.status_code}")
                return False

            # Sayfa içeriğinde hata mesajı var mı kontrol et
            error_message = BeautifulSoup(post_page.content, "html.parser").find("div", {"class": "error"})
            if error_message:
                print(f"[HATA] Site hata mesajı döndürdü: {error_message.text.strip()}")
                return False

            print("[BAŞARILI] Sayfaya giriş yapıldı.")
            return True

        except requests.RequestException as e:
            print(f"[HATA] Bağlantı hatası oluştu: {e}")
            return False


    def fetch_html(self, url):
        self.response = []  # Yanıtları temizle
        try:
            # İlk sayfayı al
            local_response = self.session_.get(url=url, cookies=self.cookies, headers=self.headers)

            # Hata kodlarına göre detaylı mesaj ver
            if local_response.status_code == 403:
                print("[HATA] Erişim engellendi (403 Forbidden). Çerezler veya oturum süresi dolmuş olabilir.")
                return False
            elif local_response.status_code == 404:
                print("[HATA] Sayfa bulunamadı (404 Not Found). URL yanlış olabilir.")
                return False
            elif local_response.status_code == 500:
                print("[HATA] Sunucu hatası (500 Internal Server Error). Site tarafında bir problem olabilir.")
                return False
            elif local_response.status_code != 200:
                print(f"[HATA] Sayfa yüklenemedi. HTTP Hata Kodu: {local_response.status_code}")
                return False

            # Sayfa içeriğini parse et
            soup = BeautifulSoup(local_response.content, "html.parser")

            # Eğer sayfa boşsa
            empty_page = soup.find("div", {"class": "my-4 text-center p-3 bg-danger text-white rounded"})
            if empty_page:
                self.this_page_isempty = True
                print("Baslik yok..")
                return

            # Sayfa sayısını al
            page_count_div = soup.find("div", {"class": "ulupages"})
            if page_count_div:
                page_count = page_count_div.get("data-pagecount")
                if page_count and page_count.isdigit():
                    page_count = int(page_count)
                    print(f"Toplam sayfa sayısı: {page_count}")
                    self.num = page_count
                else:
                    print("Sayfa sayısı bulunamadı veya geçersiz.")
            else:
                print("Toplam sayfa sayısı: 1")

            # Sayfa sayısı yoksa işlem yapma
            if not self.num and self.this_page_isempty:
                print("Sayfa sayısı alınamadı veya geçersiz.")
                return False

            # Sayfa numarasını sayısal değere dönüştür
            try:
                self.num = int(self.num)
            except ValueError:
                print("Sayfa sayısı geçersiz.")
                return False

            # İlk sayfanın içeriğini yanıt listesine ekle
            self.response.append(local_response.content)

            # Diğer sayfalara geçiş yap
            for i in range(2, self.num + 1):
                next_url = f"{url.rstrip('/')}/{i}/"
                local_response = self.session_.get(url=next_url, cookies=self.cookies, headers=self.headers)

                if local_response.status_code == 403:
                    print(f"[HATA] Sayfa {i}: Erişim engellendi (403 Forbidden).")
                    continue
                elif local_response.status_code == 404:
                    print(f"[HATA] Sayfa {i}: Sayfa bulunamadı (404 Not Found).")
                    continue
                elif local_response.status_code == 500:
                    print(f"[HATA] Sayfa {i}: Sunucu hatası (500 Internal Server Error).")
                    continue
                elif local_response.status_code != 200:
                    print(f"[HATA] Sayfa {i} alınamadı. HTTP Hata Kodu: {local_response.status_code}")
                    continue

                self.response.append(local_response.text)

            print("[BAŞARILI] HTML alındı.")
            return self.response

        except requests.RequestException as e:
            print(f"[HATA] Bağlantı hatası oluştu: {e}")
            return False


if __name__ == "__main__":
    url = "https://www.uludagsozluk.com/login/"
    data = {
        "username": "username",
        "password": "password",
    }

    my_scrpy = Scraper()
    my_scrpy.post_url(url, data)
    response = my_scrpy.fetch_html("https://www.uludagsozluk.com/mesajlarim/")
    print("Tüm işlemler tamamlandı..")
