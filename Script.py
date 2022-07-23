# import mysql.connector
import re
import requests
from bs4 import BeautifulSoup


def save_data(name, weight, cpu_brand, cpu_type, ram, storage, storage_type, gpu_brand, gpu_size, screen_size, price):
    try:
        cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='pricecalc')
        cursor = cnx.cursor()
        query = "INSERT INTO laptops (name, weight, cpu_brand, cpu_type, ram, storage, storage_type, gpu_brand, " \
                "gpu_size, screen_size, price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, weight, cpu_brand, cpu_type, ram, storage, storage_type, gpu_brand, gpu_size, screen_size, price)
        cursor.execute(query, val)
        cnx.commit()
        cnx.close()
        print("\033[92mDONE\033[0m")
    except mysql.connector.Error as err:
        print("Error acquired maybe duplicated item. Error is: ", err)


def start_data():
    try:
        cnx = mysql.connector.connect(user='root', host='127.0.0.1')
        cursor = cnx.cursor()
        query = "CREATE DATABASE IF NOT EXISTS pricecalc;"
        cursor.execute(query)
        cnx.commit()
        cnx.close()

        cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='pricecalc')
        cursor = cnx.cursor()
        query = "CREATE TABLE IF NOT EXISTS laptops
        (name nvarchar(200) primary key, weight float, cpu_brand float, " \
                "cpu_type float,ram float, storage float, storage_type float, gpu_brand float, gpu_size float, " \
                "screen_size float, price float)"
        cursor.execute(query)
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as err:
        print(err)


start_data()

