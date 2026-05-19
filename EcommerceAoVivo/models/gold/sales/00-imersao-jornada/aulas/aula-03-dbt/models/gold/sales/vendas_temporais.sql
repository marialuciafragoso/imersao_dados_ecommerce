-- ============================================
-- CAMADA GOLD: KPI - Vendas Temporais
-- ============================================
-- Conceito: Terceira camada da arquitetura Medalhão
-- Objetivo: Criar métricas de negócio prontas para análise

-- O que essa query responde na prática:
-- "Me mostra, pra cada dia e hora, quanto vendeu, quantas vendas foram, quantos clientes únicos e qual foi o ticket médio."


-- Aqui recolhe os dados do EXTRACT (quebra da data em predaços)
SELECT
    v.data_venda_date AS data_venda,
    v.ano_venda,
    v.mes_venda,
    v.dia_venda,
-- no silver, dia da semana é de 0 a 6, aqui transforma em dado legivel
    CASE v.dia_semana
        WHEN 0 THEN 'Domingo'
        WHEN 1 THEN 'Segunda'
        WHEN 2 THEN 'Terça'
        WHEN 3 THEN 'Quarta'
        WHEN 4 THEN 'Quinta'
        WHEN 5 THEN 'Sexta'
        WHEN 6 THEN 'Sábado'
    END AS dia_semana_nome,
    v.hora_venda,
    SUM(v.receita_total) AS receita_total, -- toda receita daquele dia e hora
    SUM(v.quantidade) AS quantidade_total, -- quantos itens foram vendidos no total 
    COUNT(DISTINCT v.id_venda) AS total_vendas, -- quantas vendas aconteceram 
    COUNT(DISTINCT v.id_cliente) AS total_clientes_unicos,-- quantos clientes diferentes compraram  
    AVG(v.receita_total) AS ticket_medio -- valor medio por venda
-- Acessa apenas a camada silver
FROM {{ ref('silver_vendas') }} v
-- Agrupa todas as vendas que tem mesma date e hora em uma linha (SUM e COUNT em cima)
GROUP BY 1, 2, 3, 4, 5, 6 
-- Mostra primeiro os dias mais recentes, e dentro de cada dia ordena por hora do início ao fim.
ORDER BY data_venda DESC, v.hora_venda