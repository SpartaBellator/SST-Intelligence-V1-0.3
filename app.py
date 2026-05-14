import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="SST Intelligence AI", page_icon="🛡️", layout="wide")

# --- DICIONÁRIO DE NÍVEIS (Sua escala N1-N4) ---
NIVEIS_RESPOSTA = {
    "N1": "NÍVEL 1 (Básico): Responda de forma simples, direta e didática para um trabalhador iniciante.",
    "N2": "NÍVEL 2 (Intermediário): Responda com foco em procedimentos operacionais e técnicos da norma.",
    "N3": "NÍVEL 3 (Avançado): Responda com foco em gestão, responsabilidades legais e documentação do SESMT.",
    "N4": "NÍVEL 4 (Especialista/Auditoria): Responda com análise crítica, cruzamento de normas e foco em fiscalização."
}

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    api_key = st.text_input("Insira sua Gemini API Key", type="password")
    st.divider()
    st.markdown("### 📸 Análise de Imagem")
    uploaded_file = st.file_uploader("Envie uma foto para análise", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Imagem carregada", use_column_width=True)
    st.divider()
    st.info("💡 Use N1, N2, N3 ou N4 no início da pergunta para definir o nível de profundidade.")

# --- REGRAS DO SISTEMA ---
REGRAS_BASE = """
Você é o SST Intelligence AI da PetroVida.
Sempre comece com: 'Olá! Sou a SST Inteligence AI da PetroVida.'
Use as NRs como base técnica.
Ao final, use o disclaimer: 'Este suporte é educativo. A palavra final cabe ao SESMT da empresa.'
"""

# --- LÓGICA DO CHAT ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.1-flash-lite')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ex: N1 O que é EPI?"):
            
            # --- DETECÇÃO DO NÍVEL N1, N2, N3 ou N4 ---
            instrucao_nivel = "NÍVEL PADRÃO: Responda de forma equilibrada."
            comando_detectado = prompt.split()[0].upper() # Pega a primeira palavra
            
            if comando_detectado in NIVEIS_RESPOSTA:
                instrucao_nivel = NIVEIS_RESPOSTA[comando_detectado]
                # Remove o "N1" do texto da pergunta para não confundir a IA
                pergunta_limpa = " ".join(prompt.split()[1:])
            else:
                pergunta_limpa = prompt

            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                prompt_final = [f"{REGRAS_BASE}\n\n{instrucao_nivel}\n\nPergunta: {pergunta_limpa}"]
                
                if uploaded_file:
                    prompt_final.append(img)
                
                response = model.generate_content(prompt_final)
                texto_final = response.text
                
                st.markdown(texto_final)
                st.session_state.messages.append({"role": "assistant", "content": texto_final})

    except Exception as e:
        st.error(f"Erro técnico: {e}")
else:
    st.warning("⚠️ Aguardando API Key.")
