# Dashboard E-commerce Analytics

🔗 **[Acesse o dashboard](https://ecommerce-dashboard-ml.streamlit.app/)**

Projeto desenvolvido como parte da **Jornada de Dados**, no último dia da imersão.

A ideia foi simples: depois de 3 dias construindo um pipeline completo com SQL, Python e dbt, os dados estavam prontos no banco — mas nenhum diretor acessa o banco de dados. Então criei um dashboard pra resolver isso.

## O que faz

Dashboard interativo em Streamlit com 3 páginas, cada uma pensada pra um perfil diferente:

- **Vendas** — receita diária, pico de vendas por hora e desempenho por dia da semana
- **Clientes** — segmentação VIP/TOP_TIER/REGULAR, top 10 clientes e distribuição por estado
- **Pricing** — posicionamento de preço vs concorrência e alertas de produtos mais caros que todos os concorrentes

## Stack

- Python + Streamlit
- Plotly (gráficos interativos)
- psycopg2 (conexão PostgreSQL)
- Pandas
- Supabase (banco de dados)

## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar credenciais
cp .env.example .env
# Editar .env com suas credenciais do Supabase

# Rodar
streamlit run app.py
```

## Contexto

Os dados vêm de 3 tabelasd gold construídas com dbt em arquitetura Medalhão (Bronze → Silver → Gold):

- `public_gold_sales.vendas_temporais`
- `public_gold_cs.clientes_segmentacao`
- `public_gold_pricing.precos_competitividade`

Utilizei o ClaudeAI pra me ajudar em partes a estruturar e debugar o código durante o desenvolvimento.
