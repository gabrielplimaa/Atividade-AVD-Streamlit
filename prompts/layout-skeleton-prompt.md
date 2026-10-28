# Template: rascunho de layout → esqueleto do app

Preencha cada bloco e envie à ferramenta de IA.

## Contexto

Sou estudante da disciplina de Análise e Visualização de Dados (AVD). O objetivo do dashboard em Streamlit é realizar uma análise exploratória e de correlação entre as variáveis quantitativas do dataset de características musicais (`insiyeah/musicfeatures`).

## Entrada

- **Dataset:** `insiyeah/musicfeatures` (carregado via `src/data_loader.py`).
- **Principais colunas:** `tempo`, `beats`, `chroma_stft`, `rmse`, `spectral_centroid`, `label`.
- **Perguntas a responder:**
  - Qual a correlação linear entre as características acústicas das músicas?
  - Como os filtros de intervalo e a filtragem de faixas alteram a distribuição e as correlações entre as variáveis?

**Descrição do Layout:**
- **Sidebar (à esquerda):** Título de filtros, `st.multiselect` para escolha das variáveis quantitativas, `st.toggle` para distinguir por classe/gênero e `st.slider` dinâmicos de intervalo para cada variável selecionada.
- **Área Principal:** Título do dashboard, indicador de registros filtrados e duas colunas lado a lado:
  - **Coluna 1 (Esquerda):** Subcabeçalho de Correlação e Matriz de Correlação (Heatmap).
  - **Coluna 2 (Direita):** Subcabeçalho de Distribuição, seletor de variável (`st.selectbox`) e Histograma com Boxplot.

## Restrições

- **Bibliotecas:** Streamlit, Pandas e Plotly Express (`plotly.express`).
- **Ficheiro a editar:** `app.py`.
- **Leitura de dados:** Obrigatório carregar através da função `load_data()` importada de `src/data_loader.py`.
- **Regras:** Manter a estrutura de filtros na barra lateral e a divisão em colunas (`st.columns`) no layout principal.

## Formato de saída

Código Python completo e funcional para o ficheiro `app.py`, mantendo os seletores, os sliders de intervalo e os gráficos interativos de heatmap e histograma integrados.