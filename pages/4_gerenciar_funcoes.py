import streamlit as st
from data.dados import database as db


st.set_page_config(page_title="Gerenciar Funções", page_icon="🛠️", layout="wide")

st.title("🛠️ Gerenciar Funções e Exames Associados")
st.markdown("Cadastre funções e vincule os exames necessários para cada uma.")

# --- Seção de Cadastro de Nova Função ---
st.header("Cadastrar Nova Função")
with st.form(key="nova_funcao_form", clear_on_submit=True):
    nome_nova_funcao = st.text_input("Nome da Função", placeholder="Ex: Eletricista")
    submit_nova_funcao = st.form_submit_button("Adicionar Função")

    if submit_nova_funcao and nome_nova_funcao:
        if db.add_funcao(nome_nova_funcao):
            st.success(f"Função '{nome_nova_funcao}' adicionada com sucesso!")
        else:
            st.error(f"Erro: A função '{nome_nova_funcao}' já existe.")

st.markdown("---")

# --- Seção para Associar Exames a uma Função Existente ---
st.header("Associar Exames a uma Função")

# Busca todas as funções cadastradas
funcoes_cadastradas = db.get_all_funcoes()

if not funcoes_cadastradas:
    st.warning("Nenhuma função cadastrada. Adicione uma função acima para começar.")
    st.stop()

# Cria um dicionário para o selectbox: {nome_funcao: id}
opcoes_funcoes = {funcao[1]: funcao[0] for funcao in funcoes_cadastradas}
funcao_selecionada_nome = st.selectbox("Selecione a Função", options=opcoes_funcoes.keys())

# Colunas para organizar a visualização
col1, col2 = st.columns(2)

with col1:
    st.subheader("Adicionar Novo Exame")
    with st.form(key="add_exame_form"):
        # Campo para adicionar um novo exame à função selecionada
        nome_novo_exame = st.text_input("Nome do Exame", placeholder="Ex: Acuidade Visual")
        submit_add_exame = st.form_submit_button("Vincular Exame")

        if submit_add_exame and nome_novo_exame:
            funcao_id = opcoes_funcoes[funcao_selecionada_nome]
            db.add_exame_para_funcao(funcao_id, nome_novo_exame)
            st.success(f"Exame '{nome_novo_exame}' vinculado à função '{funcao_selecionada_nome}'.")
            # Força o rerun para atualizar a lista de exames
            st.rerun()

with col2:
    st.subheader("Exames já Vinculados")
    if funcao_selecionada_nome:
        funcao_id = opcoes_funcoes[funcao_selecionada_nome]
        exames_vinculados = db.get_exames_por_funcao(funcao_id)

        if exames_vinculados:
            for exame in exames_vinculados:
                st.write(f"- {exame}")
        else:
            st.info("Nenhum exame vinculado a esta função ainda.")