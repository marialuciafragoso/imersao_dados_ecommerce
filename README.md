# E-commerce Analytics — Jornada de Dados

Pipeline completo de dados de um e-commerce, do dado bruto até o dashboard online.

🔗 **[Acessar o dashboard](https://ecommerce-dashboard-ml.streamlit.app/)**

---

## O que foi feito em 4 dias

**Dia 1 — SQL**
Exploração do negócio com queries respondendo perguntas reais sobre vendas, clientes e preços vs concorrência.

**Dia 2 — Python**
Ingestão de dados de múltiplas fontes (CSVs, APIs e banco) para o PostgreSQL no Supabase.

**Dia 3 — dbt**
Modelagem em arquitetura Medalhão:

```
Bronze → Silver → Gold
```

3 Data Marts entregues:
- `vendas_temporais` — métricas de vendas por dia/hora
- `clientes_segmentacao` — segmentação VIP/TOP_TIER/REGULAR
- `precos_competitividade` — posicionamento vs concorrência

**Dia 4 — Dashboard**
Dashboard em Streamlit com 3 páginas, uma pra cada diretor:
- **Vendas** — receita diária, ticket médio e pico por hora
- **Clientes** — segmentação, top 10 e distribuição por estado
- **Pricing** — alertas de produtos mais caros que todos os concorrentes

---

## Stack

| Camada | Ferramenta |
|---|---|
| Banco | PostgreSQL (Supabase) |
| Ingestão | Python + Pandas |
| Transformação | dbt |
| Visualização | Streamlit + Plotly |
| Deploy | Streamlit Community Cloud |

---

## Estrutura

```
imersao_dados_ecommerce/
├── EcommerceAoVivo/       # Projeto dbt (Bronze/Silver/Gold)
├── case-01-dashboard/     # Dashboard Streamlit
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
└── parquet_pipeline.py    # Pipeline de ingestão
```
