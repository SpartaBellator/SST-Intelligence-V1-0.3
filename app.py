import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SST Intelligence AI", page_icon="🛡️", layout="wide")

# Estilo Visual PetroVida
st.markdown("<h1 style='text-align: center;'>🛡️ SST Intelligence AI - Alta Performance</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Núcleo Tecnológico PetroVida | Resposta em Tempo Real</p>", unsafe_allow_html=True)

# --- DICIONÁRIO DE NÍVEIS N1-N4 ---
NIVEIS_RESPOSTA = {
    "N1": "NÍVEL 1 (Básico): Responda de forma simples e direta para um trabalhador iniciante.",
    "N2": "NÍVEL 2 (Intermediário): Responda com foco em procedimentos operacionais técnicos.",
    "N3": "NÍVEL 3 (Avançado): Responda com foco em gestão, normas e documentação SESMT.",
    "N4": "NÍVEL 4 (Especialista): Responda com análise técnica profunda e foco em auditoria."
}

# --- FUNÇÃO PARA REDUZIR IMAGEM ---
def processar_imagem(uploaded_file):
    img = Image.open(uploaded_file)
    # Redimensiona mantendo a proporção (máximo 800px de largura/altura)
    img.thumbnail((800, 800))
    return img

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Insira sua Gemini API Key", type="password")
    
    st.divider()
    st.markdown("### 📸 Visão Computacional")
    uploaded_file = st.file_uploader("Upload de foto para análise técnica", type=["jpg", "jpeg", "png"])
    
    imagem_processada = None
    if uploaded_file:
        imagem_processada = processar_imagem(uploaded_file)
        st.image(imagem_processada, caption="Imagem Otimizada", use_container_width=True)
        st.success("Imagem reduzida para processamento rápido!")

    st.divider()
    st.info("💡 Use N1, N2, N3 ou N4 no início da pergunta.")

# --- REGRAS DO SISTEMA ---
REGRAS_BASE = """
Você é o SST Intelligence AI da PetroVida.
Sempre comece com: 'Olá! Sou a SST Inteligence AI da PetroVida.'
Baseie-se nas NRs. Se houver imagem, analise conformidade técnica.
FINAL: 'Este suporte é educativo. A palavra final cabe ao SESMT da empresa.'
"""

# --- LÓGICA DO CHAT ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.1-flash-lite')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Histórico de Chat
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Como posso ajudar?"):
            
            # Detecção de Nível
            instrucao_nivel = "NÍVEL PADRÃO: Resposta técnica equilibrada."
            palavras = prompt.split()
            if palavras and palavras[0].upper() in NIVEIS_RESPOSTA:
                instrucao_nivel = NIVEIS_RESPOSTA[palavras[0].upper()]
                pergunta_corpo = " ".join(palavras[1:])
            else:
                pergunta_corpo = prompt

            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # --- GERAÇÃO COM STREAMING ---
            with st.chat_message("assistant"):
                conteudo_prompt = [f"{REGRAS_BASE}\n\n{instrucao_nivel}\n\nPergunta: {pergunta_corpo}"]
                
                if imagem_processada:
                    conteudo_prompt.append(imagem_processada)
                
                # Chamada com Streaming ativo
                response = model.generate_content(conteudo_prompt, stream=True)
                
                # Função geradora para o Streamlit "digitar" na tela
                def stream_output():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text
                
                full_response = st.write_stream(stream_output)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
else:
    st.warning("⚠️ Insira a API Key para começar.")
