import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Avaliação de Correlação entre Variáveis Quantitativas de Música",
    layout="wide",
)

st.title("Avaliação de Correlação entre Variáveis Quantitativas de Música")

df = load_data()

# Se o dataset for o de música, usamos as suas colunas numéricas:
VARS_QUANT = [col for col in df.select_dtypes(include=['float64', 'int64']).columns if col not in ['id', 'label']]

# Sidebar: filtros (variáveis + intervalo)
with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis Quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT[:5],  # Seleciona as primeiras 5 por padrão
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
    )

    separar_por_classe = st.toggle(
        "Distinguir por Classe",
        value=False,
        help="Colore a distribuição pela classe/gênero musical (se disponível).",
    )

    # Um slider de intervalo para cada variável selecionada
    intervalos = {}
    for var in variaveis:
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
        intervalos[var] = st.slider(
            f"Intervalo de {var}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

# Mantém só os registros dentro de todos os intervalos escolhidos
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(f"{len(df_filtrado)} de {len(df)} registos dentro dos intervalos escolhidos.")

# Dashboard 1: correlação (heatmap) à esquerda, distribuição (histograma) à direita
col_correlacao, col_distribuicao = st.columns([1, 1.5])

with col_correlacao:
    st.subheader("Correlação")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
    else:
        corr = df_filtrado[variaveis].corr()

        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto",
            title="Matriz de Correlação (Pearson)"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

with col_distribuicao:
    st.subheader("Distribuição")

    if variaveis:
        var_selecionada = st.selectbox(
            "Selecione a variável para o histograma:",
            options=variaveis,
            key="select_hist_var"
        )

        coluna_classe = "label" if "label" in df_filtrado.columns else None
        color_col = coluna_classe if separar_por_classe else None

        fig_hist = px.histogram(
            df_filtrado,
            x=var_selecionada,
            color=color_col,
            barmode="overlay" if separar_por_classe else "relative",
            marginal="box",
            title=f"Distribuição de {var_selecionada}"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("Selecione pelo menos 1 variável na barra lateral para visualizar a distribuição.")