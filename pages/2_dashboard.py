import streamlit as st
import pandas as pd
from data.dados import database as db

st.set_page_config(page_title="Análise de Funcionários", page_icon="👥", layout="wide")

st.title("👥 Consulta Geral de Funcionários")
st.markdown("Visualize, filtre e exporte os dados de todos os funcionários cadastrados no sistema.")

# --- 1. Buscar e Preparar os Dados ---
todos_funcionarios = db.get_all_funcionarios_detalhes()

if not todos_funcionarios:
    st.warning("Ainda não há funcionários cadastrados no sistema.")
    st.stop()

# Criamos o DataFrame com a ordem original vinda do banco de dados
df_funcionarios = pd.DataFrame(
    todos_funcionarios,
    columns=["Nome Completo", "CPF", "RG", "Matrícula", "Cargo", "Departamento", "Data de Admissão", "Empresa"]
)

# --- 2. Filtros na Barra Lateral (Sidebar) ---
st.sidebar.header("Filtros de Análise")

empresas_unicas = sorted(df_funcionarios["Empresa"].unique())
empresas_selecionadas = st.sidebar.multiselect(
    "Filtrar por Empresa:",
    options=empresas_unicas,
    default=empresas_unicas
)

cargos_unicos = sorted(df_funcionarios["Cargo"].unique())
cargos_selecionados = st.sidebar.multiselect(
    "Filtrar por Cargo/Função:",
    options=cargos_unicos,
    default=cargos_unicos
)

# Aplicando os filtros ao DataFrame
df_filtrado = df_funcionarios[
    (df_funcionarios["Empresa"].isin(empresas_selecionadas)) &
    (df_funcionarios["Cargo"].isin(cargos_selecionados))
    ]

# --- ALTERAÇÃO PRINCIPAL AQUI ---
# 3. Reordenar as colunas para a exibição final
ordem_colunas_exibicao = [
    "Matrícula",
    "Nome Completo",
    "RG",
    "Cargo",
    "Departamento",
    "Data de Admissão",
    "Empresa"
]
df_exibicao = df_filtrado[ordem_colunas_exibicao]
# --- FIM DA ALTERAÇÃO ---


# --- 4. Exibição dos Dados e Opção de Download ---
st.markdown("---")
st.write(f"**Total de funcionários encontrados:** {len(df_exibicao)}")

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')

# O download continuará exportando todas as colunas, incluindo CPF, o que é útil para relatórios completos.
csv = convert_df_to_csv(df_filtrado)

st.download_button(
    label="📥 Baixar relatório completo (.csv)",
    data=csv,
    file_name='relatorio_funcionarios_completo.csv',
    mime='text/csv',
)

# Exibe a tabela com a nova ordem de colunas
st.dataframe(df_exibicao, use_container_width=True, hide_index=True)