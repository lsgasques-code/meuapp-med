# data_helper.py
# Consolidação da Matriz 2026 e Ementário UNIPAR
MODULOS_UNIPAR = {
    "Fundamentos da Prática Médica I (1ª Série)": {
        "serie": "1ª Série",
        "carga_horaria": "1.320h",
        "ementas": "Discussão Clínica Integradora (PBL), Habilidades Clínicas e Relação Médico-Paciente (BLS, Sinais Vitais), Anatomia Humana (Nomenclatura e Sistemas), Fisiologia (Membrana, Cardiovascular, Renal), Histologia, Embriologia, Citologia, Bioquímica e Saúde Coletiva.",
        "componentes": ["Anatomia I", "Fisiologia I", "Bioquímica", "Habilidades Clínicas I", "PBL I"],
        "ciclo": "Básico"
    },
    "Fundamentos da Prática Médica II (2ª Série)": {
        "serie": "2ª Série",
        "carga_horaria": "1.400h",
        "ementas": "Discussão Clínica Integradora II, Habilidades Clínicas (Exame Físico Específico, Abdome, Neurológico), Anatomia II (Topográfica), Fisiologia II (Integrativa), Microbiologia, Parasitologia, Biologia Molecular, Imunologia, Farmacologia Básica e Patologia Geral.",
        "componentes": ["Anatomia II", "Fisiologia II", "Micro/Para", "Farmaco Básica", "Patologia Geral"],
        "ciclo": "Básico"
    },
    "Clínica Integrada e Ciclos da Vida I (3ª Série)": {
        "serie": "3ª Série",
        "carga_horaria": "1.320h",
        "ementas": "Neurologia, Hematologia, Oncologia, Endocrinologia, Farmacologia Clínica, Técnicas Cirúrgicas, Saúde da Criança, Mulher e Idoso. Foco em raciocínio clínico e ambulatorial.",
        "componentes": ["Clínica Médica I", "Cirurgia I", "Saúde Coletiva III", "Farmaco Clínica"],
        "ciclo": "Clínico"
    },
    "Clínica Integrada e Ciclos da Vida II (4ª Série)": {
        "serie": "4ª Série",
        "carga_horaria": "1.320h",
        "ementas": "Pneumologia, Cardiologia, Nefrologia, Infectologia, Reumatologia, Emergências Clínicas e Medicina Intensiva, Gastroenterologia, Ginecologia e Pediatria Avançada.",
        "componentes": ["Clínica Médica II", "Cirurgia II", "Urgência e Emergência", "Cuidados Paliativos"],
        "ciclo": "Clínico"
    }
}

# Referência ENAMED (Portaria 478/2025)
ENAMED_AREAS = ["Clínica Médica", "Cirurgia Geral", "Ginecologia e Obstetrícia", "Pediatria", "Medicina da Família e Comunidade", "Saúde Mental", "Saúde Coletiva"]
