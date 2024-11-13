import sys
from playwright.sync_api import sync_playwright, Error
import re
import time
from google_api import get_filtered_cpfs

# Função para validar o formato do CPF
def validate_cpf(cpf):
    pattern = re.compile(r'^\d{11}$')
    return pattern.match(cpf) is not None

def run_import_pessoas(cpfs):
    # Filtrar CPFs válidos
    valid_cpfs = [cpf for cpf in cpfs if validate_cpf(cpf)]

    if valid_cpfs:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # headless=False para ver o navegador em ação
            page = browser.new_page()

            try:
                page.goto('https://pessoas.tjpi.jus.br/')
                print("Página de login carregada.")

                # Preencher o campo de usuário
                page.fill('//*[@id="user_login"]', 'wilker.silva')
                print("Usuário preenchido.")

                # Preencher o campo de senha
                page.fill('//*[@id="user_password"]', 'EAgames2019')
                print("Senha preenchida.")

                # Clicar no botão "Entrar"
                page.click('xpath=//input[@type="submit" and @name="commit"]')
                print("Botão de login clicado.")

                # Navegar para a página de importações
                page.goto('https://pessoas.tjpi.jus.br/importacoes')
                print("Página de importações carregada.")

                # Cadastrar Importação
                page.click("//a[@class='btn btn-primary' and contains(text(), 'Cadastrar Importação')]")
                print("Botão de cadastrar importação clicado.")

                # Digitar o número dos CPF para importação
                cpf_string = ' '.join(valid_cpfs)
                page.fill('//*[@id="importacao_cpf_params"]', cpf_string)
                print(f"CPFs preenchidos: {cpf_string}")

                # Clicar no botão Salvar
                page.click("//input[@type='submit' and @value='Salvar' and @class='btn btn-primary']")
                print("Botão de salvar clicado.")

                # Clicar no botão Importar
                page.click("xpath=//a[@class='btn btn-primary btn-xs' and contains(text(), 'Importar')]")
                print("Botão de importar clicado.")

                # Esperar até que a importação seja concluída
                page.wait_for_selector("//button[@data-toggle='modal' and @data-target='#modal_erro_importacao_16645']")
                if page.query_selector("//button[@data-toggle='modal' and @data-target='#modal_erro_importacao_16645']"):
                    print('Importação concluída com sucesso!')
                else:
                    print('Importação concluída com erros!')

                # Esperar 3 minuto antes de fechar o navegador
                time.sleep(180)

            except Error as e:
                print(f"Ocorreu um erro durante a execução do Playwright: {e}")
            finally:
                browser.close()
    else:
        print('Nenhum CPF disponível para importação.')

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