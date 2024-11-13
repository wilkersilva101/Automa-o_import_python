import schedule
import time
import subprocess
import logging
from google_api import get_filtered_cpfs

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_aplicacao():
    cpfs = get_filtered_cpfs()
    if cpfs:
        logging.info(f"CPFs filtrados: {cpfs}")
        try:
            logging.info("Iniciando a aplicação import_pessoas.py")
            result = subprocess.run(['python', 'import_pessoas.py'] + cpfs, check=True, capture_output=True, text=True)
            logging.info(f"Saída da aplicação import_pessoas.py: {result.stdout}")
            logging.info("Aplicação import_pessoas.py executada com sucesso")
        except subprocess.CalledProcessError as e:
            logging.error(f"Erro ao executar import_pessoas.py: {e}")
            logging.error(f"Saída de erro: {e.stderr}")
        except Exception as e:
            logging.error(f"Erro inesperado ao executar import_pessoas.py: {e}")
    else:
        logging.info("Nenhum CPF pronto para execução.")

# Agendar a execução a cada 4 minutos
schedule.every(4).minutes.do(run_aplicacao)

logging.info("Agendamento iniciado. O script será executado a cada 4 minutos.")

while True:
    schedule.run_pending()
    time.sleep(1)