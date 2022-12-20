import pickle 
import random
import psycopg2

def testConnection():
    conexao = None
    try:
        con = psycopg2.connect(host='db.tqtklivytnrncchboxnp.supabase.co', database='postgres',
        user='postgres', password='NappAcademy2022*')
        return True
    except:
        return False

def openConnectionDB():
    try:
        con = psycopg2.connect(host='db.tqtklivytnrncchboxnp.supabase.co', database='postgres',
        user='postgres', password='NappAcademy2022*')
        
        cur = con.cursor()
        return con, cur
    except:
        print("Conexão com o banco falhou")

def retornaFigurinhas():
    
    lista = []
    con, cur = openConnectionDB()
    print(con)
    print(cur)
    cur.execute('select posicao_figurinha from figurinhas where adquirida = true order by posicao_figurinha')
    recset = cur.fetchall()

    if len(recset) == 0:
        print('Você ainda não possui figurinhas. Abra um pacotinho')
    else:
        for item in recset:
            lista.append(item[0])
    cur.close()
    con.close()
    return lista
    
def retornaFigurinhasRepetidas():
    lista = []
    con, cur = openConnectionDB()
    cur.execute('select posicao_figurinhas_repetidas from figurinhas_repetidas where quantidade > 0 order by posicao_figurinhas_repetidas')
    recset = cur.fetchall()
    if len(recset) == 0:
            print("Sem figurinhas repetidas")
    else:
        for item in recset:
            lista.append(item[0])
    cur.close()
    con.close()
    return lista

def retornaFaltantes():
    lista = []
    con, cur = openConnectionDB()
    cur.execute('select posicao_figurinha from figurinhas where adquirida = false order by posicao_figurinha')
    recset = cur.fetchall()
    if len(recset) == 0:
        print("Sem figurinhas faltantes")
    else:
        for item in recset:
            lista.append(item[0])
    cur.close()
    con.close()
    return lista

def trocaDeFigurinhas():
    clear()
    repetidas = retornaFigurinhasRepetidas()
    print('Você está na troca de figurinhas...')
    print(f'Lembrando, essas são as suas figurinhas repetidas: {repetidas}')

    figTroca = int(input('Digite o número da figurinha repetida desejada para a troca: '))

    if figTroca in repetidas:
        lista = retornaFaltantes()
        if len(lista) == 0:
            pass
        else:
            #Gerando um random a partir das figurinhas faltantes do album
            escolhida = random.choice(lista)

            con, cur = openConnectionDB()

            #Atualizando a quantidade da figurinha escolhida pelo usuário (quantidade-1)
            cur.execute('select quantidade from figurinhas_repetidas where posicao_figurinhas_repetidas = %s', [figTroca])
            quantidade = cur.fetchone()
            quantidade_atualizada = quantidade[0]-1
            cur.execute('UPDATE figurinhas_repetidas SET quantidade = %s WHERE posicao_figurinhas_repetidas = %s', [quantidade_atualizada, figTroca])
            con.commit()
            print(f'Foi removida uma figurinha do seu monte {figTroca}')

            #Colando figurinha gerada pelo random no álbum
            print(f'Nova figurinha adquirida! A figurinha: {escolhida} foi inserida no álbum.')
            cur.execute('UPDATE figurinhas SET adquirida = true WHERE posicao_figurinha = %s', [escolhida])
            con.commit()
            con.close()
    else:
        print('Não existe essa figurinha no seu monte de repetidas')

def clear():
    import os

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def menu():
    print(
    '''
    [ 1 ] - Abrir pacote de figurinhas
    [ 2 ] - Relatórios
    [ 3 ] - Troca de Figurinhas
    [ 4 ] - Sair
    [ 5 ] - Limpar album
    '''
    )

    opcao = int(input("Escolha uma opção: "))
    return opcao

