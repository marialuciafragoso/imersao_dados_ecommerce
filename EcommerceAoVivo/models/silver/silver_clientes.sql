-- ============================================
-- CAMADA SILVER: Clientes (Dados Limpos)
-- ============================================
-- Conceito: Segunda camada da arquitetura Medalhão
-- Objetivo: Limpeza e padronização dos dados

SELECT
    id_cliente,
    nome_cliente,
    estado,
    pais,
    data_cadastro
FROM {{ ref('bronze_clientes') }}
