import json
import requests


def Download():
    #url = "https://www.olx.ua/uk/list/user/YHM5/?page=1"
    url = "https://bovi.olx.ua/uk/home/elektronika/"

    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open("olx_page.html", "w", encoding="utf-8") as file:
            file.write(response.text)
    else:
        print(f"Failed to download page. Status code: {response.status_code}")

def Read():
  File = 'olx_page.html.json'
  with open(File, 'r', encoding='utf-8') as F:
    raw_data = F.read()

  #cleaned_data = raw_data.encode('utf-8').decode('unicode_escape')
  #cleaned_data = raw_data.encode('utf-8').decode()
  cleaned_data = raw_data.replace(r'\"', '"').replace(r'\\', '\\')

  try:
    json_data = json.loads(cleaned_data)
    Data = json.dumps(json_data, indent=2, ensure_ascii=False)
    with open(File + '_2', 'w', encoding='utf-8') as F:
      F.write(Data)

    with open(File + '_1', 'w', encoding='utf-8') as F:
      F.write(cleaned_data)

  except json.JSONDecodeError as e:
    print("Failed to parse JSON:", e)

#Download()
Read()
