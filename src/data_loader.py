import kagglehub
import pandas as pd
import streamlit as st
from kagglehub import KaggleDatasetAdapter


@st.cache_data
def load_data(path="data/clean/dataset.csv"):
    """Carrega o dataset de música usando o kagglehub com suporte a cache."""
    try:
        # Tenta carregar primeiro via kagglehub
        df = kagglehub.dataset_load(
            KaggleDatasetAdapter.PANDAS,
            "insiyeah/musicfeatures",
            "data.csv",
        )
    except Exception:
        # Fallback para o arquivo local caso esteja offline
        df = pd.read_csv(path)

    return df