from .models import Exchange, UserAccess
from datetime import datetime, date, timedelta
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class ExtractBanxico():
    url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
    token = "ffad2b55961c12f1727caf1d4be124c2d375780937319d604c30b1fa29a8f9e5"

    def extract(self):
        headers = {
            "Bmx-Token": self.token,
            "Accept": "application/xml",
        }
        res = requests.get(self.url, headers=headers)
        response = {
            "success": False
        }
        if res.status_code == 200:
            response["success"] = True
            root = ET.fromstring(res.content)
            if root[0].attrib["idSerie"] == "SF43718":
                data = root[0][0]
                response["dato"] = float(data.find('dato').text)
                response["fecha"] = datetime.strptime(data.find('fecha').text, '%d/%m/%Y').date()
        return response

    def main(self):
        td = date.today()
        tm = td + timedelta(days=1)
        items = Exchange.objects.filter(created__range=[td, tm], origin="B").count()
        if items == 0:
            data = self.extract()
            if data["success"]:
                Exchange.objects.create(
                    origin="B",
                    value=data["dato"],
                    date=data["fecha"]
                )


class ExtractFixer():
    url = "http://data.fixer.io/api/latest?access_key=TOKEN&symbols=USD,MXN&format=1"
    token = "3940be2396d3207a63c122a3c7971dd9"

    def extract(self):
        url = self.url.replace("TOKEN", self.token)
        res = requests.get(url)
        response = {
            "success": False
        }
        if res.status_code == 200:
            response["success"] = True
            data = res.json()
            response["dato"] = data["rates"]["MXN"] / data["rates"]["USD"]
            response["fecha"] = datetime.strptime(data["date"], '%Y-%m-%d').date()
        return response

    def main(self):
        td = date.today()
        tm = td + timedelta(days=1)
        items = Exchange.objects.filter(created__range=[td, tm], origin="F").count()
        if items == 0:
            data = self.extract()
            if data["success"]:
                Exchange.objects.create(
                    origin="F",
                    value=data["dato"],
                    date=data["fecha"]
                )

class ExtractDiario():
    url = "https://www.banxico.org.mx/tipcamb/tipCamMIAction.do"        

    def extract(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'lxml')
        item = soup.find('table', border='0', cellpadding='0', cellspacing='0', align='center')
        if item:
            lines = item.find_all("tr")[3:]
            for line in lines:
                cols = line.find_all("td")
                val = cols[1].text.strip()
                if val not in ["N/E", ""]:
                    return {
                        "success": True,
                        "dato": float(val),
                        "fecha": datetime.strptime(cols[0].text.strip(), '%d/%m/%Y').date()
                    }
        return {
            "success": False
        }

    def main(self):
        td = date.today()
        tm = td + timedelta(days=1)
        items = Exchange.objects.filter(created__range=[td, tm], origin="D").count()
        if items == 0:
            data = self.extract()
            if data["success"]:
                Exchange.objects.create(
                    origin="D",
                    value=data["dato"],
                    date=data["fecha"]
                )
