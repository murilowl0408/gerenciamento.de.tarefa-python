import subprocess
import persistencia
import tarefas


#funcao pra depois de rodar o comando, limpar a tela
def limpar_tela():
    subprocess.run('clear')


def exibir_nome_programa():
    print('Gerencie suas tarefas\n') #mostrar o titulo do programa


#funcao que lista as opcoes que terá na interface
def exibir_opcoes():
    print('1. Cadastrar tarefa')
    print('2. Listar tarefas')
    print('3. Atualizar tarefa')
    print('4. Excluir tarefa')
    print('5. Sair\n')


#fins esteticos, mostra o subtitulo da pagina que voce ta
def exibir_subtitulos(texto):
    limpar_tela()
    linha = '*' * len(texto) #cria uma caixinha ao redor do subtitulo com asteriscos
    print(linha)
    print(texto)
    print(linha)
    print()

#funcao que recebe a lista de tarefas e organizar por linhas
def exibir_tarefas(lista):
    if not lista:
        print('Nenhuma tarefa encontrada.')
        return
#ljust sao para fins esteticos, preenche a linha e deixa as colunas alinhadas
    print(f'{"ID".ljust(4)} | {"Título".ljust(20)} | {"Descrição".ljust(25)} | '
          f'{"Vencimento".ljust(12)} | Status')
    print('-' * 85)
    for t in lista:
        print(f'{str(t["id"]).ljust(4)} | {t["titulo"].ljust(20)} | '
              f'{t["descricao"].ljust(25)} | {t["vencimento"].ljust(12)} | {t["status"]}')


#funcao para voltar ao menu depois de realizar uma das opcoes
def voltar_ao_menu_principal():
    input('\nPressione Enter para voltar ao menu principal...')


#funcao para todas opcoes invalidas
def opcao_invalida():
    print('Esta opção é inválida!')
    voltar_ao_menu_principal()

#funcao pra fechar o sistema
def finalizar_sistema():
    exibir_subtitulos('Finalizando o app')

#funcao para ver se a data esta no padrao
def ler_data(mensagem, permitir_vazio=False):
    while True:
        texto = input(mensagem).strip()
        if permitir_vazio and texto == '':
            return None
        if tarefas.validar_data(texto): #se nao estiver no padrao, printar data invalida, e mostrar o padrao
            return texto
        print('Data inválida! Use o formato dd/mm/aaaa.')


#funcao pra validar os status
def ler_status(mensagem, permitir_vazio=False):
    while True:
        texto = input(mensagem).strip().lower()
        if permitir_vazio and texto == '':
            return None
        if texto == 'concluida':
            texto = 'concluída'
        if tarefas.validar_status(texto):
            return texto
        print('Status inválido! Use: pendente, em andamento ou concluída.')#caso o user erre, printar as opcoes certas


def ler_id(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        print('O id precisa ser um número.')
        return None


#funcao para cadastrar tarefa, um campo para cada info da tarefa
def menu_cadastrar(lista):
    exibir_subtitulos('Cadastro de novas tarefas')

    titulo = input('Digite o título da tarefa: ').strip()
    descricao = input('Digite a descrição da tarefa: ').strip()

    if not titulo:
        print('O título não pode ficar vazio.')
        voltar_ao_menu_principal()
        return

    vencimento = ler_data('Digite a data de vencimento (dd/mm/aaaa): ')
    status = ler_status('Digite o status (pendente, em andamento ou concluída): ')

    tarefas.cadastrar_tarefa(lista, titulo, descricao, vencimento, status)
    persistencia.salvar_tarefas(lista)

    print(f'\nA tarefa "{titulo}" foi cadastrada com sucesso!')
    voltar_ao_menu_principal()

#funcao para pergunatar o que voce quer filtrar da lista
def menu_listar(lista):
    exibir_subtitulos('Listando as tarefas')

    print('1. Ver todas')
    print('2. Filtrar por status')
    print('3. Filtrar por data de vencimento\n')
    escolha = input('Escolha uma opção: ').strip()

    if escolha == '1':
        resultado = tarefas.listar_tarefas(lista)
    elif escolha == '2':
        status = ler_status('Qual status? (pendente, em andamento ou concluída): ')
        resultado = tarefas.listar_tarefas(lista, status=status)
    elif escolha == '3':
        data = ler_data('Qual data? (dd/mm/aaaa): ')
        resultado = tarefas.listar_tarefas(lista, vencimento=data)
    else:
        opcao_invalida()
        return

    print()
    exibir_tarefas(resultado)
    voltar_ao_menu_principal()


#separar por campos diferentes, pra atualizar uma parte só da tarefa
def menu_atualizar(lista):
    exibir_subtitulos('Atualizando uma tarefa')

    exibir_tarefas(lista)
    if not lista:
        voltar_ao_menu_principal()
        return

    print()
    id_tarefa = ler_id('Digite o id da tarefa que deseja atualizar: ')
    if id_tarefa is None:
        voltar_ao_menu_principal()
        return

    if tarefas.buscar_por_id(lista, id_tarefa) is None: #se nao encontrar a tarefa, printar nao encontrada
        print('Tarefa não encontrada.')
        voltar_ao_menu_principal()
        return

    print('\nDeixe em branco (Enter) para manter o valor atual.\n')
    titulo = input('Novo título: ').strip() or None
    descricao = input('Nova descrição: ').strip() or None
    vencimento = ler_data('Nova data de vencimento (dd/mm/aaaa): ', permitir_vazio=True)
    status = ler_status('Novo status (pendente, em andamento ou concluída): ',
                        permitir_vazio=True)

    tarefas.atualizar_tarefa(lista, id_tarefa, titulo, descricao, vencimento, status)
    persistencia.salvar_tarefas(lista)#adicionar a lista as atualizacoes

    print('\nTarefa atualizada com sucesso!')
    voltar_ao_menu_principal()


#funcao de remocao da tarefa, na interface do sistema
def menu_remover(lista):
    exibir_subtitulos('Excluindo uma tarefa')

    exibir_tarefas(lista)
    if not lista:
        voltar_ao_menu_principal()
        return

    print()
    id_tarefa = ler_id('Digite o id da tarefa que deseja excluir: ') #selecionar a tarefa que deseja exxcluir com id
    if id_tarefa is None:
        voltar_ao_menu_principal()
        return

    confirmar = input('Tem certeza? (s/n): ').strip().lower()
    if confirmar != 's':
        print('Exclusão cancelada.') #confirmar ou nao a remocao da tarefa, com input
        voltar_ao_menu_principal()
        return

    if tarefas.remover_tarefa(lista, id_tarefa):
        persistencia.salvar_tarefas(lista)
        print('Tarefa excluída com sucesso!')
    else:
        print('Tarefa não encontrada.')

    voltar_ao_menu_principal()


#o motor do sistema, leva o user para a pagina selecionada, atraves do numero clicado
def main():
    lista = persistencia.carregar_tarefas()

    while True:
        limpar_tela()
        exibir_nome_programa()
        exibir_opcoes()
        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            menu_cadastrar(lista)
        elif opcao == '2':
            menu_listar(lista)
        elif opcao == '3':
            menu_atualizar(lista)
        elif opcao == '4':
            menu_remover(lista)
        elif opcao == '5':
            finalizar_sistema()
            break
        else:
            opcao_invalida()


if __name__ == '__main__':
    main()