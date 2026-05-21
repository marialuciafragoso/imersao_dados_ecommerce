import os
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="E-commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# TEMA / ESTILO
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fundo geral */
.stApp {
    background-color: #0f0f13;
    color: #e8e6e1;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #16161d;
    border-right: 1px solid #2a2a35;
}
section[data-testid="stSidebar"] * {
    color: #e8e6e1 !important;
}

/* Título sidebar */
.sidebar-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    color: #f0c040 !important;
    letter-spacing: -0.5px;
    margin-bottom: 0.2rem;
}
.sidebar-sub {
    font-size: 0.75rem;
    color: #666 !important;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Cabeçalho de página */
.page-header {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: #f0c040;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}
.page-sub {
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 1.5rem;
}

/* Cards de KPI */
div[data-testid="metric-container"] {
    background: #16161d;
    border: 1px solid #2a2a35;
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
div[data-testid="metric-container"] label {
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #888 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem !important;
    color: #f0c040 !important;
    font-weight: 700;
}

/* Divisor */
hr {
    border-color: #2a2a35;
    margin: 1.5rem 0;
}

/* Seção de alerta */
.alert-header {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: #ff5252;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

/* Botão de recarregar */
.stButton button {
    background: #f0c040;
    color: #0f0f13;
    border: none;
    font-weight: 700;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONEXÃO
# ─────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        port=int(os.getenv("SUPABASE_PORT", 5432)),
        dbname=os.getenv("SUPABASE_DB", "postgres"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
    )

def run_query(sql: str) -> pd.DataFrame:
    try:
        conn = get_connection()
        return pd.read_sql(sql, conn)
    except Exception as e:
        st.error(f"❌ Erro ao conectar com o banco: {e}")
        st.stop()

# ─────────────────────────────────────────────
# FORMATAÇÃO
# ─────────────────────────────────────────────
def fmt_brl(valor: float) -> str:
    return f"R$ {valor:_.2f}".replace("_", ".").replace(".", ",", 1).replace(",", ".", 1).replace(".", ",", 1)

def fmt_brl_k(valor: float) -> str:
    """Formata valor monetário em formato BRL."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_num(valor) -> str:
    return f"{int(valor):,}".replace(",", ".")

# ─────────────────────────────────────────────
# PLOTLY TEMA
# ─────────────────────────────────────────────
PLOT_BG    = "#16161d"
PAPER_BG   = "#16161d"
FONT_COLOR = "#e8e6e1"
ACCENT     = "#f0c040"
GRID_COLOR = "#2a2a35"
PALETTE    = ["#f0c040", "#4ecdc4", "#ff6b6b", "#a78bfa", "#34d399", "#fb923c"]

def base_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne", size=16, color=ACCENT)),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family="DM Sans", color=FONT_COLOR),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_COLOR)),
        margin=dict(t=50, b=40, l=40, r=20),
    )
    return fig

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 E-commerce</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Analytics Dashboard</div>', unsafe_allow_html=True)

    pagina = st.radio(
        "Navegar para",
        ["Vendas", "Clientes", "Pricing"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    if st.button("🔄 Recarregar dados"):
        st.cache_resource.clear()
        st.rerun()

    st.markdown("---")
    st.markdown('<span style="font-size:0.7rem;color:#444;">Gold Layer · Supabase · dbt</span>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PÁGINA 1: VENDAS
# ═══════════════════════════════════════════════════════
if pagina == "Vendas":
    st.markdown('<div class="page-header">Vendas</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Visão operacional para o Diretor Comercial</div>', unsafe_allow_html=True)

    df = run_query("SELECT * FROM public_gold_sales.vendas_temporais ORDER BY data_venda DESC, hora_venda")

    # Filtro de mês
    meses_disp = sorted(df["mes_venda"].unique())
    meses_labels = {m: f"Mês {int(m):02d}" for m in meses_disp}
    opcoes = ["Todos"] + [meses_labels[m] for m in meses_disp]
    sel = st.selectbox("Filtrar por mês", opcoes)
    if sel != "Todos":
        mes_num = int(sel.split()[1])
        df = df[df["mes_venda"] == mes_num]

    # ── KPIs
    receita_total  = df["receita_total"].sum()
    total_vendas   = df["total_vendas"].sum()
    ticket_medio   = receita_total / total_vendas if total_vendas else 0
    clientes_unicos = df["total_clientes_unicos"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receita Total", fmt_brl_k(receita_total))
    c2.metric("Total de Vendas", fmt_num(total_vendas))
    c3.metric("Ticket Médio", fmt_brl_k(ticket_medio))
    c4.metric("Clientes Únicos", fmt_num(clientes_unicos))

    st.markdown("---")

    # ── Gráfico 1: Receita Diária
    df_dia = df.groupby("data_venda", as_index=False)["receita_total"].sum()
    fig1 = px.line(df_dia, x="data_venda", y="receita_total", color_discrete_sequence=[ACCENT])
    fig1 = base_layout(fig1, "Receita Diária")
    fig1.update_traces(line_width=2)
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns(2)

    # ── Gráfico 2: Receita por Dia da Semana
    ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    df_semana = df.groupby("dia_semana_nome", as_index=False)["receita_total"].sum()
    df_semana["dia_semana_nome"] = pd.Categorical(df_semana["dia_semana_nome"], categories=ordem_dias, ordered=True)
    df_semana = df_semana.sort_values("dia_semana_nome")

    with col_a:
        fig2 = px.bar(df_semana, x="dia_semana_nome", y="receita_total", color_discrete_sequence=[ACCENT])
        fig2 = base_layout(fig2, "Receita por Dia da Semana")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Gráfico 3: Vendas por Hora
    df_hora = df.groupby("hora_venda", as_index=False)["total_vendas"].sum()
    with col_b:
        fig3 = px.bar(df_hora, x="hora_venda", y="total_vendas", color_discrete_sequence=["#4ecdc4"])
        fig3 = base_layout(fig3, "Volume de Vendas por Hora")
        st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════
# PÁGINA 2: CLIENTES
# ═══════════════════════════════════════════════════════
elif pagina == "Clientes":
    st.markdown('<div class="page-header">Clientes</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Segmentação e retenção para a Diretora de Customer Success</div>', unsafe_allow_html=True)

    df = run_query("SELECT * FROM public_gold_cs.clientes_segmentacao ORDER BY ranking_receita")

    # ── KPIs
    total_cli    = len(df)
    vip_count    = len(df[df["segmento_cliente"] == "VIP"])
    receita_vip  = df[df["segmento_cliente"] == "VIP"]["receita_total"].sum()
    ticket_medio = df["ticket_medio"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Clientes", fmt_num(total_cli))
    c2.metric("Clientes VIP", fmt_num(vip_count))
    c3.metric("Receita VIP", fmt_brl_k(receita_vip))
    c4.metric("Ticket Médio Geral", fmt_brl_k(ticket_medio))

    st.markdown("---")

    col_a, col_b = st.columns(2)

    # ── Gráfico 1: Distribuição por Segmento (pizza)
    df_seg = df.groupby("segmento_cliente", as_index=False).size().rename(columns={"size": "total"})
    with col_a:
        fig1 = px.pie(df_seg, names="segmento_cliente", values="total",
                      color_discrete_sequence=PALETTE, hole=0.45)
        fig1 = base_layout(fig1, "Distribuição de Clientes por Segmento")
        st.plotly_chart(fig1, use_container_width=True)

    # ── Gráfico 2: Receita por Segmento
    df_rec_seg = df.groupby("segmento_cliente", as_index=False)["receita_total"].sum()
    with col_b:
        fig2 = px.bar(df_rec_seg, x="segmento_cliente", y="receita_total",
                      color_discrete_sequence=[ACCENT])
        fig2 = base_layout(fig2, "Receita por Segmento")
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    # ── Gráfico 3: Top 10 Clientes
    df_top10 = df[df["ranking_receita"] <= 10].sort_values("receita_total")
    with col_c:
        fig3 = px.bar(df_top10, x="receita_total", y="nome_cliente",
                      orientation="h", color_discrete_sequence=["#a78bfa"])
        fig3 = base_layout(fig3, "Top 10 Clientes por Receita")
        st.plotly_chart(fig3, use_container_width=True)

    # ── Gráfico 4: Clientes por Estado
    df_estado = df.groupby("estado", as_index=False).size().rename(columns={"size": "total"})
    df_estado = df_estado.sort_values("total", ascending=False)
    with col_d:
        fig4 = px.bar(df_estado, x="estado", y="total",
                      color_discrete_sequence=["#34d399"])
        fig4 = base_layout(fig4, "Clientes por Estado")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ── Tabela detalhada com filtro
    seg_opcoes = ["Todos"] + sorted(df["segmento_cliente"].unique().tolist())
    seg_sel = st.selectbox("Filtrar tabela por segmento", seg_opcoes)
    df_tabela = df if seg_sel == "Todos" else df[df["segmento_cliente"] == seg_sel]
    st.dataframe(df_tabela.reset_index(drop=True), use_container_width=True)

# ═══════════════════════════════════════════════════════
# PÁGINA 3: PRICING
# ═══════════════════════════════════════════════════════
elif pagina == "Pricing":
    st.markdown('<div class="page-header">Pricing</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Inteligência competitiva para o Diretor de Pricing</div>', unsafe_allow_html=True)

    df = run_query("SELECT * FROM public_gold_pricing.precos_competitividade")

    # Filtro de categoria
    cats = sorted(df["categoria"].unique().tolist())
    sel_cats = st.multiselect("Filtrar por categoria", cats, default=cats)
    if sel_cats:
        df = df[df["categoria"].isin(sel_cats)]

    # ── KPIs
    total_prod   = len(df)
    mais_caros   = len(df[df["classificacao_preco"] == "MAIS_CARO_QUE_TODOS"])
    mais_baratos = len(df[df["classificacao_preco"] == "MAIS_BARATO_QUE_TODOS"])
    dif_media    = df["diferenca_percentual_vs_media"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Produtos Monitorados", fmt_num(total_prod))
    c2.metric("Mais Caros que Todos", fmt_num(mais_caros))
    c3.metric("Mais Baratos que Todos", fmt_num(mais_baratos))
    c4.metric("Diferença Média vs Mercado", f"{dif_media:+.1f}%")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    # ── Gráfico 1: Distribuição por Classificação
    df_class = df.groupby("classificacao_preco", as_index=False).size().rename(columns={"size": "total"})
    with col_a:
        fig1 = px.pie(df_class, names="classificacao_preco", values="total",
                      color_discrete_sequence=PALETTE, hole=0.45)
        fig1 = base_layout(fig1, "Posicionamento de Preço vs Concorrência")
        st.plotly_chart(fig1, use_container_width=True)

    # ── Gráfico 2: Competitividade por Categoria
    df_cat = df.groupby("categoria", as_index=False)["diferenca_percentual_vs_media"].mean()
    df_cat = df_cat.sort_values("diferenca_percentual_vs_media", ascending=False)
    cores_cat = ["#ff5252" if v > 0 else "#34d399" for v in df_cat["diferenca_percentual_vs_media"]]
    with col_b:
        fig2 = go.Figure(go.Bar(
            x=df_cat["categoria"],
            y=df_cat["diferenca_percentual_vs_media"],
            marker_color=cores_cat,
        ))
        fig2 = base_layout(fig2, "Competitividade por Categoria (%)")
        fig2.add_hline(y=0, line_color="#555", line_dash="dash")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Gráfico 3: Scatter Preço vs Volume
    fig3 = px.scatter(
        df,
        x="diferenca_percentual_vs_media",
        y="quantidade_total",
        color="classificacao_preco",
        size="receita_total",
        hover_name="nome_produto",
        color_discrete_sequence=PALETTE,
        size_max=40,
    )
    fig3 = base_layout(fig3, "Competitividade × Volume de Vendas")
    fig3.add_vline(x=0, line_color="#555", line_dash="dash")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ── Tabela de alertas
    st.markdown('<div class="alert-header">🚨 Produtos em Alerta — Mais caros que todos os concorrentes</div>', unsafe_allow_html=True)
    df_alerta = df[df["classificacao_preco"] == "MAIS_CARO_QUE_TODOS"][[
        "produto_id", "nome_produto", "categoria", "nosso_preco",
        "preco_maximo_concorrentes", "diferenca_percentual_vs_media"
    ]].sort_values("diferenca_percentual_vs_media", ascending=False)

    if df_alerta.empty:
        st.success("Nenhum produto mais caro que todos os concorrentes no filtro selecionado.")
    else:
        st.dataframe(df_alerta.reset_index(drop=True), use_container_width=True)
