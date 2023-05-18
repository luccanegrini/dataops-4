from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict ={
  "type": "service_account",
  "project_id": "coastal-cascade-384922",
  "private_key_id": "a745a5521537eaea31de011df45f4331db2d9eb3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC1c0NIDAsJpZTz\neUy/COyze2fCc8smrCEaXqgBG4dnSj9UPj4orba19miAqoxCr8PMl0/h5mr7qtu1\nacASE6aN/7avqrZQPpSkyBE+x9Xgdv7/NHlmUTEpY3gqbqDeqUxhj7KXtcb/1ldY\npoAXyZdFRw74wj9aEzmRj/ED8/ez5nKebB64ENLRSATvqnDCrW9saqQyTUOIRB5P\nDpkaZ71q82RBFclvxfR6xBUd+pHF6+A4+N7eeY6hxrfrpLIWpUdEcbLOK5Ap1nKo\n3lV6opjFKf+S3rG74ElYh267pYepOfYh3qtOaPgs4P9f53xflBHLK6iJ1/DGW6vs\n8VM8xGo/AgMBAAECggEACxgUCgiqeBmGpOhKt/dsuYCXFH2N8zxc/cbB0OeE/Ny+\nSIFRvZz5aeC5/PvwfXdPqmep+67h5adJrarckn5fFZmH6u+uG/PnlLeizkrbmdDM\nwH/N2GKoddZeF4ISFesV/3UQv1Pe6e+KAaKUfF/X/uVcVftSckhwoaTCYLJ+96HJ\nqzs09WHtLX3Rw/GFjHdFWZ1Db+v6ZUATj9iiuix/pFs5nPEV+ZGfYn+p2asg9OQp\nEIENgEJblHkPE8BhU2SSQ9DQyYRWkfZhJzfu30gf7lWOJlovy/UNacRDutfQjVqU\nyqVF3mOLimKLddEYt5lBlTBpXFA/dA1QDLzG+JJJcQKBgQD/+xnAh8gQQqC70NFm\nJ4ErXdMqWHDZwT6NXQzqBC/LtMV5EnRxz3GAEKwtterB4yk88rNI90SZWD8v74eU\nLDVR3U0e3TG+xVeZ3TQnhev4PY6Ti1HFo2WcbmPcm7y90296bLICApdPk1iHZNfv\nCxJiedlaOndPmYctroxvFeVgmQKBgQC1drxYqBT5icxTCc9tQBRygtQ6+SPBi5NY\nmdQH96phNK+9z5V248H2Spfp4H4LC4N0h584ai/LIcAJf5EBTvCmu1emYj3acgsC\nmqgxdL7a5OqtIzFMC+ciSe2NtaDjkkCqx2DjlXSkUt4GXUkEb+qT4ZTXn5UIZjdz\nD2Ipo9HwlwKBgG6dc2NfSXS9VffTJKmgKJE02itSTHHMr9smeo4lgQHl++91qhwE\nKGfOzJh0JB3kq81Kk27UazBYkfWE7HF7KQ9XMhxEOVrWrCQxEniBxpZfA11+trdR\nBHe0vDJ4mfbthx7AGawEsp4QbhET4rvJbQhg3yu+WBBtp5x18PmP3K8BAoGAWJ+X\nltjn/YMeBgQJiPq9wbtBeVfJ7bGEEcZ29jkvve+kUNg7z+emB+ogTTm1dSF3XwcJ\nbNz3YIaoKjtiDziFcXiXcwwR10jRNcFgmV7CA1e/gTVp0xERHf7rBMWKwPnhmUZs\nfFm2sLZD9unCSmd6MiT+s1wdxg9dz1TZBSsb0hsCgYEA5X4ssGuJwlUixMhCdeeR\nAA0XP4dK2/1vxmEEqGv2+2duNCppiak9mdC2N8HmIVRhP81kvJ/mWUv+ZXOji3Fp\nzZrJnVByVsYMKWq2Utnh/iaIkAXs19yg6bt13KPxxsEmwCl8evwSFYBl5Z6DW6O4\nrfpkxElQyO1hSdbQ5LzTOxI=\n-----END PRIVATE KEY-----\n",
  "client_email": "575872358278-compute@developer.gserviceaccount.com",
  "client_id": "101424858554171284489",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/575872358278-compute%40developer.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('dataops-4') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
