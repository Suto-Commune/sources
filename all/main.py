import requests
import os
import json
from threading import Thread
import time
import sys


def jar():
    os.system("java -jar reader.jar")


t_reader = Thread(target=jar, args="", name="Reader")

t_reader.start()

time.sleep(30)

list1 = []


def traverse_folders(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for dirname in dirnames[:]:
            if dirname.startswith('.') or dirname == 'all':
                dirnames.remove(dirname)

        for filename in filenames:
            # 在此处执行对文件的操作
            if "source" in filename:
                list1.append(os.path.join(dirpath, filename))
                print("文件路径：", os.path.join(dirpath, filename))


# 指定要遍历的根文件夹
root_folder = '../'

# 调用遍历函数
traverse_folders(root_folder)

print(list1)
for i in list1:
    with open(i, "r+", encoding="UTF-8") as f:
        payload = f.read()
        headers = {
            'Content-Type': 'text/plain'
        }
        payload = payload.encode('UTF-8')
        response = requests.post("http://127.0.0.1:8080/reader3/saveBookSources", headers=headers, data=payload)

sources = requests.get("http://127.0.0.1:8080/reader3/getBookSources")
os.system("sudo rm -rf sources.json")
with open("sources.json", "w", encoding="UTF-8") as f:
    f.write(str(json.dumps(sources.json()["data"], indent=4, ensure_ascii=False)))

os.system("killall java")
os.system("killall python")
os.system("killall python3")
sys.exit()
