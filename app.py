import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Dashboard de Análise Musical",
    layout="wide",
)

st.title("Dashboard de Análise e Métricas Musicais")

df = load_data()

# Identificação automática das colunas numéricas
VARS_QUANT = [col for col in df.select_dtypes(include=['float64', 'int64']).columns if col not in ['id', 'label']]

# Encontra a coluna de gênero no dataset
COL_CLASSE = None
for col in df.columns:
    if col.lower() in ['label', 'genre', 'genero', 'class']:
        COL_CLASSE = col
        break

# --- SIDEBAR (FILTROS GLOBAIS) ---
with st.sidebar:
    st.header("Filtros Globais")

    # 1. Filtro Seletor de Gêneros Musicais
    if COL_CLASSE:
        generos_disponiveis = sorted(list(df[COL_CLASSE].dropna().unique()))
        
        generos_selecionados = st.multiselect(
            "Selecione o Gênero Musical:",
            options=generos_disponiveis,
            default=[],  # Inicia vazio para o usuário escolher apenas os gêneros desejados
            placeholder="Escolha os gêneros (ou deixe vazio para todos)...",
            help="Escolha um ou mais gêneros para filtrar todo o dashboard."
        )
    else:
        generos_selecionados = []
        st.warning("Coluna de gênero ('label') não encontrada no dataset.")

    st.markdown("---")
    st.subheader("Filtros de Variáveis (Dashboard 1)")

    variaveis = st.multiselect(
        "Variáveis Quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT[:5],
        help="Selecione as variáveis para a matriz de correlação e histogramas.",
    )

    separar_por_classe = st.toggle(
        "Distinguir por Classe/Gênero",
        value=False,
        help="Aplica divisão por gênero nos gráficos do Dashboard 1.",
    )

    # Sliders de intervalo para as variáveis escolhidas
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

# --- APLICAÇÃO DOS FILTROS NO DATAFRAME ---
df_filtrado = df

# Aplica o filtro de Gênero Musical apenas se o usuário escolher algum
if COL_CLASSE and generos_selecionados:
    df_filtrado = df_filtrado[df_filtrado[COL_CLASSE].isin(generos_selecionados)]

# Aplica os filtros de intervalo das variáveis quantitativas
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(f"{len(df_filtrado)} de {len(df)} registros considerados após filtragem.")

# --- ESTRUTURA DE ABAS ---
tab1, tab2 = st.tabs(["Dashboard 1: Correlação & Distribuição", "Dashboard 2: KPIs & Análise Geral"])

# ==============================================================================
# DASHBOARD 1: CORRELAÇÃO E DISTRIBUIÇÃO
# ==============================================================================
with tab1:
    col_correlacao, col_distribuicao = st.columns([1, 1.3])

