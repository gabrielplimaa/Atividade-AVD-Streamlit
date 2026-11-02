# Declaração de Uso de IA

**Nome:** Gabriel Pereira Lima  
**Data:** 28/10/2026 - 02/11/2026

---

## Ferramenta

Gemini 2.5 Pro (via interface web)

---

## Prompts Utilizados

- *"me de um codigo com a correlação-heatmap [código do app.py fornecido]"*
- *"como rodar meu projeto streamlit"*
- *"ModuleNotFoundError: No module named 'plotly'" / "KeyError: 'age'"* (prints de erros do terminal e do navegador)
- *"deu isso no deploy [imagem do erro ModuleNotFoundError: No module named 'kagglehub']"*
- *"Como declarar dependências e limites de versão corretamente no arquivo requirements.txt para evitar erros no Streamlit Cloud?"*

---

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** 
  - Código do mapa de calor de correlação em Plotly (`px.imshow`) com matriz triangular (`np.tril`) e histogramas em grade (`px.histogram`).
  - Comandos para resolução de erros de ambiente virtual e instalação de dependências (`pip install plotly kagglehub`).
  - Inclusão da biblioteca kagglehub no ficheiro requirements.txt para solucionar a falha de deploy no Streamlit Cloud.
  - Adaptação dinâmica para selecionar automaticamente colunas numéricas do dataset de música (`VARS_QUANT`).

- **Modificado:** 
  - Mantida estritamente a estrutura original do layout do `app.py` fornecida pelo professor (com as colunas e filtros do sidebar), apenas preenchendo os blocos que estavam com `pass` / `TODO`.
  - Reestruturação do gráfico de contagem do Dashboard 2 para **Média de Beats por Gênero**, garantindo variação e valor analítico à visualização.
  - Ajuste nos rótulos do boxplot da variável spectral_centroid para clarificar a interpretação visual de "brilho musical / agudos".
  - Adequação do Visual 3 do Dashboard 2: Reescritos o título e os rótulos do eixo do Boxplot de `spectral_centroid` para deixar claro o conceito de Brilho Musical / Frequências Agudas entre os gêneros.
  - Reestruturação do Visual 1 do Dashboard 2: Rejeitada a proposta inicial de contagem de músicas por gênero (que gerava barras fixas e estáticas em 100) e substituída pela Média de Beats por Gênero, garantindo variação dinâmica e valor analítico à visualização.

- **Rejeitado:** 
  - Proposta inicial de utilizar o dataset `heart` (UCI), pois o projeto foi migrado para o dataset de características musicais (`insiyeah/musicfeatures`).
  - Pré-seleção forçada de todos os gêneros no `st.multiselect`, permitindo ao usuário escolher livremente os gêneros desejados sem poluir o visual.