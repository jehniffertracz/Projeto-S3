"""
Demonstração das operações principais do Amazon S3
utilizando o simulador Floci e a biblioteca boto3.

Operações implementadas: criar bucket, enviar arquivo,
listar arquivos, baixar arquivo e excluir arquivo.
"""

import os
import boto3

# Conexão com o S3 simulado (Floci)
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

NOME_BUCKET = "demo-s3-trabalho"


def bucket_existe():
    """Verifica se o bucket de demonstração já foi criado."""
    buckets = s3.list_buckets()["Buckets"]
    return any(b["Name"] == NOME_BUCKET for b in buckets)


def criar_bucket():
    try:
        s3.create_bucket(Bucket=NOME_BUCKET)
        print(f"\nBucket '{NOME_BUCKET}' criado com sucesso!\n")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"\nO bucket '{NOME_BUCKET}' já existe, não é necessário criar novamente.\n")


def enviar_arquivo():
    if not bucket_existe():
        print("\nO bucket ainda não foi criado. Use a opção 1 antes de enviar arquivos.\n")
        return

    nome_arquivo = input("Digite o nome do arquivo (dentro da pasta 'arquivos/'): ")
    caminho_local = f"arquivos/{nome_arquivo}"

    if not os.path.exists(caminho_local):
        print(f"\nErro: o arquivo '{caminho_local}' não foi encontrado.\n")
        return

    tamanho = os.path.getsize(caminho_local)
    print(f"Enviando '{nome_arquivo}' ({tamanho} bytes)...")

    s3.upload_file(caminho_local, NOME_BUCKET, nome_arquivo)
    print(f"Arquivo '{nome_arquivo}' enviado com sucesso para o bucket!\n")


def listar_arquivos():
    if not bucket_existe():
        print("\nO bucket ainda não foi criado. Use a opção 1 primeiro.\n")
        return

    resposta = s3.list_objects_v2(Bucket=NOME_BUCKET)

    if "Contents" not in resposta:
        print("\nO bucket está vazio.\n")
        return

    print("\nArquivos no bucket:")
    for objeto in resposta["Contents"]:
        print(f"- {objeto['Key']} ({objeto['Size']} bytes)")
    print()


def baixar_arquivo():
    if not bucket_existe():
        print("\nO bucket ainda não foi criado. Use a opção 1 primeiro.\n")
        return

    nome_arquivo = input("Digite o nome do arquivo que deseja baixar: ")
    caminho_destino = f"downloads/{nome_arquivo}"

    try:
        s3.download_file(NOME_BUCKET, nome_arquivo, caminho_destino)
        print(f"\nArquivo '{nome_arquivo}' baixado com sucesso para a pasta 'downloads/'!\n")
    except Exception as erro:
        print(f"\nErro ao baixar o arquivo: {erro}\n")


def excluir_arquivo():
    if not bucket_existe():
        print("\nO bucket ainda não foi criado. Use a opção 1 primeiro.\n")
        return

    nome_arquivo = input("Digite o nome do arquivo que deseja excluir: ")

    s3.delete_object(Bucket=NOME_BUCKET, Key=nome_arquivo)
    print(f"\nArquivo '{nome_arquivo}' excluído do bucket!\n")


def menu():
    while True:
        print("=================================")
        print(" Demonstração Amazon S3 - Floci")
        print("=================================")
        print("1 - Criar Bucket")
        print("2 - Enviar Arquivo")
        print("3 - Listar Arquivos")
        print("4 - Baixar Arquivo")
        print("5 - Excluir Arquivo")
        print("6 - Sair")

        opcao = input("\nEscolha: ")

        if opcao == "1":
            criar_bucket()
        elif opcao == "2":
            enviar_arquivo()
        elif opcao == "3":
            listar_arquivos()
        elif opcao == "4":
            baixar_arquivo()
        elif opcao == "5":
            excluir_arquivo()
        elif opcao == "6":
            print("\nEncerrando aplicação...")
            break
        else:
            print("\nOpção inválida, tente novamente.\n")


if __name__ == "__main__":
    menu()