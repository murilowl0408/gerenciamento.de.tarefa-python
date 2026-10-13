from datetime import datetime #importar o padrao de data

STATUS_VALIDO = ['pendente', 'em andamento', 'concluída'] #limitar as opcoes criando uma constante


def gerar_id(lista):
    if not lista: #gerar o primeiro ID
        return 1
    return max(t['id'] for t in lista) + 1 #gerar o maximo de IDs somando 1 com base no último criado


#funcao pra ver se a data esta no padrao, se nao, mostrar o erro
def validar_data(texto):
    try:
        datetime.strptime(texto, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validar_status(texto):
    return texto in STATUS_VALIDO 


#funcao para pesquisa de tarefas, e se for inexistente, nao mostrar nada
def buscar_por_id(lista, id_tarefa):
    for tarefa in lista:
        if tarefa['id'] == id_tarefa:
            return tarefa
    return None


#funcao para cadastrar a tarefa e adicionar na lista de tarefas
def cadastrar_tarefa(lista, titulo, descricao, vencimento, status='pendente'): #todas as informacoes que devem acompanhar as tarefas
    nova = {
        'id': gerar_id(lista),
        'titulo': titulo,
        'descricao': descricao,
        'vencimento': vencimento,
        'status': status,
    }
    lista.append(nova) #adicionar a nova tarefa na lista
    return nova
 
 
def listar_tarefas(lista, status=None, vencimento=None):
    resultado = lista

 #if para filtrar por status
    if status is not None:
        resultado = [t for t in resultado if t['status'] == status] 

  #if para filtrar por data de vencimento
    if vencimento is not None:
        resultado = [t for t in resultado if t['vencimento'] == vencimento]
 
    return resultado
 

 #funcao com if para atualizar apenas o que voce quer
def atualizar_tarefa(lista, id_tarefa, titulo=None, descricao=None,
                     vencimento=None, status=None):
    tarefa = buscar_por_id(lista, id_tarefa)
    if tarefa is None:
        return False
 
    if titulo is not None:
        tarefa['titulo'] = titulo
    if descricao is not None:
        tarefa['descricao'] = descricao
    if vencimento is not None:
        tarefa['vencimento'] = vencimento
    if status is not None:
        tarefa['status'] = status
 
    return True
 

 #funcao para remover tarefa
def remover_tarefa(lista, id_tarefa):
    tarefa = buscar_por_id(lista, id_tarefa)
    if tarefa is None:
        return False
 
    lista.remove(tarefa) #retirar tarefa selecionada da lista
    return True
