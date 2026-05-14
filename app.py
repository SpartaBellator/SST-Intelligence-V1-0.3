import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SST Intelligence AI", page_icon="🛡️", layout="centered")

# Estilo Visual PetroVida
st.markdown("<h1 style='text-align: center;'>🛡️ SST Intelligence AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Núcleo Tecnológico PetroVida | Engenharia de Segurança</p>", unsafe_allow_html=True)
st.markdown("---")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Insira sua Gemini API Key", type="password")
    st.info("Modelo ativo: Gemini 3.1 Flash-Lite")
    st.divider()
    st.markdown("### Equipe do Projeto\n- Samuel\n- João Manuel")

# --- REGRAS DO SISTEMA (Baseado no seu Colab) ---
REGRAS = """
Você é o SST Intelligence AI da PetroVida. 
Sempre comece com: 'Olá! Sou a SST Inteligence AI. Faço parte do aglomerado da PetroVida como uma assistente tecnológica.'
Use as NRs (Normas Regulamentadoras) como base técnica.
Ao final de toda resposta, coloque o aviso: 'Este suporte é educativo. A palavra final cabe ao SESMT da empresa.'
"""

# --- LÓGICA DO CHAT ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # O modelo que funcionou ontem! ✅
        model = genai.GenerativeModel('gemini-3.1-flash-lite')

        # Inicializa o histórico de mensagens
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Exibe as mensagens salvas
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Campo de entrada do usuário
        if prompt := st.chat_input("Como posso ajudar com a segurança hoje?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Combinando as regras com a pergunta
                prompt_completo = f"{REGRAS}\n\nPergunta do usuário: {prompt}"
                
                # Gerando a resposta
                response = model.generate_content(prompt_completo)
                texto_final = response.text
                
                st.markdown(texto_final)
                st.session_state.messages.append({"role": "assistant", "content": texto_final})

    except Exception as e:
        st.error(f"Erro de conexão: {e}")
else:
    st.warning("⚠️ Insira sua API Key na barra lateral para ativar a IA.")
