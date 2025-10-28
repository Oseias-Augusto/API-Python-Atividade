import re
from datetime import datetime
from PintoresFamosos import Pintores
from QuadrosFamosos import Quadros
import database
import os

database.criar_tabelas()

limpar_tela = lambda: os.system('cls' if os.name == 'nt' else 'clear')

fundo_tipo = 1
fundo_pattern = 1
fundo_espacamento = 6
fundo_espessura = 1

def desenhar_fundo(linhas=10, largura=85):
    if fundo_pattern == 1:
        pattern = "♦"
        
    elif fundo_pattern == 2:
        pattern = "•"

    elif fundo_pattern == 3:
        pattern = "☼"

    elif fundo_pattern == 4:
        pattern = "█"

    elif fundo_pattern == 5:
        pattern = "◄►"
        largura = 55

    elif fundo_pattern == 6:
        pattern = "▓"

    for i in range(linhas):
        linha = ""
        for j in range(largura):
            if fundo_tipo == 1:
                cond = (i + j) % fundo_espacamento < fundo_espessura
            elif fundo_tipo == 2:
                cond = (i-j) % fundo_espacamento < fundo_espessura
            elif fundo_tipo == 3:
                cond = j % fundo_espacamento < fundo_espessura
            elif fundo_tipo == 4:
                cond = i % fundo_espacamento < fundo_espessura
            elif fundo_tipo == 5:
                cond = (j % fundo_espacamento < fundo_espessura) or (i % fundo_espacamento < fundo_espessura)
            else:
                cond = False

            linha += pattern if cond else " "
        print(linha)
        

def linha_superior(titulo, tipoA = True):
    print("╔" + "═" * 85 + "╗")
    print("║" + titulo.center(85) + "║")
    if tipoA == True:
        print("╠" + "═" * 85 + "╣")
    else:
        None

def linha():
    print("╔" + "═" * 85 + "╗")

def linha_inferior():
    print("╚" + "═" * 85 + "╝")

def mostrar_menu():
    limpar_tela()
    desenhar_fundo(linhas=5, largura=90)
    linha_superior(" GALERIA DE ARTE VIRTUAL ")
    print("║ 1. Visualizar Pintores e Quadros".ljust(86) + "║")
    print("║ 2. Adicionar Pintores e/ou Quadros".ljust(86) + "║")
    print("║ 3. Atualizar Pintores e/ou Quadros".ljust(86) + "║")
    print("║ 4. Deletar Pintores e/ou Quadros".ljust(86) + "║")
    print("║ 5. Configurações de Estilo".ljust(86) + "║")
    print("║ 6. Sair".ljust(86) + "║")
    linha_inferior()

