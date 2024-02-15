import requests

from getpass import getpass
username = input('Enter your username : ')
password = getpass('Enter your password : ')

auth_endpoint = "http://localhost:8000/api/auth/"

auth_response = requests.post(auth_endpoint, json={'username' : username, 'password' : password})
print(auth_response.json())


if auth_response.status_code == 200:
    token = auth_response.json()['token']
    endpoint = "http://localhost:8000/api/products/"

    headers = {'Authorization' : f'Token {token}'}

    get_response = requests.get(endpoint, headers=headers)


    print(get_response.json())