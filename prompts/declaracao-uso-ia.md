# Declaração de Uso de IA

**Nome:** Gabriel Pereira Lima
**Data:** 28/10/2026

## Ferramenta

Gemini 2.5 Pro (via interface web)

## Prompt usado

> "me de um codigo com a correlação-heatmap [código do app.py fornecido]"
> "como rodar meu projeto streamlit"
> "ModuleNotFoundError: No module named 'plotly'" / "KeyError: 'age'" (prints de erros do terminal e do navegador)

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** 
  - Código do mapa de calor de correlação em Plotly (`px.imshow`) e histograma (`px.histogram`).
  - Comandos para resolução de erros de ambiente virtual e instalação de dependências (`python -m pip install plotly kagglehub`).
  - Adaptação dinâmica para selecionar automaticamente colunas numéricas do dataset de música (`VARS_QUANT`).

- **Modificado:** 
  - Mantida estritamente a estrutura original do layout do `app.py` fornecida pelo professor (com as colunas e filtros do sidebar), apenas preenchendo os blocos que estavam com `pass` / `TODO`.

- **Rejeitado:** 
  - Proposta inicial de utilizar o dataset `heart` (UCI), pois o projeto foi migrado para o dataset de características musicais (`insiyeah/musicfeatures`).