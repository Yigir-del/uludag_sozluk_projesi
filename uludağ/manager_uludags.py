import wish_list
import sys
import unicodedata
import json
import os
import requests
import parser
from requests.utils import quote  # Güvenli URL oluşturma

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding="utf-8")

import scrpy


class Manager:
    def __init__(self, url1, target_url):
        self.url1 = url1
        self.target_url = target_url
        self.call_scrpy()

    def call_scrpy(self):
        my_scrpy = scrpy.Scraper()
        response = my_scrpy.fetch_html(self.url1)

        if not response:
            print(f"❌ Hata: {self.target_url} için HTML içeriği alınamadı.")
            return

        if not isinstance(response, list):
            print(
                f"❌ Hata: {self.target_url} için geçersiz yanıt alındı -> {response}"
            )
            return

        try:
            parsed_data = parser.HtmlParser(response)
            if self.target_url not in data_dict:
                data_dict[self.target_url] = (
                    {}
                )  # Her istek data için yeni bir sözlük oluştur
            # Aynı başlıklar için yorumları birleştir
            for baslik, yorumlar in parsed_data.to_dict().items():
                if baslik in data_dict[self.target_url]:
                    data_dict[self.target_url][baslik].update(yorumlar)
                else:
                    data_dict[self.target_url][baslik] = yorumlar
        except Exception as e:
            print(f"❌ Hata: {self.target_url} için veri ayrıştırılamadı. {e}")

        self.all_data = data_dict


def fix_unicode(text):
    """Unicode normalizasyonu yap ve hatalı karakterleri düzelt."""
    text = unicodedata.normalize("NFC", text)  # Bozuk karakterleri düzelt
    text = text.replace("i̇", "i").replace("İ", "İ")  # Bağımsız noktayı düzelt
    return text


data_dict = {}

if __name__ == "__main__":
    target_istek = [fix_unicode(istek.lower()) for istek in wish_list.istekler]
    target_istek = [quote(istek, safe="") for istek in target_istek]

    for target in target_istek:
        help_url = (
            f"https://www.uludagsozluk.com/ax/?ne=tavsiye&nw=baslik&q={target}"
        )
        print(f" URL: {help_url}")

        response = requests.get(help_url)

        try:
            data = response.json()
            if "basliklar" not in data:
                print(f" Uyarı: {target} için başlık bulunamadı.")
                continue

            for basliklar in data["basliklar"]:
                baslik = basliklar.get("baslik", "").strip()
                if not baslik:
                    continue

                target_help = baslik.replace(" ", "-")
                target_url = f"https://www.uludagsozluk.com/k/{target_help}"

                print(f"📌 İşleniyor: {target_url}")
                my_manager = Manager(url1=target_url, target_url=target)

        except json.JSONDecodeError:
            print(f" Hata: {target} için JSON verisi parse edilemedi.")
            continue

    # Eğer veri varsa JSON dosyasına kaydet
    if data_dict:
        data_dict["total_comments"] = parser.HtmlParser.counter
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data_dict, file, indent=4, ensure_ascii=False)
        print(" Veriler başarıyla `data.json` dosyasına kaydedildi!")
    else:
        print(" Uyarı: Kaydedilecek veri bulunamadı.")
