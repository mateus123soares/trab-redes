import requests
import math

def send_response_server(soma_pares,soma_impares,pi):
    url = 'http://localhost:8080/response'
    data = {
        "soma_pares":soma_pares,
        "soma_impares":soma_impares,
        "pi":pi
    }
    response = requests.post(url, json=data)

def calcular_soma_pares_impares(intervalo):
    soma_pares = 0
    soma_impares = 0
    
    for num in range(intervalo[0], intervalo[1]+1):
        if num % 2 == 0:
            soma_pares += num
        else:
            soma_impares += num
            
    return soma_pares, soma_impares

def calcular_pi(intervalo):
    soma_pi = 0
    sinal = 1
    for num in range(intervalo[0], intervalo[1]+1):
        soma_pi += sinal * (1**num / ((2 * num) - 1))
        sinal *= -1
    return soma_pi

def main():
    url = 'http://localhost:8080'
    data = {
        'teste': '1'
    }
    response = requests.post(url, json=data)
    data = response.json()
    print(data)
    if data["range"] != "empty":
        soma_pares, soma_impares = calcular_soma_pares_impares(data["range"])
        pi = calcular_pi(data["range"])
        send_response_server(soma_pares,soma_impares,pi)
    else:
        print("Finalizou")
        exit(0)

if __name__ == "__main__":
    main()