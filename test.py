import requests
response = requests.get("https://api.thecatapi.com/v1/breeds")
print(response.text)