# Demonstração Amazon S3 com Floci

Aplicação de linha de comando, desenvolvida em Python, que demonstra as operações principais do **Amazon S3** utilizando o simulador **Floci** e a biblioteca oficial da AWS para Python, **boto3**.

Trabalho desenvolvido para a disciplina de Computação em Nuvem, com base no simulador AWS - Floci.

## O que a aplicação faz

Um menu interativo no terminal permite executar, separadamente, as cinco operações fundamentais de um serviço de armazenamento de objetos:

1. Criar bucket
2. Enviar arquivo
3. Listar arquivos do bucket
4. Baixar arquivo
5. Excluir arquivo

Cada opção do menu chama diretamente a API do S3 (via `boto3`), simulada localmente pelo Floci — ou seja, são as mesmas chamadas que seriam feitas contra a AWS real, apenas redirecionadas para um ambiente local.

## Estrutura do projeto

```
Projeto-S3/
├── app.py              # menu principal e funções de cada operação
├── arquivos/           # arquivos disponíveis para envio (contém um exemplo)
├── downloads/          # destino dos arquivos baixados do bucket
└── requirements.txt    # dependências do projeto
```

## Pré-requisitos

- Python 3.10 ou superior
- Docker (para rodar o Floci)

## Como executar

**1. Subir o Floci (simulador da AWS):**

```bash
docker run -d --name floci -p 4566:4566 floci/floci:latest
```

**2. Criar e ativar um ambiente virtual:**

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

**3. Instalar as dependências:**

```bash
pip install -r requirements.txt
```

**4. Executar a aplicação:**

```bash
python app.py
```

## Sobre a conexão

A aplicação se conecta ao S3 simulado apontando o `boto3` para o endereço local do Floci (`http://localhost:4566`), em vez do endereço real da AWS. As credenciais de acesso são fixas e fictícias, já que o ambiente simulado não realiza autenticação real:

```python
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)
```

