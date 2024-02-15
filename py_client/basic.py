import requests

# endpoint = "https://httpbin.org/anything"

endpoint = "http://localhost:8000/api/products/1"

get_response = requests.get(endpoint, params={"abc":123}, json={"title" : "Hello World!", "content" : "Test", "price" : 122})

# print(get_response.text)
# print(get_response.status_code)

print(get_response.json())