def abrirPacote():
    clear()
    print('''
    Voce ganhou 5 figurinhas. Parabens!
    ''')
    lista = []
 
    res = [random.randrange(1, 670, 1) for i in range(5)]

    print("As figurinhas do pacotinho são : " +  str(res))
    
    con, cur = openConnectionDB()

    cur.execute('select posicao_figurinha from figurinhas where adquirida = true')
    recset = cur.fetchall()

    if len(recset) == 0:
        for r in res:
            print(f'Nova figurinha adquirida! A figurinha: {r} foi inserida no álbum.')
            cur.execute('UPDATE figurinhas SET adquirida = true WHERE posicao_figurinha = %s', [r])
            con.commit()
    else:
        for rec in recset:
            lista.append(rec[0])
        for r in res: 
            if r in lista:
                try:
                    cur.execute('select quantidade from figurinhas_repetidas where posicao_figurinhas_repetidas = %s', [r])
                    quantidade = cur.fetchone()
                    quantidade_atualizada = quantidade[0]+1
                    cur.execute('UPDATE figurinhas_repetidas SET quantidade = %s WHERE posicao_figurinhas_repetidas = %s', [quantidade_atualizada, r])
                    con.commit()
                    print(f'Figurinha repetida... A figurinha: {r} foi incrementada em seu monte.')
                except:
                    print('Erro ao adicionar a figurinha no monte')
            else:
                try:
                    print(f'Nova figurinha adquirida! A figurinha: {r} foi inserida no álbum.')
                    cur.execute('UPDATE figurinhas SET adquirida = true WHERE posicao_figurinha = %s', [r])
                    con.commit()
                except:
                    print('Erro ao adicionar a figurinha no álbum')

def exibirRelatorios():
    clear()
    print('''
    Opções de relatórios

    [ 1 ] - Ver figurinhas já obtidas
    [ 2 ] - Ver figurinhas faltantes
    [ 3 ] - Ver figurinhas repetidas
    [ 4 ] - Verificar UMA figurinha
    [ 5 ] - Voltar ao Menu
    ''')

    opcao = int(input("Escolha o relatório desejado: "))

    if opcao == 1:
        clear()
        print("Relatório de figurinhas já obtidas")
        recset = retornaFigurinhas()
        print(recset)
    elif opcao == 2:
        clear()
        print("Relatório de figurinhas faltantes")
        recset = retornaFaltantes()
        print(recset)
    elif opcao == 3:
        clear()
        print("Relatório de figurinhas repetidas")
        recset = retornaFigurinhasRepetidas()
        print(recset)
    elif opcao == 4:
        clear()
        print("Vamos veriricar qualquer figurinha para você...")
        verificaUma()
    elif opcao == 5:
        clear()
        print("Voltou ao Menu")
    else:
        clear()
        print("Entrada inválida! Esolha uma das opções disponíveis.\n")
        opcao = int(input("Escolha a opção desejada: "))

def verificaUma():
    entrada = int(input('Qual figurinha deseja verificar se há colada no álbum: '))
    con, cur = openConnectionDB()
    cur.execute('select adquirida from figurinhas where posicao_figurinha = %s', [entrada])
    recset = cur.fetchone()
    if len(recset) == 0:
        print("Digite uma figurinha entre 1 e 670 na próxima vez")
    else:
        if recset[0] == True:
            print('Você já possui colada essa figurinha :)')
        else: 
            print('Você não tem essa figurinha ainda :(')
            
    cur.close()
    con.close()

def limparAlbum():
    clear()
    print('''
    Você está prestes a recomeçar seu album do zero!
    Deseja mesmo excluir todas as informações antes armazenadas?

    [ 1 ] - Sim! Excluir album.
    [ 2 ] - Não! Voltar ao Menu

    ''')

    opcao = int(input("Escolha a opção desejada: "))

    if opcao == 1:
        clear()
        try:
            con = psycopg2.connect(host='db.tqtklivytnrncchboxnp.supabase.co', database='postgres',
            user='postgres', password='NappAcademy2022*')
            cur = con.cursor()
        except:
            print("Conexão com o banco falhou")

        # Zerar informações da tabela de figurinhas
        cur.execute('UPDATE figurinhas SET adquirida = false WHERE adquirida = true')
        con.commit()

        # Zerar informações da tabela de figurinhas repetidas
        cur.execute('UPDATE figurinhas_repetidas SET quantidade = 0 WHERE quantidade <> 0')
        con.commit()

        con.close()
    elif opcao == 2:
        clear()
        print("Você voltou ao Menu")
    else:
        clear()
        print("Entrada inválida! Esolha uma das opções disponíveis.\n")
        opcao = int(input("Escolha a opção desejada: "))

def sair():
    clear()
    print(
        '''
        Você fechou seu album. Todas as suas figurinhas já obtidas estão armazenadas.
        Até mais!
        '''
    )
    exit()


if __name__ == "__main__":
    clear()
    opcao = 0

    print('''
    ===============================
    Bem vindo ao seu album da copa
    ===============================
    ''')

    while opcao != 4:
        opcao = menu()
        if opcao == 1:
            abrirPacote()
        elif opcao == 2:
            exibirRelatorios()
        elif opcao == 3:
            trocaDeFigurinhas()
        elif opcao == 4:
            sair()
        elif opcao == 5:
            limparAlbum()
        else:
            clear()
            print("Opção inválida. Escolha outra opção.")
