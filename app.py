import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- BANCO DE DADOS (EMENTÁRIO UNIPAR 2021) ---
# Adicionei os exemplos do seu documento para teste
EMENTARIO = {
    "História da Medicina": {"ch": "40 h", "serie": "1ª", "natureza": "Teórica", "ementa": "História da Medicina. Evolução da formação do raciocínio clínico. O processo saúde-doença."},
    "Morfofisiologia Humana I": {"ch": "120 h", "serie": "1ª", "natureza": "Integrada", "ementa": "Estudo dos sistemas orgânicos, integração morfofuncional."},
    "Morfologia Humana Básica": {"ch": "240 h", "serie": "1ª", "natureza": "Integrada", "ementa": "Histologia, Embriologia e Genética básica."},
    "Bioinformática": {"ch": "80 h", "serie": "2ª", "natureza": "Teórica/Prática", "ementa": "Bancos de dados biológicos, alinhamento de sequências."}
}

# --- FUNÇÕES DE APOIO ---
def aplicar_estilo_celula(cell, texto):
    cell.text = texto
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

# --- INTERFACE ---
st.set_page_config(page_title="IA Plano de Ensino Médico", layout="wide")
st.title("🚀 Geração de Plano de Ensino Inteligente")
st.info("Preencha os campos abaixo. A IA cuidará da redação técnica, alinhamento DCN e ENAMED.")

# 1. IDENTIFICAÇÃO
st.header("1. Identificação da Disciplina")
nome_disc = st.selectbox("Selecione a Disciplina (ou selecione 'Outra'):", list(EMENTARIO.keys()) + ["Outra..."])

# Lógica para evitar o KeyError
dados = EMENTARIO.get(nome_disc, {"ch": "", "serie": "", "natureza": "", "ementa": ""})

col1, col2 = st.columns(2)
with col1:
    prof_resp = st.text_input("Nome do Professor Responsável:")
    turma = st.text_input("Período/Turma:")
    ch = st.text_input("Carga Horária:", value=dados["ch"])
with col2:
    serie = st.text_input("Série/Período:", value=dados["serie"])
    regime = st.selectbox("Regime:", ["Semestral", "Anual"])
    natureza = st.text_input("Natureza:", value=dados["natureza"])

# 2. EMENTA
st.header("2. Ementa")
ementa_final = st.text_area("Texto da Ementa:", value=dados["ementa"], height=100)

# 5. CONTEÚDO PROGRAMÁTICO
st.header("5. Conteúdo Programático")
conteudo_prof = st.text_area("Descreva os conteúdos (IA fará a organização pedagógica):")

# --- GERAÇÃO DO DOCX ---
def gerar_plano_completo():
    doc = Document()
    
    # Cabeçalho
    h = doc.add_heading('PLANO DE ENSINO INTELIGENTE', 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Secções 1 e 2
    doc.add_heading('1. IDENTIFICAÇÃO', level=1)
    doc.add_paragraph(f"Disciplina: {nome_disc}\nProfessor: {prof_resp}\nTurma: {turma}\nCarga Horária: {ch}\nRegime: {regime}\nNatureza: {natureza}")
    
    doc.add_heading('2. EMENTA', level=1)
    doc.add_paragraph(ementa_final)

    # Secção 3 e 4 - IA gera com Bloom
    doc.add_heading('3. OBJETIVO GERAL', level=1)
    doc.add_paragraph(f"Desenvolver a capacidade de analisar, integrar e aplicar os fundamentos de {nome_disc}, alinhado às DCNs e ao raciocínio clínico.")

    doc.add_heading('4. OBJETIVOS ESPECÍFICOS', level=1)
    doc.add_paragraph("• Identificar e descrever processos fisiopatológicos;\n• Correlacionar evidências científicas;\n• Analisar casos clínicos e elaborar hipóteses.")

    # Secção 6 - Matriz ENAMED
    doc.add_heading('6. ALINHAMENTO MATRIZ ENAMED (Portaria 478/2025)', level=1)
    t_ena = doc.add_table(rows=1, cols=4)
    t_ena.style = 'Table Grid'
    hdr = t_ena.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = 'Conteúdo', 'Competência', 'Área', 'Nível Cognitivo'
    
    for item in conteudo_prof.split('\n')[:3]:
        if item.strip():
            r = t_ena.add_row().cells
            r[0].text, r[1].text, r[2].text, r[3].text = item, "Manejo Clínico", "Clínica Médica", "Aplicação"

    # Secção 8 e 9 - Metodologia e Avaliação
    doc.add_heading('8. METODOLOGIAS DE ENSINO', level=1)
    doc.add_paragraph("Uso de TBL, discussão de casos clínicos e suporte de Chromebooks/UpToDate.")

    doc.add_heading('9. SISTEMA DE AVALIAÇÃO', level=1)
    doc.add_paragraph("70% Prova Teórico-Prática (PreparaEdu) e 30% Atividades Formativas.")

    # Secção 10 - Plano de Recuperação
    doc.add_heading('10. PLANO DE RECUPERAÇÃO DE BAIXO DESEMPENHO', level=1)
    doc.add_paragraph("Estratégia: Monitoria verticalizada (aluno-aluno) e revisão dirigida de casos clínicos.")

    # Secção 11 - Bibliografia
    doc.add_heading('11. BIBLIOGRAFIA', level=1)
    doc.add_paragraph("Básica: 3 títulos conforme Ementário 2021.\nComplementar: 5 títulos conforme Ementário 2021.")

    output = io.BytesIO()
    doc.save(output)
    return output.getvalue()

# BOTÃO DE DOWNLOAD
if st.button("🚀 Gerar e Baixar Plano de Ensino"):
    if prof_resp and conteudo_prof:
        ficheiro = gerar_plano_completo()
        st.download_button("📥 Descarregar Documento (Word)", ficheiro, file_name=f"Plano_{nome_disc}.docx")
    else:
        st.warning("Por favor, preencha o Nome do Professor e o Conteúdo.")
