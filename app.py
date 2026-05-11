import streamlit as st
from docx import Document
import datetime

# --- 1. BANCO DE DADOS DE REFERÊNCIA (DCN e ENAMED) ---
MATRIZ = {
    "EIXOS": {
        "I": "Ética Médica e Humanidades", "II": "Bioética e Bioestatística", 
        "III": "Ciências Morfofuncionais", "IV": "Fisiopatologia e Semiológica",
        "XVII": "Vigilância em Saúde e Doenças Transmissíveis",
        "XX": "Metodologia Científica e MBE", "XXI": "Tecnologias de Informação (Saúde Digital)"
        # Adicione os outros eixos aqui seguindo o mesmo padrão
    },
    "DOMINIOS": ["Cognitivo (Saber)", "Psicomotor (Fazer)", "Atitudinal (Ser)"]
}

# --- 2. INTERFACE DO USUÁRIO ---
st.set_page_config(page_title="Gerador de Plano de Ensino Medicina", layout="wide")
st.title("🏥 Assistente de Planos de Ensino - Medicina 2025")
st.markdown("Desenvolvido para conformidade com DCNs 2025 e Matriz ENAMED.")

col1, col2 = st.columns(2)

with col1:
    st.header("📝 Dados da Disciplina")
    professor = st.text_input("Nome do Professor")
    disciplina = st.text_input("Nome da Disciplina")
    duracao = st.selectbox("Duração", ["20 Semanas", "40 Semanas"])
    temas = st.text_area("Insira os tópicos principais (um por linha):", height=150)

with col2:
    st.header("⚙️ Configurações Institucionais")
    st.write("**Recursos Disponíveis:** Chromebooks, UpToDate, Bibliotecas, Monitores.")
    st.write("**Avaliação:** 70% Prova Teórico-Prática | 30% Atividades Ativas.")
    metodologia = st.multiselect("Metodologias Ativas:", ["TBL", "PBL", "Seminários", "Simulação"])

# --- 3. LÓGICA DE GERAÇÃO DO DOCUMENTO ---
def gerar_docx(dados):
    doc = Document()
    doc.add_heading(f'Plano de Ensino: {dados["disciplina"]}', 0)
    
    # Seção 1: Objetivos
    doc.add_heading('1. Objetivos de Aprendizagem (DCN 2025)', level=1)
    doc.add_paragraph(f"Esta disciplina foca nos domínios: {', '.join(MATRIZ['DOMINIOS'])}.")
    
    # Seção 2: Cronograma e ENAMED
    doc.add_heading('2. Cronograma e Eixos ENAMED', level=1)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Semana'
    hdr_cells[1].text = 'Conteúdo'
    hdr_cells[2].text = 'Eixo ENAMED'

    lista_temas = dados["temas"].split('\n')
    for i, tema in enumerate(lista_temas):
        if tema.strip():
            row = table.add_row().cells
            row[0].text = str(i+1)
            row[1].text = tema
            row[2].text = "Eixo XX/XVII (Verificar na Portaria 478)" # Sugestão padrão

    # Seção 3: Avaliação e Recuperação
    doc.add_heading('3. Sistema de Avaliação e Monitoria', level=1)
    doc.add_paragraph("Nota: 70% Prova (PreparaEdu) e 30% Atividades (UpToDate/Seminários).")
    doc.add_paragraph("Recuperação: Programa de Monitoria Oficial (Atendimento aluno-aluno).")
    
    filename = f"Plano_{dados['disciplina']}.docx"
    doc.save(filename)
    return filename

# --- 4. BOTÃO DE EXECUÇÃO ---
if st.button("🚀 GERAR MEU PLANO DE ENSINO"):
    if professor and disciplina and temas:
        dados_plano = {
            "professor": professor,
            "disciplina": disciplina,
            "temas": temas
        }
        arquivo = gerar_docx(dados_plano)
        
        with open(arquivo, "rb") as f:
            st.download_button("📥 Clique aqui para baixar o arquivo Google Docs (DOCX)", f, file_name=arquivo)
        st.success("Plano estruturado com sucesso!")
    else:
        st.warning("Preencha o nome do professor, disciplina e temas.")

# --- 5. VALIDADOR DE QUESTÕES ---
st.divider()
st.header("🏷️ Validador de Questões para PreparaEdu")
questao = st.text_area("Cole sua questão aqui para conferência:")
if st.button("Analisar Questão"):
    st.info("Lógica de Tagging: Esta questão deve ser salva no PreparaEdu com o Eixo correspondente ao conteúdo técnico inserido.")
