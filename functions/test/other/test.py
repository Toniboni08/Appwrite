import json

import requests


playerUuid = "d4bf2b5a30b94dd297ced52e4eecf245"
response = requests.get("https://67bccd83c5825af82441.appwrite.global/get_challenge", data='{"uuid": "%s"}' % playerUuid).json()

print(response)

requests.post("https://sessionserver.mojang.com/session/minecraft/join", data=json.dumps({
    "accessToken": "eyJraWQiOiJhYzg0YSIsImFsZyI6IkhTMjU2In0.eyJ4dWlkIjoiMjUzNTQyNDA4MTgyMDQ5MSIsImFnZyI6IlRlZW4iLCJzdWIiOiJkZTE1MjU0Yy0wYmYxLTQ2M2ItOTlkYy0wN2IyYjcxM2NmNDAiLCJhdXRoIjoiWEJPWCIsIm5zIjoiZGVmYXVsdCIsInJvbGVzIjpbXSwiaXNzIjoiYXV0aGVudGljYXRpb24iLCJmbGFncyI6WyJ0d29mYWN0b3JhdXRoIiwibXNhbWlncmF0aW9uX3N0YWdlNCIsIm9yZGVyc18yMDIyIiwibXVsdGlwbGF5ZXIiXSwicHJvZmlsZXMiOnsibWMiOiJkNGJmMmI1YS0zMGI5LTRkZDItOTdjZS1kNTJlNGVlY2YyNDUifSwicGxhdGZvcm0iOiJPTkVTVE9SRSIsInl1aWQiOiI3OGFjNDJiNjg1YjVkZjhjZDExZWRjMzMxMmFiOTIwYSIsIm5iZiI6MTc0MDQzMDM0NiwiZXhwIjoxNzQwNTE2NzQ2LCJpYXQiOjE3NDA0MzAzNDZ9.lYov_HG9aeHSRifejMfE7CxvxFvLznRSuAzv_wK6nOE",
    "selectedProfile": playerUuid,
    "serverId": response["serverId"]
}))


print(requests.get("https://67bccd83c5825af82441.appwrite.global/authenticate", data=json.dumps({
    "uuid": playerUuid,
    "serverId": response["serverId"]
})).json())