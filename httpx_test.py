import httpx

client = httpx.Client(headers={"Authorization": "Bearer token123"})

response = client.get("https://httpbin.org/get")
print(response.json())

client.close()
