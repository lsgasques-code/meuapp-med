import streamlit as st
from openai import OpenAI
import data_helper

st.set_page_config(page_title="Gerador de Planos UNIPAR", layout="wide")

st.title("🍎 Arquiteto de Ensino Medicina UNIPAR")
st.caption("Alinhado às DCNs 2025 e Matriz de Referência ENAMED (Portaria 478/2025)")

# Sidebar para Configurações
with st.sidebar:
    st.header("Configurações")
    api_key = st.text_input("Insira sua OpenAI API Key", type="password")
    professor_nome = st.text_input("Nome do Professor Responsável")

# 1. Identificação do Módulo
modulo_selecionado = st.selectbox("Selecione o Módulo Integrado:", list(data_helper.MODULOS_UNIPAR.keys()))
dados_modulo = data_helper.MODULOS_UNIPAR[modulo_selecionado]

# 2. Entrada do Professor
conteudo_input = st.text_area("Descreva os temas centrais que deseja focar neste semestre:")

if st.button("Gerar Plano de Ensino Ótimo"):
    if not api_key:
        st.error("Por favor, insira a API Key na barra lateral.")
    else:
        client = OpenAI(api_key=api_key)
        
        # Prompt de Engenharia para a IA
        prompt = f"""
        Atue como um Especialista em Educação Médica. Gere um Plano de Ensino para a UNIPAR:
        Módulo: {modulo_selecionado}
        Série: {dados_modulo['serie']}
        Carga Horária: {dados_modulo['carga_horaria']}
        Ementas Oficiais: {dados_modulo['ementas']}
        Ciclo Atual: {dados_modulo['ciclo']}
        
        DIRETRIZES OBRIGATÓRIAS:
        1. Use Taxonomia de Bloom: Para o ciclo {dados_modulo['ciclo']}, use verbos de {'Conhecimento/Compreensão' if dados_modulo['ciclo'] == 'Básico' else 'Aplicação/Análise'}.
        2. Visão Integrada: Organize o conteúdo de forma sistêmica, não separando as disciplinas.
        3. ENAMED: Relacione o conteúdo com as competências da Portaria 478/2025.
        4. Avaliação: Aplique a regra de 70% para provas (Teórica/Prática/OSCE) e 30% para atividades formativas/PBL.
        5. Metodologia: Sugira um mix criativo (TBL, Simulação, Mini-Cex).
        6. Bibliografia: Sugira 3 obras básicas e 5 complementares em ABNT.
        7. Plano de Recuperação: Gere uma estratégia para alunos de baixo desempenho.

        Conteúdo sugerido pelo professor: {conteudo_input}
        """

        with st.spinner('A IA está arquitetando seu plano pedagógico...'):
            response = client.chat.completions.create(
                model="gpt-4o", # ou "gpt-3.5-turbo"
                messages=[{"role": "system", "content": "Você é um consultor pedagógico de medicina de elite."},
                          {"role": "user", "content": prompt}]
            )
            
            plano_gerado = response.choices[0].message.content
            st.markdown(plano_gerado)
            st.download_button("Baixar Plano (Markdown)", plano_gerado, file_name="plano_unipar.md")
