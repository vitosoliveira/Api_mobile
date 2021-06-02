from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

produtos = [{"id": e, "nome": "Produto "+str(e), "receita":"Receita "+str(e), "foto":"https://www.daninoce.com.br/wp-content/uploads/2017/10/dani-noce-bolo-brigadeiro-morango-imagem-destaque-960x625.jpg", "valor": "Valor "+str(e)} for e in range(1,11)]   

@app.route("/produtos", methods=['GET'])
def get():
    return jsonify(produtos)

@app.route("/produtos/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in produtos if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/produtos", methods=['POST'])
def post():
    global produtos
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in produtos]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        produtos.append(content)
        return jsonify({"status":"OK", "msg":"produtos adicionada com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/produtos/<int:id>", methods=['DELETE'])
def delete(id):
    global produtos
    try:
        produtos = [e for e in produtos if e["id"] != id]
        return jsonify({"status":"OK", "msg":"produtos removida com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	d = random.choice(produtos)
	data = {
		"to": token,
		"notification" : {
			"title":d["nome"],
			"body":"Você tem nova receita em "+d['nome']
		},
		"data" : {
			"receitaID":d['id']
		}
	}
	req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key='+key)
	jsondata = json.dumps(data)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	print(response)
	return jsonify({"status":"OK", "msg":"Push enviado"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')