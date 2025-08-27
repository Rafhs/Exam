# pages/1_Dashboard.py (Versão com Edição)

import streamlit as st
import pandas as pd
from data.dados import database as db
from datetime import datetime

st.set_page_config(page_title="Edição de Funcionários", page_icon="👥", layout="wide")

st.title("👥 Consulta e Edição de Funcionários")
st.markdown("Selecione um funcionário na lista para visualizar ou editar suas informações.")

if st.sidebar.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.success("Dados atualizados!")

# --- 1. Seleção do Funcionário para Edição ---
# Usamos a nova função para buscar todos os dados, incluindo o ID
todos_funcionarios = db.get_all_funcionarios_for_editing()

if not todos_funcionarios:
    st.warning("Ainda não há funcionários cadastrados no sistema.")
    st.stop()

# Criamos um dicionário para mapear o nome de exibição ao ID do funcionário
dict_funcionarios = {f"{f[1]} ({f[4]}) - {f[8]}": f[0] for f in todos_funcionarios}
lista_display_funcionarios = ["Selecione um funcionário para editar..."] + sorted(list(dict_funcionarios.keys()))

selecao_display = st.selectbox("Selecione o Funcionário:", options=lista_display_funcionarios)


# --- 2. Formulário de Edição ---
# O formulário só aparece se um funcionário válido for selecionado
if selecao_display != "Selecione um funcionário para editar...":
    # Encontra o ID do funcionário selecionado
    id_selecionado = dict_funcionarios[selecao_display]

    # Busca os dados completos do funcionário selecionado
    dados_atuais = [f for f in todos_funcionarios if f[0] == id_selecionado][0]

    st.divider()
    st.subheader(f"Editando: **{dados_atuais[1]}**")

    with st.form(key="edicao_funcionario_form"):
        # Extrai os dados atuais para preencher o formulário
        _, nome, cpf, rg, matricula, cargo, depto, dt_admissao, empresa, cnpj = dados_atuais
        dt_admissao_obj = datetime.strptime(dt_admissao, '%Y-%m-%d').date()

        # Layout em colunas para organizar o formulário
        col1, col2 = st.columns(2)
        with col1:
            novo_nome = st.text_input("Nome Completo", value=nome)
            novo_cpf = st.text_input("CPF (apenas números)", value=cpf, max_chars=11)
            novo_rg = st.text_input("RG (apenas números)", value=rg, max_chars=9)
            novo_matricula = st.text_input("Matrícula", value=matricula, max_chars=10)
            novo_cargo = st.text_input("Cargo / Função", value=cargo) # Usamos text_input para permitir cargos não cadastrados

        with col2:
            novo_depto = st.text_input("Departamento", value=depto)
            novo_dt_admissao = st.date_input("Data de Admissão", value=dt_admissao_obj)
            novo_empresa = st.text_input("Nome da Empresa", value=empresa)
            novo_cnpj = st.text_input("CNPJ (apenas números)", value=cnpj, max_chars=14)

        # Botão de salvar dentro do formulário
        submit_button = st.form_submit_button(label="Salvar Alterações")

        if submit_button:
            # Validações básicas
            if not (novo_cpf.isdigit() and novo_rg.isdigit() and novo_matricula.isdigit() and novo_cnpj.isdigit()):
                st.error("Erro: CPF, RG, Matrícula e CNPJ devem conter apenas números.")
            else:
                # Chama a função de update do banco de dados
                db.update_funcionario_detalhes(
                    id_selecionado, novo_nome, novo_cpf, novo_rg, novo_matricula,
                    novo_cargo, novo_depto, novo_dt_admissao.strftime('%Y-%m-%d'),
                    novo_empresa, novo_cnpj
                )
                st.success("Dados do funcionário atualizados com sucesso!")
                st.info("A página será atualizada para refletir as mudanças.")
                st.cache_data.clear() # Limpa o cache para forçar a recarga dos dados
                st.rerun() # Recarrega a página

st.divider()

# --- 3. Tabela de Visualização Geral (Opcional, mas útil) ---
st.subheader("Visão Geral dos Funcionários")
# Usamos a função antiga para visualização, que já tem o formato de data correto
df_funcionarios = pd.DataFrame(
    db.get_all_funcionarios_detalhes(),
    columns=["Nome Completo", "CPF", "RG", "Matrícula", "Cargo", "Departamento", "Data de Admissão", "Empresa"]
)
st.dataframe(df_funcionarios, use_container_width=True, hide_index=True)