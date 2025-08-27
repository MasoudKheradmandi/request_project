import requests


def get_token_and_return(username,password):
    payload = {
        "username":username,
        "password":password
    }
    response = requests.post(url="http://2.179.194.90/signin/",json=payload)
    return response.json()['token']



print(get_token_and_return(username="josebennett",password="GO62k0Ma+$"))

