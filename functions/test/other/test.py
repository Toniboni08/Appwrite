import requests

print(requests.get("https://67bccd83c5825af82441.appwrite.global/get_challenge", data='{"uuid": "123"}').json())