with col_correlacao:
    st.subheader("Correlação")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis na barra lateral.")
    else:
        corr = df_filtrado[variaveis].corr()
        
        # Máscara triangular abaixo da diagonal (k=-1)
        mask = np.tril(np.ones(corr.shape, dtype=bool), k=-1)
        corr_triangular = corr.where(mask)

        # Remove a 1ª linha e a última coluna totalmente vazias
        corr_triangular = corr_triangular.iloc[1:, :-1]

        # Escala divergente personalizada: -1 (Lilás claro) -> 0 (Neutro escuro) -> +1 (Roxo vibrante)
        escala_roxo_divergente = [
            [0.0, "#f3e8ff"],   # -1: Correlação negativa (Lilás claro contrastante)
            [0.5, "#18181b"],   #  0: Neutro (combina com o fundo escuro)
            [1.0, "#a855f7"]    # +1: Correlação positiva (Roxo/Lilás vibrante)
        ]

        fig_corr = px.imshow(
            corr_triangular,
            text_auto=".2f",
            color_continuous_scale=escala_roxo_divergente,
            zmin=-1,
            zmax=1,
            aspect="auto",
            title="Matriz de Correlação Triangular (sem Diagonal)"
        )
        fig_corr.update_traces(connectgaps=False)
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_distribuicao:
        st.subheader("Distribuições das Variáveis")

        if variaveis:
            color_col = COL_CLASSE if separar_por_classe else None
            num_cols = 2 if len(variaveis) > 1 else 1
            cols_hist = st.columns(num_cols)

            for idx, var in enumerate(variaveis):
                col_target = cols_hist[idx % num_cols]
                with col_target:
                    fig_hist = px.histogram(
                        df_filtrado,
                        x=var,
                        color=color_col,
                        barmode="overlay" if separar_por_classe else "relative",
                        marginal="box",
                        title=f"Distribuição: {var}",
                        height=280,
                        color_discrete_sequence=px.colors.sequential.Purples_r if not separar_por_classe else px.colors.qualitative.Set2
                    )
                    
                    if not separar_por_classe:
                        fig_hist.update_traces(marker_color="#a855f7", marker_line_color="#c084fc", marker_line_width=1)

                    fig_hist.update_layout(
                        margin=dict(l=10, r=10, t=40, b=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.warning("Selecione pelo menos 1 variável na barra lateral para visualizar as distribuições.")

# ==============================================================================
# DASHBOARD 2: KPIS E MÉTRICAS PRÓPRIAS
# ==============================================================================
with tab2:
    st.subheader("Indicadores Chave de Desempenho (KPIs)")

    # 1. BLOCO DE MÉTRICAS (Quantidade de Músicas, Beats e Tempo)
    m1, m2, m3 = st.columns(3)

    qnt_musicas = len(df_filtrado)
    m1.metric("Quantidade de Músicas", qnt_musicas)

    if "beats" in df_filtrado.columns and not df_filtrado.empty:
        beats_medio = df_filtrado["beats"].mean()
        m2.metric("Média de Beats", f"{beats_medio:.1f}")
    else:
        m2.metric("Média de Beats", "N/A")

    if "tempo" in df_filtrado.columns and not df_filtrado.empty:
        tempo_medio = df_filtrado["tempo"].mean()
        m3.metric("Tempo Médio (BPM)", f"{tempo_medio:.1f}")
    else:
        m3.metric("Tempo Médio (BPM)", "N/A")

    st.markdown("---")
    st.subheader("Visualizações Complementares")

    # BLOCO SUPERIOR (Visual 1 e Visual 2 Lado a Lado)
    c_vis1, c_vis2 = st.columns([1, 1])

    with c_vis1:
        # Visual 1: Média de Beats por Gênero
        if COL_CLASSE in df_filtrado.columns and "beats" in df_filtrado.columns and not df_filtrado.empty:
            beats_by_genre = df_filtrado.groupby(COL_CLASSE)["beats"].mean().reset_index()
            fig_bar = px.bar(
                beats_by_genre,
                x=COL_CLASSE,
                y="beats",
                color=COL_CLASSE,
                title="Visual 1: Média de Beats por Gênero Musical",
                labels={COL_CLASSE: "Gênero", "beats": "Média de Beats"},
                text_auto=".1f"
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    with c_vis2:
        # Visual 2: Dispersão (Tempo vs Beats) - Legenda alinhada perfeitamente na direita
        if "tempo" in df_filtrado.columns and "beats" in df_filtrado.columns:
            fig_scatter = px.scatter(
                df_filtrado,
                x="tempo",
                y="beats",
                color=COL_CLASSE if COL_CLASSE in df_filtrado.columns else None,
                title="Visual 2: Relação entre Tempo (BPM) e Beats",
                labels={"tempo": "Tempo (BPM)", "beats": "Beats", COL_CLASSE: "Gênero Musical"}
            )
            fig_scatter.update_layout(
                showlegend=True,
                legend=dict(
                    title=dict(text="<b>Gênero Musical</b>"),
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # BLOCO INFERIOR (Visual 3: Boxplot)
    if "spectral_centroid" in df_filtrado.columns and COL_CLASSE in df_filtrado.columns:
        fig_box = px.box(
            df_filtrado,
            x=COL_CLASSE,
            y="spectral_centroid",
            color=COL_CLASSE,
            title="Visual 3: Comparação de Brilho Som/Agudos (Centroide Espectral) por Gênero",
            labels={
                COL_CLASSE: "Gênero",
                "spectral_centroid": "Brilho Espectral (Frequência em Hz)"
            }
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)