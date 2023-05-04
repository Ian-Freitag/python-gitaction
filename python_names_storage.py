from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  
  "type": "service_account",
  "project_id": "dataops-382123",
  "private_key_id": "6bafb770588bd2b3f5d9eb24124ba5b1a1bb526d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCuiOzLPv9nfxaP\nJPC4Trz3ZZ9fWhqALFFMOyLysbTTw/fTzlvZf1oaFPcq/9bFTixNiI+LtxiKEn0B\n4uMvyLS97z3KqiE6JlGTtLtl+sluJ0Elgqgtnvq+2VAsgTgTM6cl1cITtPsW6nO1\nWp49u9QpjhjceEtJMaJYziln4HuhPiZWwOSEtTIxGm6mxloupPAzu0d8YMpofPCC\nFFSA1g+ZoQ/GujcPWUlCf0fcW7gaexOgQ6rVcpOtR75nqHAHviFKT5v7LtSc5Oai\neokOf8NbAyxf4jYzi1czMaey5jEhrseGXThZyCnF6h7SrkdC9eTgzCtuAKnldB3h\nJzXARShHAgMBAAECggEAB3kJWnJqEQ5Z8usL+3gzkwwg1L5Q4CgFmxP1HRsKuP5s\n//6X5CoVu4QmSQsHMQ91yiQMsVi3jkHYZFpIi+U2B+PUa3b5UToOyBo249jnAvZf\nTbHYbYufBMjdK+qkcf4GLBKI6rsW/RYwuhUVLWN7ZAQXgGkOICYl41OAZlgwMuka\nLo2VEH0+h5SPx+WpVRoZZgvOcUVFRbjClD73Ewx2B464pXpEZAJ4BcxOx9O039hL\nie8D7NXV6BvVqAo2E/r5qgw3U85/NDtfPM+m7buMGPOz8I3sypUFfxhV7E0Gp4LB\nWpdH0HU3bpQdn8QTu2AG1GwlE7uNLxuWJfPChu5q0QKBgQDfG53mfKzhOyEDnsG8\nzGE52HOiYqwz+jHhihAoZcsZeKAcgQUmVOKLKVZ1dkYNTgUbM5HNExcGfrbqzf9U\ntrmtEJdAD2Io3l+K9W0nks8TY035MFsz0Lqw75vDlBcc34VZpnXWhwY94yTofQPO\n7/6dPGpr6yu+zzvo65x2azB1kwKBgQDIRBlbQ9psntagFk0fxwmkdizHH5INTufz\nsIf5j65aTReOtx4tiGPDXY3a9l70X5qzy+Q9YpWwxJOVwXNEuAPBriT7wmVNhnOG\nWzntIDsx1oRmb2cjLwMAwa9X7aOQpsEpgmxc66lMbdnP+19W+5YwbY2V64KK3fMe\nvYiDmlTy/QKBgAMqfykgJ8vibOuCOzmUpOSPP8TUJaFvMXoD3YrVNvabkZoV8p7C\noZxb79Am54OU0dm695yzYqZC8hGO7sqi9SuRirPsA/aUgUKVjQD8wleCFz8sAn9P\nvPZ5z/oMhe9w9JF7HTz4GYyTRpjN/VnYagKNMu1pHuvMQQtjHItJphxlAoGAVbIu\nV4t1kD14AhEI96woSCP5jUvJJ8C4KONFjFkbdrC+f+eEFl/isNr7tNLwVwoCHSYG\niO4CuB2mOdMKDEHh+aMXWFQbHU2Hadrnsry0F+N/zIWnULrxQgWfjrS15VQ2HBkf\nXbPKQlZPelxKs+H8psR6bcjVl67aNjFMlWQZLdECgYEAz6xc+A4JFnE74d+WMz43\nRiWfSjyYqUui/lvdDwDwCN8VWxNqx4htVz5xqeq7DnE8bSq3ML4GoOgRwhOorx8u\nAUvb/BhpDweehWRujQxUky8yYH5ote+aol3zvGmlW7aP3wwa+z3Y3I0b2fBZZuld\ngJToOxLWbEblJDPbLMqK6x0=\n-----END PRIVATE KEY-----\n",
  "client_email": "659957543123-compute@developer.gserviceaccount.com",
  "client_id": "106579603627942545993",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/659957543123-compute%40developer.gserviceaccount.com"
}



try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('bucket_dataops_atividade4') ### Nome do seu bucket
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
