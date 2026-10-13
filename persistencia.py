import json #para transformar em texto e salvar
import os #confirmar se o arquivo existe

ARQUIVO = 'tarefas.json'


def salvar_tarefas(lista_tarefas):
    with open(ARQUIVO, 'w', encoding='utf-8') as arquivo: #abre o arquive em escrita(w) e o utf serve para considerar acentos e ç
        json.dump(lista_tarefas, arquivo, indent=4, ensure_ascii=False)
        #escreve a lista no arquivo, indent4 serve para deixar organizado



def carregar_tarefas():
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as arquivo: #r abre o arquivo para leitura
            dados = json.load(arquivo)
    except json.JSONDecodeError:#evita de ter arquivo json quebrado ou vazio
        return []
    
    if not isinstance(dados, list):#checagem extra se esta ttudo certo
        return []

    return dados

