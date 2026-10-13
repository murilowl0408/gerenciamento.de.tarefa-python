# Sistema de Gerenciamento de Tarefas

  
Sistema em Python para cadastrar, listar, filtrar, editar e excluir tarefas. Os dados ficam salvos em `tarefas.json`.

Tem duas interfaces: **web (Flask)** e **terminal**.

## Funcionalidades

* Cadastrar tarefa (título, descrição, vencimento e status)
* Listar e filtrar por status ou data de vencimento
* Editar tarefa e alterar o status
* Excluir tarefa
* Salvar e carregar automaticamente

## Estrutura

```
├── app.py            # Interface web (Flask)
├── interface.py      # Interface de terminal
├── tarefas.py        # Regras do sistema
├── persistencia.py   # Salvar e carregar o JSON
├── templates/
│   └── index.html    # Página web
└── static/
    └── style.css     # Estilo da página
```

## Como executar

**Web**

```bash
pip install flask
python3 app.py
```

Abra http://127.0.0.1:5000 no navegador.

**Terminal**

```bash
python3 interface.py
```

## Integrantes
* Murilo Wengrzynek Leitão RM575401

