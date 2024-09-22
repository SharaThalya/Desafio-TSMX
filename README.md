# Importação de Contratos - Documentação

Este repositório tem como objetivo importar dados dos clientes de um arquivo Excel para um banco de dados PostgreSQL, garantindo que os dados sejam validados, normalizados e inseridos corretamente, evitando duplicações com base em diversas validações.

## 🚀 Funcionalidades

- Importação dos clientes a partir de um arquivo Excel.
- Limpeza de campos, como remoção de caracteres indesejados em CPFs e CNPJs utilizando regex.
- Limpeza de telefones/celulares formatando a partir de regex conforme o padrão.
- Limpeza de e-mail utilizando regex para validar.
- Importação dos contratos de clientes a partir de um arquivo Excel.
- Validação de dados de clientes, planos, status do contrato e endereços.
- Prevenção de duplicações de contrato com base no endereço e cliente.
- Limpeza de campos, como remoção de caracteres indesejados em CEPs.
- Geração de logs para cada execução na linha de importação.

## 🛠️ Tecnologias Utilizadas

- **Python 3.12.6**
- **Pandas 2.2.2** - Para manipulação e leitura de arquivos Excel.
- **Psycopg2** - Para conexão com o banco de dados PostgreSQL.
- **Phonenumbers** - Para validação e formatação de números de telefone fixo e celulares.

## 📂 Estrutura do Projeto

📦 projeto-importacao 
    │
    ├── 📁 config 
    │   │ 
    │   └── connection.py # Script para conexão com o banco de dados
    │
    ├── 📁 data # Diretório para armazenar fontes de dados (Arquivos excel, csv).
    │
    ├── 📁 env # Diretório do ambiente virtual.
    │
    ├── 📁 logs # Diretório para armazenar logs das importações (registros e motivos).
    │ 
    ├── 📁 scripts 
    │   │ 
    │   ├── validacao.py # Funções de validação e formatação de dados 
    │   │ 
    │   ├── tratamento.py # Funções para tratamento de dados como UF, status, planos, contrato e CEP.
    │   │ 
    │   └── importacao.py # Script principal de importação.
    │ 
    ├── 📁 services # Diretório para armazenar as regras de cada objeto de importação.
    │   │ 
    │   ├── 📁 cliente_contratos.py # Regras para contratos.
    │   │ 
    │   ├── 📁 cliente_contatos.py # Regras para contatos.
    │   │
    │   ├── 📁 cliente_planos.py # Regras para planos.
    │   │
    │   └── 📁 clientes.py # Regras para clientes.
    │ 
    └── 📁 sql # Diretório para armazenar as scripts SQL.
    

 ```mermaid
graph TD;
    importacao.py-->service - cliente_contratos.py;
    importacao.py-->service - cliente_contatos.py;
    importacao.py-->service - cliente_planos.py;
    importacao.py-->service - clientes.py;
```

## ⚙️ Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/SharaThalya/Desafio-TSMX

2. **Crie um ambiente virtual e ative-o**:

    python -m venv env
    source venv/bin/activate  # Linux/Mac
    env\Scripts\activate     # 
    
3. **Instale as dependências**:

    pip install -r requirements.txt

4. **Configure as variáveis de ambiente no arquivo .env para a conexão com o banco de dados**:

    DB_HOST=localhost
    DB_NAME=seu_banco
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha

## ⚙️ Para utilizar

1. **Execute o script de importação**:

    python .\scripts\importacao.py
