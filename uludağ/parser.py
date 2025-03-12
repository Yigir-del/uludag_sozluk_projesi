from bs4 import BeautifulSoup


class HtmlParser:
    counter = 0

    def __init__(self, html):
        self.all_data = {}  # Tüm başlık ve yorumları saklamak için sözlük

        for i in range(0,len(html)):  # HTML sayfalarını sırayla işle
            print(f"Html: {i+1}")
            self.soup = BeautifulSoup(html[i], "html.parser")
            self.extract_data(self.soup)

    def extract_data(self, text1):
        tablo = text1.find("div", {"class": "col-entry-main-ulu"})
        if not tablo:
            return  # Eğer tablo bulunamazsa işlemi sonlandır

        # Başlık bilgisini al
        baslik_row = tablo.find(
            "div",
            {
                "class": "entry-header ms-0 ms-lg-3 d-flex justify-content-between align-items-center"
            },
        )
        baslik = (
            baslik_row.find("span").text.strip()
            if baslik_row and baslik_row.find("span")
            else None
        )

        if not baslik:
            return  # Eğer başlık yoksa işlemi sonlandır

        # Yazar bilgilerini al
        yorum_listesi = []  # Bu başlığa ait yorumları tutacak liste
        users = tablo.find_all("div", {"class": "entry-area px-0 px-lg-3"})

        for kademe in users:
            user = kademe.find("div", {"class": "entry-body"})
            id_ = user["id"]
            username_kademe = kademe.find("div", {"class": "entry-footer"})
            username = (
                username_kademe.find("div", {"class": "yazar-div"}).text.strip()
                if username_kademe
                and username_kademe.find("div", {"class": "yazar-div"})
                else None
            )
            date_blok = username_kademe.find("a", {"title": "entry tarihi"})
            like_blok = username_kademe.find("div", {"title": "favlayanlar"})
            wiev_blok = username_kademe.find("span", {"class": "f_12"})
            up_block = username_kademe.find(
                "div", {"class": "f_12 ms-2 arti_sayi arti_area"}
            )

            if up_block:
                up_ = up_block.text
            else:
                up_ = "0"

            if wiev_blok:
                wiev = wiev_blok.text.strip()
            else:
                wiev = "0"

            if like_blok:
                if isinstance(like_blok, int):
                    like = like_blok.text.strip()
                else:
                    like = "0"
            else:

                like = "0"
            if date_blok:
                date = date_blok.text.strip()

            if user and username:
                self.counter += 1
                yorum_listesi.append(
                    {
                        "id": id_,
                        "username": username,
                        "yorum": user.text.strip(),
                        "wiev": wiev,
                        "like": like,
                        "up": up_,
                        "date": date,
                    }
                )

        # Eğer başlık ve yorumlar varsa güncelle
        if yorum_listesi:
            if baslik in self.all_data:
                self.all_data[baslik].extend(yorum_listesi)  # Önceki listeye ekleme yap
            else:
                self.all_data[baslik] = yorum_listesi  # Yeni başlık ekle

    def to_dict(self):
        return self.all_data
