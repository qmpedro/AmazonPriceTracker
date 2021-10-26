import urllib.request
import bs4
import datetime
import json

# --------------- parameters
fileName_dataJson = "productdata.json"
fileName_report = "REPORT.txt"
productsUrl = [
    "https://www.amazon.com.br/dp/1736633309/?coliid=I4E6H92J2QW34&colid=3C0KAOLA2IUR8&psc=1&ref_=lv_ov_lig_dp_it",
    "https://www.amazon.com.br/dp/111969129X/?coliid=I32052DOE2YEY8&colid=3C0KAOLA2IUR8&psc=1&ref_=lv_ov_lig_dp_it",
    "https://www.amazon.com.br/dp/8577534189/?coliid=I3KG3VVX7DSOVZ&colid=3C0KAOLA2IUR8&psc=1&ref_=lv_ov_lig_dp_it"
]

for productUrl in productsUrl:
    # --------------- Get infos from amazon page
    response = urllib.request.urlopen(productUrl)
    myBytes = response.read()
    htmlText = myBytes.decode("utf8","strict")
    response.close()

    soup = bs4.BeautifulSoup(htmlText, 'html.parser')

    if soup.find("span", {"class": "a-size-base a-color-price a-color-price"}):
        title = soup.find("span", {"id": "productTitle"}).text.strip()
        price = soup.find("span", {"class": "a-size-base a-color-price a-color-price"}).text.strip()
        dateToday = datetime.datetime.now().strftime("%x")

        # --------------- Create a product object
        snapshotProduct = {
            "Title": title,
            "Price": price,
            "DateTime": dateToday
        }

        # --------------- Read file and convert to json object
        contentFile = open(fileName_dataJson, "r")
        jsonProducts = json.loads(contentFile.read())
        contentFile.close()

        # --------------- Append a new object in json and Sort products by Title, Date
        jsonProducts["products"].append(snapshotProduct)
        jsonProducts["products"].sort(key=lambda x: (x["Title"], x["DateTime"]))

        # --------------- Rewrite on file with new product sorted
        f = open(fileName_dataJson, "w")
        f.write(json.dumps(jsonProducts))
        f.close()

        # --------------- Write report file
        f = open(fileName_report, "w")
        for line in jsonProducts["products"]:
            f.writelines(line["Title"] +" | "+ line["Price"] +" | "+ line["DateTime"]+ "\n")
        f.close()


        print(title+" updated")

    else:
        print("Error: This product have no price")