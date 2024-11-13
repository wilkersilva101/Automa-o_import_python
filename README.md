# Importador de Registros e Perfil dos Servidores Públicos do TJPI

## Resumo do Projeto
Este projeto automatiza a importação de registros e perfis dos servidores públicos do TJPI.

## Funcionamento

1. O script acessa a planilha de importação ("Pendências Cadastro Pessoas"):
[Link para a Planilha](https://docs.google.com/spreadsheets/d/16hzIW5ImASPiEIwvzgoQfFo1y-b2nYrK9rDyK4qTWUQ/edit?gid=0#gid=0)

2. Ele verifica se há servidores aptos para importação, conferindo os seguintes requisitos:

### 1. Na aba "SERVIDORES":
- Verifica a coluna "Pendência" para a informação "Deferido".
- Verifica a coluna "Resolvido?" para a informação "Sim" ou se está vazia.
- Caso ambos os critérios sejam atendidos, os dados são importados.

### 2. Na aba "ESTAGIÁRIOS NOVOS":
- Verifica a coluna "Status" para a informação "Deferido".
- Caso esse critério seja atendido, os dados são importados.

3. Em seguida, o script acessa o sistema [pessoas.tjpi.jus.br](http://pessoas.tjpi.jus.br), realiza o login e importa os dados.

4. Execute o seguinte comando para instalar as dependências:
```bash
pip install -r requirements.txt
