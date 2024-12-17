import requests
from django.http import JsonResponse


def run_simulation(simulation_steps: int):
    url = 'http://projects:8080/'

    payload = simulation_steps

    headers = {
        'Content-Type': 'application/json',
    }

    print(f"Sending post request to {url} with payload {payload}")
    response = requests.post(url, json=payload, headers=headers)
    print(f"response = {response}")

    if response.status_code == 200:
       return True
    else:
        return False
