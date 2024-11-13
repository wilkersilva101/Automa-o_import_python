import sys
from import_pessoas import run_import_pessoas

def main(cpfs):
    try:
        if cpfs:  # Verifica se a lista não está vazia
            print(f"CPFs filtrados: {cpfs}")
            run_import_pessoas(cpfs)  # Executa a importação dos CPFs filtrados
        else:
            print("Nenhum CPF encontrado para importação.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cpfs = sys.argv[1:]  # Recebe os CPFs como argumentos
        main(cpfs)
    else:
        print("Nenhum CPF fornecido para importação.")