# pages/3_Lançar_Exames.py (Versão com Atualização Automática)

import streamlit as st
from datetime import datetime, timedelta
from data.dados import database as db


st.set_page_config(page_title="Lançar Exames", page_icon="📋", layout="wide")

st.header("📋 Lançar Novo Exame Ocupacional")
st.markdown("Selecione um funcionário para ver seus detalhes e os exames recomendados.")

if st.sidebar.button("🔄 Atualizar Listas (Manual)"):
    st.cache_data.clear()
    st.success("Listas de funções e funcionários atualizadas!")

# --- ETAPA 1: Lógica de Seleção de Funcionário ---
todos_funcionarios = db.get_all_funcionarios()
if not todos_funcionarios:
    st.warning("Nenhum funcionário cadastrado.")
    st.stop()

lista_funcionarios_detalhes = [
    {"id": id, "nome": nome, "matricula": matricula, "cargo": cargo, "empresa": empresa}
    for id, nome, matricula, cargo, empresa in todos_funcionarios
]
nomes_unicos = sorted(list(set([func["nome"] for func in lista_funcionarios_detalhes])))
funcionario_selecionado_final = None

col_func, col_desambiguacao = st.columns(2)
with col_func:
    st.subheader("1. Selecione o Funcionário")
    nome_selecionado = st.selectbox(
        "Funcionário",
        options=["Selecione..."] + nomes_unicos,
        label_visibility="collapsed"
    )

if nome_selecionado and nome_selecionado != "Selecione...":
    candidatos = [func for func in lista_funcionarios_detalhes if func["nome"] == nome_selecionado]
    if len(candidatos) > 1:
        with col_desambiguacao:
            st.subheader("Desambiguação")
            opcoes_desambiguacao = {f"{c['matricula']} - {c['empresa']}": c for c in candidatos}
            chave_selecionada = st.radio(
                "Múltiplos funcionários encontrados. Selecione o correto:",
                options=opcoes_desambiguacao.keys()
            )
            funcionario_selecionado_final = opcoes_desambiguacao[chave_selecionada]
    else:
        funcionario_selecionado_final = candidatos[0]

# --- Layout para Detalhes e Opções ---
col_emp, col_atual, col_tipo_exame = st.columns(3)
empresa_selecionada = ""
funcionario_cargo = ""
if funcionario_selecionado_final:
    empresa_selecionada = funcionario_selecionado_final["empresa"]
    funcionario_cargo = funcionario_selecionado_final["cargo"]

with col_emp:
    st.text_input("Empresa", value=empresa_selecionada, disabled=True)
with col_atual:
    st.text_input("Função Atual", value=funcionario_cargo, disabled=True)
with col_tipo_exame:
    tipo_exame_selecionado = st.selectbox(
        "Tipo de Exame",
        options=["Admissional", "Periódico", "Mudança de Risco", "Retorno ao Trabalho", "Demissional"]
    )

mudanca_funcao = False
nova_funcao_selecionada = None
if funcionario_selecionado_final:
    mudanca_funcao = st.checkbox("Realizar Mudança de Função?")
    if mudanca_funcao:
        funcoes = db.get_all_funcoes()
        opcoes_funcoes = [funcao[1] for funcao in funcoes]
        if funcionario_cargo and funcionario_cargo not in opcoes_funcoes:
            opcoes_funcoes.insert(0, funcionario_cargo)
        nova_funcao_selecionada = st.selectbox("Selecione a Nova Função", options=opcoes_funcoes)
        tipo_exame_selecionado = "Mudança de Risco"

st.markdown("---")

# --- O restante da página só aparece após uma seleção final ---
exames_realizados = []
if funcionario_selecionado_final:
    funcao_base_recomendacao = nova_funcao_selecionada if mudanca_funcao else funcionario_cargo
    with st.expander(f"Exames Específicos Recomendados para a Função: **{funcao_base_recomendacao}**", expanded=True):
        # Lógica para mostrar exames...
        if funcao_base_recomendacao:
            exames_recomendados = db.get_exames_por_nome_funcao(funcao_base_recomendacao)
            if exames_recomendados:
                for exame in exames_recomendados:
                    if st.checkbox(exame, key=f"exame_{funcao_base_recomendacao}_{exame}"):
                        exames_realizados.append(exame)
            else:
                st.info(f"Não há exames específicos pré-cadastrados para a função '{funcao_base_recomendacao}'.")
        else:
            st.warning("Funcionário sem cargo definido ou nova função não encontrada.")

    with st.form(key="lancamento_exame_form"):
        st.subheader("2. Detalhes do Lançamento")
        exames_especificos_str = ", ".join(exames_realizados)
        nome_final_exame = f"{tipo_exame_selecionado} ({exames_especificos_str})" if exames_especificos_str else tipo_exame_selecionado
        tipo_exame = st.text_input("Descrição Final do Exame", value=nome_final_exame)
        data_realizacao = st.date_input("Data de Realização", value=datetime.now(), format="DD/MM/YYYY")
        vencimento_default = data_realizacao + timedelta(days=365)
        data_vencimento = st.date_input("Data de Vencimento do Próximo Exame", value=vencimento_default, format="DD/MM/YYYY")
        status = st.radio("Status do Exame:", ["Apto", "Inapto", "Apto com restrições"], horizontal=True)
        observacoes = st.text_area("Observações")

        submit_button = st.form_submit_button(label="Salvar Alterações e Lançar Exame")

        if submit_button:
            if tipo_exame and funcionario_selecionado_final:
                funcionario_id = funcionario_selecionado_final["id"]

                if mudanca_funcao and nova_funcao_selecionada:
                    if db.update_funcionario_funcao(funcionario_id, nova_funcao_selecionada):
                        st.success(f"A função do funcionário foi alterada para '{nova_funcao_selecionada}' com sucesso!")

                db.add_exame(
                    funcionario_id, tipo_exame, data_realizacao.strftime('%Y-%m-%d'),
                    data_vencimento.strftime('%Y-%m-%d'), status, observacoes
                )
                st.success(f"Exame para {funcionario_selecionado_final['nome']} lançado com sucesso!")
                st.balloons()

                # --- ALTERAÇÃO PRINCIPAL AQUI ---
                # Esta linha limpa o cache de dados, forçando a atualização em todas as páginas.
                st.cache_data.clear()
            else:
                st.error("Erro: Um funcionário deve ser selecionado e o campo 'Descrição Final do Exame' é obrigatório.")
else:
    st.info("Selecione um funcionário acima para continuar.")