import requests

def testar_acesso():
    url = 'http://localhost:5000/verificar_acesso'
    dados = {
        "cliente_id": "cliente1",
        "senha": "senha1"
    }
    resposta = requests.post(url, json=dados)
    print(resposta.json())

testar_acesso()
