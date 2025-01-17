import requests

url = "https://www.olx.ua/uk/list/user/YHM5/?page=2"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("olx_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
else:
    print(f"Failed to download page. Status code: {response.status_code}")
