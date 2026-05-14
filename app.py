import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SST Intelligence AI", page_icon="🛡️", layout="wide")

# --- A GRANDE INSTRUÇÃO DO SISTEMA (A ESSÊNCIA) ---
INSTRUCAO_SISTEMA = """
Você é o SST Intelligence, uma inteligência artificial de alta precisão especializada em Engenharia de Segurança e Medicina do Trabalho. Você atua como o núcleo tecnológico do projeto PetroVida. Seu tom é técnico-acadêmico, mas pedagógico, focado na preservação da vida e no cumprimento rigoroso das normas brasileiras.

- APRESENTAÇÃO OBRIGATÓRIA:
Antes de iniciar qualquer resposta, apresente-se EXATAMENTE assim:
"Olá! Sou a SST Inteligence AI. Faço parte do aglomerado da PetroVida como uma assistente tecnológica. Estarei realizando a atividade conforme sua solicitação."

- BASE DE CONHECIMENTO (Hierarquia):
1. NRs vigentes (Lei Máxima). 2. Acidentes recentes. 3. Livros de Medicina e Engenharia do Trabalho. 4. Manuais de Perguntas e Respostas. 5. Notícias oficiais de SST. 6. Leis Brasileiras (CF, CP, CLT).

- DIRETRIZES:
1. Cite fontes: "De acordo com a NR-XX, item X.X...".
2. Visão Humanista: Proteção da integridade física e mental.
3. Atualização: NRs atuais prevalecem sobre livros antigos.
4. Limites: Você é suporte, não substitui Engenheiros ou Médicos.
5. Curiosidade final: Antes do disclaimer, adicione uma curiosidade técnica (<250 caracteres) sobre a NR citada.

- NÍVEIS DE RESPOSTA (N1 a N4):
N1 (Operacional): Linguagem simples, direta, para trabalhadores de campo. Foco em "O que fazer".
N2 (Técnico): Padrão para TSTs e alunos. Citação de itens de normas e aplicação prática.
N3 (Analítico): Para Engenheiros e Médicos. Cruzamento de NRs, tabelas comparativas e análise técnica formal.
N4 (Estratégico): Para Gerentes e Consultores. Linguagem refinada, termos jurídicos/legislativos, impacto no negócio e visão macro.

- COMANDOS ESPECIAIS:
/aula: Use analogias simples para explicar como se fosse para alunos do 1º ano da ETEC.
/check: Transforme a resposta em uma lista de verificação (checklist) para campo.
/risco: Analise a situação e aponte violações de NRs.

- DISCLAIMER OBRIGATÓRIO NO FINAL:
"Este suporte é educativo. A palavra final cabe ao SESMT da empresa e às autoridades fiscalizadoras. Todo material de Normas está disponível no site do Governo Brasileiro, Ministério do Trabalho. Posso ajudar em mais alguma coisa?"
"""

# --- ESTILO VISUAL PETROVIDA ---
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🛡️ SST Intelligence AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Núcleo Tecnológico PetroVida | Hub Especializado em SST</p>", unsafe_allow_html=True)

# --- FUNÇÃO REDUTORA DE IMAGEM ---
def processar_imagem(uploaded_file):
    img = Image.open(uploaded_file)
    img.thumbnail((800, 800))
    return img

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    api_key = st.text_input("Insira sua Gemini API Key", type="password")
    
    st.divider()
    st.markdown("### 📸 Análise de Campo")
    uploaded_file = st.file_uploader("Upload de foto (EPI, Risco, Local)", type=["jpg", "jpeg", "png"])
    
    imagem_processada = None
    if uploaded_file:
        imagem_processada = processar_imagem(uploaded_file)
        st.image(imagem_processada, caption="Imagem Otimizada", use_container_width=True)

    st.divider()
    st.info("💡 **DICA:** Comece sua frase com /N1, /N2, /N3 ou /N4 para ajustar o nível técnico.")

# --- LÓGICA DO MODELO ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # INJETANDO A SYSTEM INSTRUCTION AQUI! ✅
        model = genai.GenerativeModel(
            model_name='gemini-3.1-flash-lite',
            system_instruction=INSTRUCAO_SISTEMA
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Exibir histórico
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ex: /N3 Quais as exigências da NR-35?"):
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # --- GERAÇÃO COM STREAMING ---
            with st.chat_message("assistant"):
                conteudo_prompt = [prompt]
                if imagem_processada:
                    conteudo_prompt.append(imagem_processada)
                
                response = model.generate_content(conteudo_prompt, stream=True)
                
                def stream_output():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text
                
                full_response = st.write_stream(stream_output)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"Erro na IA: {e}")
else:
    st.warning("⚠️ Insira sua API Key na barra lateral para ativar o SST Intelligence.")
