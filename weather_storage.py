from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "dataops-382123",
  "private_key_id": "77424f603d3450b46f82875439f3be29090afd34",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+b+oJj4PyV5xK\n+6yM1zm2r3Csxnv5fpmcAqO92TUhMiByCu9+qOruK4sm1rmEYxPX5t0Eqw/KK7AB\nbBSieMdCitaeMhLIoTnRFIr4AnByTRfJeQRN4BEhAAUen6VuCEXOeF1HQoukKAgU\n9chxrEsilbZT0so4KHTkpj7fm+dsKhHPLNZ+dAliAutQEI517CQGgw2jQ464JTF5\nxxNBj9H0dFk6pL7hDz6b52vMt4SAKlKRohCy6SZiiuVYZj4tWKXAWThTTUQKrUFv\njp03DPXhv7+QQohB1A1lU2y/Hrp9dAEXNA/r4i2mRWmmeIwDc/BuB8+TTTRbtMjt\nkuWypv2ZAgMBAAECggEAAYg2do26RsaYKg1EydxIaVUXf7hYEn2HgFcQGKyo7gOw\neaJnY1o6C6D7jVwwYWWHqRbBI/K5XYvE7nn/X4A/wCQMTnkCKC2N4MX8yTqBy5Wd\nsaAA3hyFnsGYiPLJWq2D3EGhJHvfUjqFOB/zFSEI+LYCIcICIPoIWLeSrWtcbQUV\nDoBw43W4vIMqvQZvAS0ofdG1GXrBwW0DcZsFvn23Z+X4X9KxqZht/BYS2xCxe7EH\ns938awCK4Y94esSi77wvxGqdJlw51e6gfH962mUgdQkDMI4ZwD3XGIDNyvurQxRE\nCO09lJixYN9OKz8vzya4CzuLqKPiriu0igvCNAMldQKBgQDyxXwfP6zeycXHDVlU\n84jk0ayVEE/4wzqvFWISUyy8OyMKTbm9N856Yio1Vx8L1+uTq/S+5jzGuaScB6oh\n6FssClHqwyKcEgRW4vp7Sh4pmRZHMFsiDUr0lJs6+IBW0lthegLGXyLvncZIAcYY\n+APr4uzQmeD7spolXAEtx3zUJQKBgQDI0GXf9QtKCoI1hnx1yLYxQhfvzeSKlEjj\ncSgFLE/0xeFhee8E61zjiPmRrFDzzAwO8IKTO0Yaa6wfr5nm7DLDGUHmRwg1jON2\nkPcDCH8yKw8Uznc2dNM4c4uAqGmW5L2Hm5oo+ftXAbsyXnxI4arqeCBEriSR+OjE\n8uV5ZTqvZQKBgQDhFFl8u1NyBs44O1ccXOIJi6AfX81VTOPmmcOgS78JESbukZto\nJApqCwMpCwn8uAZwlhfGub2VXV6RTsXcxAlrbnH+X0aCPm4JhE1I6zHFzWoLPHjx\nvDNHSVQWO3j5hfQ1DqLt+hxw3e2MqyBX2/H+zBhVWqVtlmw1wPRS1kYUhQKBgCln\n1umjtA0zN3/j1/vNQ8vKTfczI+FzC8hhx5exeFcHCh64LpF8Gi4MSzE/L33lX8Mg\n0jubaCwAcYAjC/+yShEyPwVFNiscfrYu08+7S8bDXBu1Kp1+3yJvqJ8BmqvzRCUW\n72VtjeZ1w+xx0PySE1S/KiAfLAkxIoWhc7FhLwWFAoGBAMwHpHExDkBVD40U1lTu\nkrEQBklcynJT6/54nNIrxyD3lBrmaMUV61sosY/TY6gLsc2Uvej0bLoid0evCByx\nTzcKHR8RZo9iJLLQnxAXrFHhnUDEKufpqocjcN8lRDembGaXqeXTIxbLd8yBToyF\nOKdanqQhAar2SXFwcqebhkOw\n-----END PRIVATE KEY-----\n",
  "client_email": "659957543123-compute@developer.gserviceaccount.com",
  "client_id": "106579603627942545993",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/659957543123-compute%40developer.gserviceaccount.com"
}

try:
    res = requests.get(
    f'https://www.google.com/search?q=SaoPauloCidade&oq=SaoPauloCidade&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)

    print("Loading...")

    soup = BeautifulSoup(res.text, 'html.parser')

    info = soup.find_all("span", class_="LrzXr kno-fv wHYlTd z8gr9e")[0].getText()

    print(info)

    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket('weather_sp_dataops')
    blob = bucket.blob('weather_info_storage.txt')

    blob.upload_from_string(info + '\n')
    print('File uploaded.')

    with open('weather_info.txt', 'a') as f:
        f.write(info + '\n')
    print('ACABOUUU')

except Exception as ex:
    print(ex)