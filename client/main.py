import requests

def main():
    url = 'http://localhost:8080'
    data = {
        'teste': '1'
    }
    response = requests.post(url, json=data)
    print(response.text)

if __name__ == "__main__":
    main()