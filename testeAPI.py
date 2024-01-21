import requests
import json

url = f"https://demofunctionappstorage.azurewebsites.net/api/fn_http_trigger?cep=12246-875"

response = requests.get(
    url = url
)

print("Status Code:", response.status_code)
print(json.dumps(json.loads(response.content),indent=4))