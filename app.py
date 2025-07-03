
from flask import Flask, request, jsonify
from flask_cors import CORS 
app = Flask(__name__)
CORS(app) 

# Dados da cidade: valor e tipo de cobrança
dados_vale = {
    ("Juiz de Fora", "MG"): {"valor": 3.75, "tipo": "por entrada"},
    ("Belo Horizonte", "MG"): {"valor": 5.75, "tipo": "por entrada"},
    ("Rio de Janeiro", "RJ"): {"valor": 8.80, "tipo": "por entrada"},
    ("São Paulo", "SP"): {"valor": 5.49, "tipo": "diário"},
    ("Vitória", "ES"): {"valor": 4.90, "tipo": "diário"}
}

@app.route('/calcular', methods=['GET'])
def calcular_vale():
    cidade = request.args.get('cidade')
    estado = request.args.get('estado')
    vales_por_dia = request.args.get('vales_por_dia', type=int)
    dias_trabalhados = request.args.get('dias_trabalhados', type=int)

    if not cidade or not estado or dias_trabalhados is None:
        return jsonify({"erro": "Parâmetros obrigatórios: cidade, estado, dias_trabalhados"}), 400

    chave = (cidade, estado)
    info = dados_vale.get(chave)

    if not info:
        return jsonify({"erro": "Cidade ou estado não encontrados"}), 404

    valor_unitario = info["valor"]
    tipo = info["tipo"]

    if tipo == "por entrada":
        if vales_por_dia is None:
            return jsonify({"erro": "vales_por_dia é obrigatório para cidades com cobrança por entrada"}), 400
        total = valor_unitario * vales_por_dia * dias_trabalhados
    else:
        total = valor_unitario * dias_trabalhados

    return jsonify({
        "cidade": cidade,
        "estado": estado,
        "tipo_cobranca": tipo,
        "valor_unitario": valor_unitario,
        "vales_por_dia": vales_por_dia if tipo == "por entrada" else None,
        "dias_trabalhados": dias_trabalhados,
        "total": round(total, 2)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import send_from_directory
import os

@app.route('/')
def homepage():
    return send_from_directory(os.getcwd(), 'index.html')


