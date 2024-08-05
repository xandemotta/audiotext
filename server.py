from flask import Flask, request, jsonify
import secrets
import hashlib
import time

app = Flask(__name__)

# Configuração
TOKEN_EXPIRATION_TIME = 3600  # Tempo de expiração do token em segundos (1 hora)
usuarios = {
    "cliente1": {
        "senha_hash": hashlib.sha256("senha1".encode()).hexdigest(),
        "token": None,
        "token_expiration": None
    },
    "cliente2": {
        "senha_hash": hashlib.sha256("senha2".encode()).hexdigest(),
        "token": None,
        "token_expiration": None
    }
}

# Endpoint para login e geração de token
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    cliente_id = dados.get('cliente_id')
    senha = dados.get('senha')
    
    if cliente_id in usuarios:
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        if usuarios[cliente_id]['senha_hash'] == senha_hash:
            # Gera um novo token
            token = secrets.token_hex(16)
            token_expiration = time.time() + TOKEN_EXPIRATION_TIME
            usuarios[cliente_id]['token'] = token
            usuarios[cliente_id]['token_expiration'] = token_expiration
            return jsonify({"acesso": "permitido", "token": token})
    
    return jsonify({"acesso": "negado"}), 403

# Endpoint para verificar o status
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Servidor ativo"})

# Endpoint protegido que requer autenticação por token
@app.route('/protegido', methods=['GET'])
def protegido():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"mensagem": "Token não fornecido"}), 401

    for usuario in usuarios.values():
        if usuario['token'] == token:
            if time.time() < usuario['token_expiration']:
                return jsonify({"mensagem": "Acesso autorizado"})
            else:
                return jsonify({"mensagem": "Token expirado"}), 403
    
    return jsonify({"mensagem": "Acesso negado"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