for i in range(6):
    req_add_page = i + 1
    req_add = "https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno=" \
              + str(req_add_page) + "&sortby=4"
    print(req_add)
    res = requests.get(req_add)
    soup = BeautifulSoup(res.text, "html.parser")
    all_items = soup.find_all("div", attrs={"class": "c-product-box c-promotion-box js-product-box is-plp"})

    for item in all_items:
        s = re.findall(r"href=\"(.*)\" target", str(item))
        new_req_link = "https://www.digikala.com" + str(s[0])
        new_res = requests.get(new_req_link)
        new_soup = BeautifulSoup(new_res.text, "html.parser")
        new_all_items = str(new_soup.find_all("span", attrs={"class": "block"}))
        final_all_items = re.sub(r"\s", "", new_all_items)

        # Name
        find_name = str(new_soup.find_all("h1", attrs={"class": "c-product__title"}))
        item_name_find = re.findall(r'^\s*(.*)\s*$', (re.findall(r'.*\n\s*?(.*)\n.*', find_name)[0]))
        item_name_save = item_name_find[0]
        print(item_name_save)

        # Price
        find_price = str(new_soup.find_all("div", attrs={"class": "c-product__price-survey-question"}))
        item_price = re.findall(r'data-observed-price="(.*?)"', find_price)
        print("Price: " + item_price[0] + " Tomans")
        item_price_save = float(item_price[0])

        # Weigh
        item_weight = re.findall(r'spanclass="block">وزن</span>,<spanclass="block">(.*)کیلوگرم</span>',
                                 final_all_items)
        print("Weight: " + item_weight[0] + " KG")
        item_weight_save = float(item_weight[0])

        # CPU
        item_cpu_brand = str(re.findall(r'<spanclass="block">سازندهپردازنده</span>,.*">(Intel|AMD)<.*',
                                        final_all_items))
        print("CPU brand: " + item_cpu_brand)
        icb = 0
        if item_cpu_brand == "Intel":
            icb = 1
        elif item_cpu_brand == "AMD":
            icb = 2
        elif item_cpu_brand != "Intel" and item_cpu_brand != "Amd":
            icb = 3
        # print(icb)
        item_cpu_brand_save = icb

        item_cpu_type = str(re.findall(r'<spanclass="block">سریپردازنده</span>,<spanclass="block">(.*?)</span>',
                                       final_all_items))
        print("CPU type: " + item_cpu_type)
        if item_cpu_type.lower() == "pentium":
            ict = 2
        elif item_cpu_type.lower() == "celeron":
            ict = 1
        elif item_cpu_type.lower() == "bristolridge":
            ict = 2
        elif item_cpu_type.lower() == "carrizo":
            ict = 1
        elif item_cpu_type.lower() == "stoneyridge":
            ict = 1.5
        elif item_cpu_type.lower() == "quadcore":
            ict = 3
        else:
            ict = re.sub(r'[a-zA-Z]', "", item_cpu_type)
        # print(ict)
        item_cpu_type_save = (ict)

        item_cpu_model = re.findall(r'<spanclass="block">مدلپردازنده</span>,<spanclass="block">(.*?)</span>',
                                    final_all_items)
        print("CPU model: " + item_cpu_model[0])

        # item_cpu_cache = re.findall(r'>حافظهCache<.*</div></span>,<spanclass="block">(.*)مگابایت</span>',
        # final_all_items)
        # print("CPU cache: " + item_cpu_cache[0] + " MB")

        # RAM
        item_ram_type = str(re.findall(r'<spanclass="block">نوعحافظهRAM</span>,<spanclass="block">(.*?)</span>',
                                       final_all_items))
        print("RAM type: " + item_ram_type)
        irt = re.sub(r'\D', '', item_ram_type)
        # print(irt)

        item_ram = str(re.findall(r'<spanclass="block">ظرفیتحافظهRAM</span>,<spanclass="block">(.*?)گیگابایت</span>',
                                  final_all_items))
        print("RAM: " + item_ram + " GB")
        item_ram_save = item_ram

        # Storage
        item_storage = str(re.findall(r'<spanclass="block">ظرفیتحافظهداخلی</span>,<spanclass="block">(.*?)</span>',
                                      final_all_items))
        print("Storage: " + item_storage)
        ic = re.sub(r'\D', "", item_storage)
        ic_save = 0
        if not ic:
            if item_storage == "یکونیمترابایت":
                ic_save = 1536
            elif item_storage == "یکترابایت":
                ic_save = 1024
            elif item_storage == "دوترابایت":
                ic_save = 2048
        else:
            ic_save = ic
        # print(ic_save)
        item_storage_save = ic_save

        item_storage_type = str(re.findall(r'<spanclass="block">نوعحافظهداخلی</span>,<spanclass="block">(.*?)</span>',
                                           final_all_items))
        print("Storage type: " + item_storage_type)
        st = 0
        if item_storage_type == "هارددیسک":
            st = 0
        elif item_storage_type == "SSD":
            st = 1
        elif item_storage_type == "حافظه‌هایهیبریدی":
            st = 2
        # print(st)
        item_storage_type_save = float(st)

        # GPU
        item_gpu_brand = str(re.findall(r'<spanclass="block">سازندهپردازندهگرافیکی</span>,'
                                        r'<spanclass="block">(.*?)</span>', final_all_items))
        print("GPU brand: " + item_gpu_brand)
        gb = 0
        if item_gpu_brand.lower() == "intel":
            gb = 1
        elif item_gpu_brand.lower() == "nvidia":
            gb = 2
        elif item_gpu_brand.lower() == "amd":
            gb = 3
        # print(gb)
        item_gpu_brand_save = gb

        item_gpu_model = str(re.findall(r'<spanclass="block">مدلپردازندهگرافیکی</span>,<spanclass="block">(.*?)</span>',
                                        final_all_items))
        print("GPU model: " + item_gpu_model)

        item_gpu_size = str(re.findall(r'<spanclass="block">حافظهاختصاصیپردازندهگرافیکی</span>,'
                                       r''r'<spanclass="block">(.*?)</span>', final_all_items))
        print("GPU: " + item_gpu_size)
        ig = 0
        if item_gpu_size == "بدونحافظه‌یگرافیکیمجزا":
            ig = 0
        else:
            ig = re.sub(r'\D', "", item_gpu_size)
            if ig == '512':
                ig = 0.5
        # print(ig)
        item_gpu_size_save = ig

        item_screen_size = str(re.findall(r'<spanclass="block">اندازهصفحهنمایش</span>,'
                                          r'<spanclass="block">(.*?)اینچ</span>,', final_all_items))
        print("Size: " + item_screen_size + " inches")
        item_screen_size_save = item_screen_size

        item_matte = re.findall(r'<spanclass="block">صفحهنمایشمات</span>,<spanclass="block">(.*?)</span>',
                                final_all_items)
        # print("Matte: " + item_matte[0])

        item_touch = re.findall(r'<spanclass="block">صفحهنمایشلمسی</span>,<spanclass="block">(.*?)</span>',
                                final_all_items)
        # print("Touch: " + item_touch[0])

        # save_data(item_name_save, item_weight_save, item_cpu_brand_save, item_cpu_type_save, item_ram_save,
        #           item_storage_save, item_storage_type_save, item_gpu_brand_save, item_gpu_size_save,
        #           item_screen_size_save, item_price_save)

        print("\n****************************\n")