while True:
    mostrar_menu()
    try:
        menu = int(input("Digite o código da opção: "))
    except ValueError:
        print("⚠ Entrada inválida, tente novamente.")
        continue

    match menu:

        case 1:
            limpar_tela()
            
            linha_superior(" Pintores ", False)
            linha_inferior()
            Pintores.listar()
            
            desenhar_fundo()
            linha_superior(" Quadros ", False)
            linha_inferior()
            Quadros.listar()

            desenhar_fundo()
            linha_superior(" Opções ")
            print("║ 1. Voltar ao Menu".ljust(86) + "║")
            print("║ 0. Sair".ljust(86) + "║")
            linha_inferior()

            try:
                escolha = int(input("Escolha: "))
            except ValueError:
                print("⚠ Entrada inválida.")
                continue

            match escolha:
                case 0:
                    break
                case 1:
                    continue
                case _:
                    print("⚠ ERRO: Opção Inexistente")
                    continue
            

        case 2:
            while True:
                limpar_tela()
                linha_superior(" ADICIONAR REGISTRO ")
                print("║ 1. Adicionar Pintor".ljust(86) + "║")
                print("║ 2. Adicionar Quadro".ljust(86) + "║")
                print("║ 0. Voltar".ljust(86) + "║")
                linha_inferior()

                try:
                    escolha = int(input("Escolha: "))
                except ValueError:
                    print("⚠ Entrada inválida.")
                    continue
                    
                match escolha:
                    case 0:
                        break
                    case 1:
                    
                        obj_pintor = {
                            'nome': input("Nome do pintor: "),
                            'nacionalidade': input("Nacionalidade: "),
                            'anoNasc': input("Ano de nascimento (dd/mm/AAAA): "),
                            'anoMort': input("Ano de morte (dd/mm/AAAA): "),
                            'estilo': input("Estilo: ")
                        }

                        padrao_data = r'^\d{2}/\d{2}/\d{4}$'
                        for campo in ["anoNasc", "anoMort"]:
                            if obj_pintor[campo] and re.match(padrao_data, obj_pintor[campo]):
                                data_convertida = datetime.strptime(obj_pintor[campo], "%d/%m/%Y")
                                obj_pintor[campo] = data_convertida.strftime("%d/%m/%Y")

                        pintor = Pintores(
                            nome=obj_pintor["nome"],
                            anoMorte=obj_pintor["anoMort"],
                            anoNasc=obj_pintor["anoNasc"],
                            estilo=obj_pintor["estilo"],
                            nacionalidade=obj_pintor["nacionalidade"]
                        )
                        pintor.salvar()

                    case 2:
                        obj_quadro = {
                            'nome': input("Nome do quadro: "),
                            'anoCriacao': input("Ano de criação (dd/mm/AAAA): "),
                            'valorEstimado': input("Valor estimado: ") or None,
                            'descricao': input("Descrição: "),
                            'pintor_id': input("ID do pintor: ")
                        }

                        if obj_quadro['pintor_id'] == "":
                            obj_quadro['pintor_id'] = None
                        else:
                            obj_quadro['pintor_id'] = int(obj_quadro['pintor_id'])

                        quadro = Quadros(
                            nome=obj_quadro["nome"],
                            anoCriacao=obj_quadro["anoCriacao"],
                            valorEstimado=obj_quadro["valorEstimado"],
                            descricao=obj_quadro["descricao"],
                            pintor_id=obj_quadro["pintor_id"]
                        )
                        quadro.salvar()

                    case _:
                        print("⚠ ERRO: Opção Inexistente")
                        continue
                
                desenhar_fundo()
                linha_superior(" Opções ")
                print("║ 1. Continuar Adicionando".ljust(86) + "║")
                print("║ 2. Voltar ao Mneu".ljust(86) + "║")
                linha_inferior()

                try:
                    escolha = int(input("Escolha: "))
                except ValueError:
                    print("⚠ Entrada inválida.")
                    continue

                match escolha:
                    case 1:
                        continue
                    case 2:
                        break
                    case _:
                        print("⚠ ERRO: Opção Inexistente")
                        continue

        case 3:
            while True:
                limpar_tela()
                linha_superior(" ATUALIZAR REGISTRO ")
                print("║ 1. Atualizar Pintor".ljust(86) + "║")
                print("║ 2. Atualizar Quadro".ljust(86) + "║")
                linha_inferior()
                escolha = int(input("Escolha: "))

                if escolha == 1:
                    desenhar_fundo(5, 85)
                    Pintores.listar()
                    
                    id_pintor = int(input("ID do pintor: "))

                    nome = input("Novo nome: ")
                    nacionalidade = input("Nova nacionalidade: ") or None
                    anoNasc = input("Novo ano de nascimento: ") or None
                    anoMort = input("Novo ano de morte: ") or None
                    estilo = input("Novo estilo: ") or None

                    Pintores.atualizar(id_pintor, nome, nacionalidade, anoNasc, anoMort, estilo)

                elif escolha == 2:
                    desenhar_fundo(5, 85)
                    Pintores.listar()
                    desenhar_fundo(5, 85)
                    Quadros.listar()

                    id_quadro = int(input("ID do quadro: "))

                    nome = input("Novo nome: ")
                    anoCriacao = input("Novo ano de criação: ") or None
                    valorEstimado = input("Novo valor estimado: ")
                    descricao = input("Nova descrição: ") or None
                    pintor_id = input("Novo ID do pintor: ")
                    valorEstimado = float(valorEstimado) if valorEstimado else None
                    pintor_id = int(pintor_id) if pintor_id else None

                    Quadros.atualizar(id_quadro, nome, anoCriacao, valorEstimado, descricao, pintor_id)

                else:  
                    print("⚠ ERRO: Opção Inexistente")
                    continue

                desenhar_fundo()
                linha_superior(" Opções ")
                print("║ 1. Continuar Atualizando".ljust(86) + "║")
                print("║ 2. Voltar ao Menu".ljust(86) + "║")
                linha_inferior()

                try:
                    escolha = int(input("Escolha: ")) 
                except ValueError:
                    print("⚠ Entrada inválida.")
                    continue

                match escolha:
                    case 1:
                        continue
                    case 2:
                        break
                    case _:
                        print("⚠ ERRO: Opção Inexistente")
                        continue

        case 4:
            while True:
                limpar_tela()
                linha_superior(" DELETAR REGISTRO ")
                print("║ 1. Deletar Pintor".ljust(86) + "║")
                print("║ 2. Deletar Quadro".ljust(86) + "║")
                linha_inferior()
                escolha = int(input("Escolha: "))

                match escolha:
                    case 1:
                        desenhar_fundo()
                        linha_superior(" Pintores ", False)
                        linha_inferior()
                        Pintores.listar()

                        id_pintor = int(input("ID do pintor: "))
                        Pintores.deletar(id_pintor)

                    case 2:
                        desenhar_fundo()
                        linha_superior(" Quadros ", False)
                        linha_inferior()
                        Quadros.listar()

                        id_quadro = int(input("ID do quadro: "))
                        Quadros.deletar(id_quadro)

                    case _:
                        print("⚠ ERRO: Opção Inexistente")
                        continue
                    
                
                desenhar_fundo()
                linha_superior(" Opções ")
                print("║ 1. Continuar Deletando".ljust(86) + "║")
                print("║ 2. Voltar ao Menu".ljust(86) + "║")
                linha_inferior()

                try:
                    escolha = int(input("Escolha: "))
                except ValueError:
                    print("⚠ Entrada inválida.")
                    continue

                match escolha:
                    case 2:
                        break
                    case 1:
                        continue
                    case _:
                        print("⚠ ERRO: Opção Inexistente")
                        continue
            

        case 5:
            limpar_tela()
            linha_superior(" CONFIGURAÇÃO DO PLANO DE FUNDO ")
            print("║ 1. Diagonal(Esquerda)".ljust(86) + "║")
            print("║ 2. Diagonal(Direita)".ljust(86) + "║")
            print("║ 3. Vertical".ljust(86) + "║")
            print("║ 4. Horizontal".ljust(86) + "║")
            print("║ 5. Grade".ljust(86) + "║")
            print("║ 6. Voltar ao Menu".ljust(86) + "║")
            linha_inferior()

            escolha = int(input("Escolha o tipo de fundo: "))
            if escolha == 6: continue
            lista_tipos = [1, 2, 3, 4, 5]
            fundo_tipo = escolha if escolha in lista_tipos else 1

            desenhar_fundo()
            print("\n")
            linha_superior("Patterns", False)
            print("║ 1. ♦ | 2. • | 3. ☼ | 4. █ | 5. ◄► | 6. ▓".ljust(86) + "║")
            linha_inferior()
            escolha_pattern = int(input("Opção: "))
            patterns = [1, 2, 3, 4, 5, 6]
            fundo_pattern = escolha_pattern if escolha_pattern in patterns else 1

            desenhar_fundo()

            try:
                fundo_espacamento = int(input("Espaçamento (ex: 6): "))
                fundo_espessura = int(input("Espessura (ex: 1): "))
            except ValueError:
                print("⚠ Valores inválidos, mantendo configuração anterior.")
            
            desenhar_fundo()

            print("\nConfiguração salva! O fundo será aplicado no menu principal.")
            input("Pressione Enter para continuar...")


        case 6:
            linha_superior(" Saindo da Galeria... Até logo! ", False)
            linha_inferior()
            break

        case _:
            print("⚠ Opção inválida, tente novamente.")
