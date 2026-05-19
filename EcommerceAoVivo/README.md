# Ecommerce Analytics

Pipeline de dados de um mercado construído com dbt, seguindo a arquitetura Medallion (Bronze → Silver → Gold).

O projeto nasceu de um problema real: transformar dados operacionais brutos em métricas de negócio úteis — como receita por período, comportamento de clientes e monitoramento de preços competidores.

---

## Arquitetura

```
Supabase (dados operacionais)
        │
        ▼
   [ Bronze ]  → cópia fiel da fonte, sem transformações
        │
        ▼
   [ Silver ]  → dados limpos e enriquecidos
        │
        ▼
    [ Gold ]   → métricas prontas para análise
```

---

## Domínios

**Sales** — receita, quantidade vendida e ticket médio agregados por dia e hora

**Customer Success** — comportamento e frequência de compra por cliente

**Pricing** — comparativo de preços com competidores

---

## O que foi aplicado

- Arquitetura Medallion com separação clara entre dado bruto, limpo e agregado
- Colunas calculadas na silver (ex: `receita_total = quantidade × preço unitário`)
- Dimensões temporais extraídas para facilitar análises (ano, mês, dia, hora, dia da semana)
- Métricas de negócio agregadas na gold prontas para dashboard


## Tecnologias

| Ferramenta | Uso |
|------------|-----|
| Supabase   | Banco de dados operacional (fonte dos dados) |
|    dbt     | Transformação e modelagem dos dados |
|    SQL     | Linguagem de transformação |
|    Git     | Versionamento |

