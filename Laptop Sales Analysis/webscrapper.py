from bs4 import BeautifulSoup
import requests
import pandas as pd
import time,re
import csv


def fetch_amazon_data(page):

    def get_title(soup):

        try:
            title = soup.find("span",attrs={"id":'productTitle'}).text.strip()
        except AttributeError:
            title=""
        return title
    
    def get_price(soup):

        try:
            price = soup.find("span",attrs={"class":'a-price-whole'}).text.strip()[:-1]
        except AttributeError:
            price=""
        return price
    
    def get_rating(soup):

        try:
            rating = soup.find("span",attrs={"class":'a-icon-alt'}).text.strip()
        except AttributeError:
            rating=""
        return rating
    
    def get_brand(string):
        title = string
        regex = r"(avita|hp|asus|lenovo|dell|msi|acer|apple|infinix|samsung|microsoft|gigabyte|ultimus|thomson|chuwi|zebronics|wings|primebook|colorful|alienware|realme|warnercann|vaio|walker|axl|honor|jiobook)"
        match = re.findall(regex,title,re.I)
        return match[0] if match else ""
        
    def get_processor_brand(string):
        title = string
        regex = r"(intel|amd|mediatek|apple|qualcomm|core\s+i\d|core\s+ultra\s+\d|ryzen|axl)"
        match = re.findall(regex,title,re.I)
        return match[0] if match else ""
    
    def get_hard_size(title):

        regex1 = r"((\d+\s*(TB|GB)?\s*([a-zA-Z]+\s*)?(SSD|SDD|eMMC|HDD)))"
        regex2 = r"(([,/)(])\s*\d{3}\s*(TB|GB)\s*([,/)(]))"
        regex3=r"(([,/)(])\s*\d\s*(TB)\s*([,/)(]))"
        matches = re.findall(regex1, title,re.I)
        if matches:
            return matches[0][0]
        else:
            matches = re.findall(regex2, title,re.I)
            if matches:
                return matches[0][0]
            else:
                matches = re.findall(regex3,title,re.I)
                return matches[0][0] if matches else ""
    
    def get_ram(title):

        regex1 = r"(([,/)(\s])\s*\d+\s*(GB)?\s*([a-zA-Z0-9]+\s*)?(RAM|SDRAM|Unified Memory|DDR4|DDR5))"
        regex2=r"([,/()]\s*\d{1,2}\s*GB\s*[,/()+])"
        regex3=r"(([,/)(])\s*\d{1,2}\s*(GB)?\s*([a-zA-Z0-9]+\s*)([,/)(]))"
        matches = re.findall(regex1, title,re.I)
        if matches:
            return matches[0][0]
        else:
            matches = re.findall(regex2,title,re.I)
            if matches:
                return matches[0]
            else:
                matches = re.findall(regex3,title,re.I)
                return matches[0] if matches else ""
    
    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    url_amazon = f"https://www.amazon.in/s?k=laptop&page={page}"
    response_amazon = requests.get(url_amazon,headers=HEADERS)
    
    if response_amazon.status_code != 200:
        print(f"Failed to fetch page {page}. Status code: {response_amazon.status_code}")
        return []
    
    
    soup_amazon = BeautifulSoup(response_amazon.content,"html.parser")
    scraped_data_amazon = []
    laptop_links_amazon = soup_amazon.find_all("a",attrs={'class':'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})
    laptop_links_amazon_list=[]

    for link in laptop_links_amazon:
        laptop_links_amazon_list.append(link.get('href'))

    for link in laptop_links_amazon_list:

        print("https://www.amazon.in"+link)

        try:
            in_response_amazon = requests.get("https://www.amazon.in"+link, headers=HEADERS)
        except Exception as e:
            pass

        in_soup_amazon = BeautifulSoup(in_response_amazon.content,"html.parser")
        record_dict = {}
        title_string = get_title(in_soup_amazon)
        record_dict["Title"] = title_string
        record_dict["Price"] = get_price(in_soup_amazon)
        record_dict["Rating"] = get_rating(in_soup_amazon)
        record_dict["Brand"] = get_brand(title_string)
        record_dict["RAM"] = get_ram(title_string)
        record_dict["Processor-Brand"] = get_processor_brand(title_string)
        record_dict["Hard-Disk"] = get_hard_size(title_string)

        scraped_data_amazon.append(record_dict)
        time.sleep(1)

    return scraped_data_amazon



def fetch_flipkart_data(page):

    def get_title(soup):

        try:
            title = soup.find("span",attrs={"class":'VU-ZEz'}).text.strip()
        except AttributeError:
            title=""
        return title
   
    def get_price(soup):
        try:
            price =  soup.find("div",attrs={"class":'CxhGGd'}).text.strip()[1:]
            print(price)
        except:
            price=""
        return price
    
    def get_rating(soup):
        
        try:
            rating =  soup.find("div",attrs={"class":'XQDdHH'}).text.strip()
        except AttributeError:
            rating=""
        return rating
    
    def get_data(soup,string):
        
        try:
            tables = soup.find_all("table",attrs={"class":'_0ZhAN9'})[1]
            headers = tables.find_all("td",attrs={"class":'+fFi1w col col-3-12'})
            data = tables.find_all("td",attrs={"class":'Izz52n col col-9-12'})
            dic = {}
            for i in range(len(headers)):
                key=headers[i].text.strip().replace(" ","-")
                val =data[i].text.strip()
                dic[key]=val
            if dic["SSD"]=="No":
                dic["SSD-Capacity"]=dic["EMMC-Storage-Capacity"]
            return dic[string]
        except KeyError or IndexError or Exception as e:
            return ""
    
    def get_brand(string):
        title = string
        regex = r"(avita|hp|asus|lenovo|dell|msi|acer|apple|infinix|samsung|microsoft|gigabyte|ultimus|thomson|chuwi|zebronics|wings|primebook|colorful|alienware|realme|warnercann|vaio|walker|axl|honor|jiobook)"
        match = re.findall(regex,title,re.I)
        return match[0] if match else ""


    url_flipkart = f"https://www.flipkart.com/search?q=laptop&page={page}"
    response_flipkart = requests.get(url_flipkart,headers=HEADERS) 

    if response_flipkart.status_code != 200:
        print(f"Failed to fetch page {page}. Status code: {response_flipkart.status_code}")
        return []
    
    soup_flipkart = BeautifulSoup(response_flipkart.content,"html.parser")
    scraped_data_flipkart = []

    laptop_links_flipkart = soup_flipkart.find_all("a",attrs={'CGtC98'})
    laptop_links_flipkart_list=[]

    for link in laptop_links_flipkart:
        laptop_links_flipkart_list.append(link.get('href'))

    for link in laptop_links_flipkart_list:

        print("https://www.flipkart.com" + link)
        in_response_flipkart = requests.get("https://www.flipkart.com"+link,headers=HEADERS)
        in_soup_flipkart = BeautifulSoup(in_response_flipkart.content,"html.parser")

        record_dict = {}

        title_string = get_title(in_soup_flipkart)
        record_dict["Title"] = title_string
        record_dict["Price"] = get_price(in_soup_flipkart)
        record_dict["Rating"] = get_rating(in_soup_flipkart)

        record_dict["Brand"] = get_brand(title_string)
        record_dict["RAM"] = get_data(in_soup_flipkart,"RAM")
        record_dict["Processor-Brand"] = get_data(in_soup_flipkart,"Processor-Brand")
        record_dict["Hard-Disk"] = get_data(in_soup_flipkart,"SSD-Capacity")

        scraped_data_flipkart.append(record_dict)
        time.sleep(2)
       
    return scraped_data_flipkart
    
def save_to_csv(data, filename="laptops.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Rating","Brand","RAM","Processor-Brand","Hard-Disk"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

if __name__ == '__main__':
    
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    }

    all_data_list = []

    for page in range(1,20): 

        print(f'Fetching Page {page} from Amazon...')
        data_list_amazon = fetch_amazon_data(page)

        if not data_list_amazon:
            print("No data found on page... Stopping...")

        all_data_list.extend(data_list_amazon)
        time.sleep(1)
    
    for page in range(21,40):
        
        print(f'Fetching page {page} from Flipkart ...')
        data_list_flipkart = fetch_flipkart_data(page)

        if not data_list_flipkart:
            print("No data found on page... Stopping...")
        
        all_data_list.extend(data_list_flipkart)
        time.sleep(1)
    

    if all_data_list:
        save_to_csv(all_data_list)
        df = pd.DataFrame(all_data_list)
        print(df)



