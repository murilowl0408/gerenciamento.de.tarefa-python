from flask import Flask, jsonify, request, render_template
import persistencia
import tarefas

app = Flask(__name__)
lista = persistencia.carregar_tarefas()


def erro(mensagem, codigo=400):
    return jsonify({"erro": mensagem}), codigo


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tarefas", methods=["GET"])
def listar():
    status = request.args.get("status") or None
    vencimento = request.args.get("vencimento") or None
    return jsonify(tarefas.listar_tarefas(lista, status, vencimento))


@app.route("/api/tarefas", methods=["POST"])
def cadastrar():
    dados = request.get_json() or {}
    titulo = (dados.get("titulo") or "").strip()
    descricao = (dados.get("descricao") or "").strip()
    vencimento = dados.get("vencimento") or ""
    status = dados.get("status") or "pendente"

    if not titulo:
        return erro("O título não pode ficar vazio.")
    if not tarefas.validar_data(vencimento):
        return erro("Data inválida. Use o formato dd/mm/aaaa.")
    if not tarefas.validar_status(status):
        return erro("Status inválido.")

    nova = tarefas.cadastrar_tarefa(lista, titulo, descricao, vencimento, status)
    persistencia.salvar_tarefas(lista)
    return jsonify(nova), 201


@app.route("/api/tarefas/<int:id_tarefa>", methods=["PUT"])
def atualizar(id_tarefa):
    dados = request.get_json() or {}
    titulo = dados.get("titulo")
    descricao = dados.get("descricao")
    vencimento = dados.get("vencimento")
    status = dados.get("status")

    if titulo is not None and not titulo.strip():
        return erro("O título não pode ficar vazio.")
    if vencimento is not None and not tarefas.validar_data(vencimento):
        return erro("Data inválida. Use o formato dd/mm/aaaa.")
    if status is not None and not tarefas.validar_status(status):
        return erro("Status inválido.")

    if not tarefas.atualizar_tarefa(lista, id_tarefa, titulo, descricao, vencimento, status):
        return erro("Tarefa não encontrada.", 404)

    persistencia.salvar_tarefas(lista)
    return jsonify(tarefas.buscar_por_id(lista, id_tarefa))


@app.route("/api/tarefas/<int:id_tarefa>", methods=["DELETE"])
def remover(id_tarefa):
    if not tarefas.remover_tarefa(lista, id_tarefa):
        return erro("Tarefa não encontrada.", 404)

    persistencia.salvar_tarefas(lista)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)