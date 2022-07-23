import mysql.connector
import re
from sklearn import tree


try:
    cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='pricecalc')
    cursor = cnx.cursor()
    query = "SELECT weight, cpu_brand, cpu_type, ram, storage, storage_type, gpu_brand, gpu_size, screen_size," \
            " price FROM laptops"
    cursor.execute(query)

    x = []
    y = []
    for item in cursor:
        x.append(item[0:9])
        y.append(item[9])
    cnx.close()
    print("\033[92mData Loaded\033[0m")
except mysql.connector.Error as err:
    print(err)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

run_program = True
while run_program:
    new_weight = input("\nWeight (KG): ")
    new_cpu_brand = input("CPU Brand (Intel/AMD): ")
    new_cpu_type = input("CPU Type (CoreIX/RyzenX/Pentium/Celeron/BristolRidge/Carrizo/StoneyRidge/QuadCore): ")
    new_ram = input("RAM (GB): ")
    new_storage = input("Storage Size (GB): ")
    new_storage_type = input("Storage Type (HDD/SSD/SSHD): ")
    new_gpu_brand = input("GPU Brand (Intel/Nvidia/AMD): ")
    new_gpu_size = input("GPU VRAM Size (GB): ")
    new_screen_size = input("Screen Size (Inch): ")

    new_weight_save = float(new_weight)
    new_ram_save = float(new_ram)
    new_storage_save = float(new_storage)
    new_gpu_size_save = float(new_gpu_size)
    new_screen_size_save = float(new_screen_size)

    # CPU Brand
    ncb = 0
    if new_cpu_brand.lower() == "intel":
        ncb = 1
    elif new_cpu_brand.lower() == "amd":
        ncb = 2
    elif new_cpu_brand.lower() != "intel" and new_cpu_brand.lower() != "amd":
        ncb = 3
    new_cpu_brand_save = float(ncb)

    # CPU Type
    nct = 0
    if new_cpu_type.lower() == "pentium":
        nct = 2
    elif new_cpu_type.lower() == "celeron":
        nct = 1
    elif new_cpu_type.lower() == "bristolridge":
        nct = 2
    elif new_cpu_type.lower() == "carrizo":
        nct = 1
    elif new_cpu_type.lower() == "stoneyridge":
        nct = 1.5
    elif new_cpu_type.lower() == "quadcore":
        nct = 3
    else:
        nct = re.sub(r'[a-zA-Z]', "", new_cpu_type)
    new_cpu_type_save = float(nct)

    # Storage Type
    nst = 0
    if new_storage_type.lower() == "hdd":
        nst = 0
    elif new_storage_type.lower() == "ssd":
        nst = 1
    elif new_storage_type.lower() == "sshd":
        nst = 2
    new_storage_type_save = float(nst)

    # GPU Brand
    ngb = 0
    if new_gpu_brand.lower() == "intel":
        ngb = 1
    elif new_gpu_brand.lower() == "nvidia":
        ngb = 2
    elif new_gpu_brand.lower() == "amd":
        ngb = 3
    new_gpu_brand_save = float(ngb)

    new_data = [[new_weight_save, new_cpu_brand_save, new_cpu_type_save, new_ram_save, new_storage_save,
                 new_storage_type_save, new_gpu_brand_save, new_gpu_size_save, new_screen_size_save]]
    answer = clf.predict(new_data)
    print(answer[0])

    c = input("\nContinue (y/n): ")
    if c == "y":
        pass
    else:
        run_program = False
