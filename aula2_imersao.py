
import boto3
import pprint
import io #manipular dados em memória como se fossem arquivos.
import pandas as pd
from sqlalchemy import create_engine

# ESTRUTURA DIDÁTICA:
# - PARTE 1.A: Ler UM Parquet do DataLake (io + boto3 + pandas)
# - PARTE 1.B: Salvar essa tabela no PostgreSQL (sqlalchemy)
# - PARTE 2:   Refatorar tudo com FOR para as 4 tabelas

# Configurações do DataLake 
S3_ENDPOINT_URL = "https://bhqrihrvphxvwqisdfyc.storage.supabase.co/storage/v1/s3"
AWS_REGION = "us-east-2"
AWS_ACCESS_KEY_ID = "a280a61182677c361a5b7e689c71c976"
AWS_SECRET_ACCESS_KEY = "b97827ee637266aa62de3b062275a7eaf1644db044d2d0db38be6d0b03315a7c"
BUCKET_NAME = "datalake_ecommerce"


# Criar cliente S3
s3 = boto3.client(
         "s3",
     region_name=AWS_REGION,
     endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
 )

# --- Teste de conexão: listar arquivos no bucket ---

# response = s3.list_objects(Bucket=BUCKET_NAME)
# arquivos = [obj["Key"] for obj in response["Contents"]]
# print("Arquivos encontrados no DataLake: ")
# print(arquivos)


# # --- Baixar o arquivo Parquet de UMA tabela (produtos) ---
# print("\n📥 Baixando produtos.parquet do DataLake...")

# file_key = "produtos.parquet"
# response = s3.get_object(Bucket=BUCKET_NAME, Key=file_key) #busca o arquivo no S3, igual a um "download"
# parquet_bytes = response["Body"].read() #lê o conteúdo do arquivo como bytes (zeros e uns crus)

# # --- Converter bytes → DataFrame ---
# df_produtos = pd.read_parquet(io.BytesIO(parquet_bytes))  #transforma os bytes num "arquivo falso" na memória
# pprint.pprint(df_produtos)
# print(f"✅ produtos: {len(df_produtos)} linhas carregadas")

# # Configurações do PostgreSQL (Supabase)

#  Configurações do PostgreSQL (Supabase)
DATABASE_URL = "postgresql://postgres.bhqrihrvphxvwqisdfyc:Fragoso2007!@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
# -----CONECTA COM O BANCO DE DADOS!!!!
engine = create_engine(DATABASE_URL)

# df_produtos.to_sql(
#     "produtos",            # Nome da tabela no banco
#     engine,                # Engine de conexão
#     if_exists="replace",   # Substituir se existir
#     index=False,           # Não salvar índice do pandas
# )

#REFORMANDO COM FOR!!!!!!!!!!!!!!

# Lista com os nomes das 4 tabelas que vamos carregar
TABELAS = ["produtos", "clientes", "vendas", "preco_competidores"]

# Dicionário vazio onde vamos guardar os DataFrames
# Chave = nome da tabela, Valor = DataFrame com os dados
dataframes = {}

for tabela in TABELAS:
    print(f"📥 Baixando {tabela}.parquet do DataLake...")

# Montar o nome do arquivo: "produtos" → "produtos.parquet"
    file_key = f"{tabela}.parquet"

 # Baixar o arquivo do S3 (mesmo código da PARTE 1.A, mas com variável)
    response = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    parquet_bytes = response["Body"].read()

# Converter bytes → DataFrame e guardar no dicionário
    dataframes[tabela] = pd.read_parquet(io.BytesIO(parquet_bytes))

    print(f"✅ {tabela}: {len(dataframes[tabela])} linhas carregadas")

# --- FOR 2: Salvar cada tabela no PostgreSQL ---

for tabela, df in dataframes.items():
    print(f"Salvando {tabela} no PostgreSQL...")

    df.to_sql(
        tabela,                # Nome da tabela no banco
        engine,                # Engine de conexão
        if_exists="replace",   # Substituir se existir
        index=False,           # Não salvar índice do pandas
    )