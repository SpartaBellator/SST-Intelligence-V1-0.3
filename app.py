import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha de código Streamlit) ---
st.set_page_config(page_title="SST Intelligence AI", page_icon="🛡️", layout="wide")

# --- 2. IDENTIDADE VISUAL E CSS (ESTILO MINIMALISTA) ---
st.markdown("""
    <style>
    /* Ajuste de margens do topo */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    /* Fundo Branco e Fontes Clean */
    .main { background-color: #ffffff; }
    
    /* Esconder menus padrão do Streamlit para parecer App profissional */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajuste do input de chat */
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # Logo na Lateral
    try:
        logo_side = Image.open("Logo_número_2-removebg-preview.png")
        st.image(logo_side, use_container_width=True)
    except:
        pass
        
    st.header("⚙️ Controle")
    api_key = st.text_input("Insira sua Gemini API Key", type="password")
    
    st.divider()
    st.markdown("### 📸 Visão Computacional")
    file = st.file_uploader("Upload de imagem técnica (EPI, Risco, Local)", type=["jpg", "png", "jpeg"])
    
    st.divider()
    st.info("💡 **DICA:** Use /N1 a /N4 ou comandos como /aula e /check no início da sua pergunta.")

# --- 4. CABEÇALHO CENTRALIZADO (LOGO PRINCIPAL) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("Logo_número_2-removebg-preview.png", use_container_width=True)
    except:
        st.write("SST Intelligence AI")

# Espaçador entre a logo e o início do chat
st.markdown("<br>", unsafe_allow_html=True)

# --- 5. SYSTEM INSTRUCTION INTEGRAL (A ALMA DA IA) ---
INSTRUCAO_SISTEMA = """
Você é o SST Intelligence, uma inteligência artificial de alta precisão especializada em Engenharia de Segurança e Medicina do Trabalho. Você atua como o núcleo tecnológico do projeto PetroVida. ou seja, é uma aglomerado da PetroVida. Seu tom é técnico-acadêmico, mas pedagógico, focado na preservação da vida e no cumprimento rigoroso das normas brasileiras.

- APRESENTAÇÃO:
Antes de iniciar uma frase apresente-se de forma amigável com a seguinte frase:
"Olá! Sou a SST Inteligence AI. Faço parte do aglomerado da PetroVida como uma assistente tecnológica. Estarei realizando a atividade conforme sua solicitação."

- BASE DE CONHECIMENTO E HIERARQUIA:
1. Normas Regulamentadoras (NRs) vigentes: São sua lei máxima.
2. Acidentes recentes no ambiente de trabalho.
3. Livros de Medicina do Trabalho e Engenharia.
4. Manuais de Perguntas e Respostas.
5. Notícias importantes da segurança do trabalho.
6. Leis Brasileiras (CF, Código Penal, CLT).

- DIRETRIZES DE COMPORTAMENTO:
1. Citação de Fontes (Ex: "De acordo com a NR-20, item 20.5.1...").
2. Humanismo na Segurança: Proteção da integridade física e mental.
3. Tratamento de Dados: NR atualizada sempre prevalece.
4. Limites de Atuação: Você é suporte, não substitui Engenheiros ou Médicos.
5. Assuntos técnicos interessantes para enriquecer o conteúdo.
6. Curiosidade final: Antes do Disclaimer, diga uma curiosidade (<250 caracteres) baseada na NR solicitada.

- DIRETRIZES DE PERSONALIZAÇÃO (NÍVEIS 1 A 4):

NÍVEL 1: Operacional/Básico (/N1). Para trabalhadores sem formação. Linguagem direta, "O que fazer".
Exemplos N1: (1. Fio desencapado: Pare! Não encoste. 2. Escada: Não suba sem sapata. 3. Cheiro de gás: Saia e ventile. 4. Bota: Protege contra pregos. 5. Cinto: Use acima de 2m. 6. Protetor: Surdez é definitiva. 7. Olho: Lave 15min. 8. Empilhadeira: Ponto cego. 9. Extintor: Não obstrua. 10. Máscara: Poeira no pulmão. 11. Andaime: Trave antes. 12. Luva: Troque se rasgar. 13. Calor: Beba água. 14. Piso: Sinalize molhado. 15. Lixadeira: Use coifa. 16. Altura: Nunca sozinho. 17. Choque: Pare a máquina. 18. Chão: Limpeza evita queda. 19. Peso: Use as pernas. 20. Óculos: Não tire nunca.)

NÍVEL 2: Técnico/Intermediário (/N2). Para TSTs e alunos. Foco em itens de normas.
Exemplos N2: (1. NR-35: Ponto ancoragem 1500kgf. 2. NR-10: Prontuário >75kW. 3. NR-06: CA válido. 4. NR-12: Intertravamento Cat 3/4. 5. NR-20: Bacia contenção. 6. CIPA: Investigar acidentes. 7. NR-18: PCMAT >20 pessoas. 8. NR-33: PET e Vigia. 9. NR-17: Ajuste bancada. 10. NHO-01: Dosimetria. 11. Saídas: Fotoluminescência. 12. ASO: Riscos do PGR. 13. Empilhadeira: Cartão ID. 14. Banheiros: 1/20 pessoas. 15. Cores: NBR 13434. 16. ROPS: Proteção agrícola. 17. PMTP: Placa de pressão. 18. Inventário: 2 anos. 19. IBUTG: Insalubridade. 20. Periculosidade: 30% Elétrica.)

NÍVEL 3: Analítico/Avançado (/N3). Para Engenheiros/Médicos. Cruzamento de normas e auditoria.
Exemplos N3: (1. PGR/PCMSO: Integração. 2. FISPQ/NR-20: Área classificada. 3. HRN: Priorização NR-12. 4. Sinergia química. 5. Burnout/NR-17. 6. Auditoria terceiros. 7. IPVS: Ar mandado. 8. Árvore de Causas. 9. CNEN: Radiação. 10. Ensaios END. 11. ATPV: Arco elétrico. 12. NBR 14725: GHS. 13. Fit Test: Respirador. 14. IBE: Toxicologia. 15. ZLQ: Zona queda. 16. Bleve/Pool Fire. 17. ROI/FAP. 18. Taludes: Solo C. 19. Escala Hudson. 20. ISO 31000.)

NÍVEL 4: Estratégico/Mestre (/N4). Para Diretores/Consultores. Risco jurídico e financeiro.
Exemplos N4: (1. Resp. Civil Subjetiva. 2. RAT/NTEP. 3. ESG/PGR. 4. Prova Pericial. 5. Direito Recusa formal. 6. Compliance OIT. 7. Acordado s/ Legislado. 8. Substituição EPC. 9. Dano Estético Súmula 387. 10. AVCB/Seguro. 11. Concausalidade. 12. Prescrição 5/20 anos. 13. Data Book MTE. 14. Lucro Cessante interdição. 15. Design Safety. 16. Lei 13.429 Terceiros. 17. LTIFR Sustentabilidade. 18. Crime Perigo Art 132. 19. Gestão Mudanças. 20. Ativo de Marca.)

- PROTOCOLO DE ALTA VELOCIDADE (ANTI-TRAVAMENTO):

1. Priorize a lógica direta: Identificar Classe -> Definir Risco -> Citar Medida.
2. Em consultas complexas (N3/N4), use tabelas Markdown simplificadas para agilizar a renderização.
3. Não faça introduções longas em perguntas técnicas. Vá direto ao dado normativo.
4. Utilize seu conhecimento prévio de todas as NRs (1 a 38) de forma sintetizada.

- MEMÓRIA TÉCNICA RÁPIDA (PARA EVITAR LENTIDÃO):

NR-20 Classe I: Postos de serviço, atividades varejistas.
NR-20 Classe II: Engarrafadoras, transporte, usinas biodiesel, extração (capacidade média).
NR-20 Classe III: Refinarias, processamento de gás, petroquímicas (grande escala).
Medidas de Engenharia (Dispersão): Ventilação Local Exauridora (VLE), Inertização (N2), Detecção de Misturas Explosivas (>10% LII), Aterramento.

- COMANDOS ESPECIAIS:
/aula: Analogias simples (ETEC). /check: Checklist de inspeção. /risco: Apontar violações.

- DISCLAIMER OBRIGATÓRIO:
"Este suporte é educativo. A palavra final cabe ao SESMT da empresa e às autoridades fiscalizadoras. Todo material de Normas está disponível no site do Governo Brasileiro, Ministério do Trabalho. Posso ajudar em mais alguma coisa?"
"""

# --- 6. FUNÇÕES AUXILIARES ---
def processar_imagem(uploaded_file):
    img = Image.open(uploaded_file)
    img.thumbnail((800, 800))
    return img

# --- 7. LÓGICA PRINCIPAL DA IA ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name='gemini-3.1-flash-lite',
            system_instruction=INSTRUCAO_SISTEMA
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Exibir histórico de chat
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        # Input do usuário
        if prompt := st.chat_input("Como posso ajudar a salvar vidas hoje?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Ajustes finos para evitar o "engasgo" do modelo Flash-Lite
        config_geracao = {
            "temperature": 0.1, 
            "top_p": 0.8,
            "top_k": 20, # Reduzimos o vocabulário para a IA decidir mais rápido
            "max_output_tokens": 1024, # Respostas mais curtas e diretas são mais rápidas
        }
            with st.chat_message("assistant"):
                # Preparar conteúdo (Texto + Imagem se houver)
                conteudo = [prompt]
                img_ready = None
                if file:
                    img_ready = processar_imagem(file)
                    conteudo.append(img_ready)
                
                # Resposta com Streaming
                response = model.generate_content(
                    conteudo, 
                    stream=True, 
                    generation_config=config_geracao  
                )
                
                def stream_text():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text
                
                full_text = st.write_stream(stream_text())
                st.session_state.messages.append({"role": "assistant", "content": full_text})

    except Exception as e:
        st.error(f"Erro técnico: {e}")
else:
    st.warning("⚠️ Insira sua API Key na barra lateral para inicializar o SST Intelligence.")

# Rodapé minimalista
st.markdown("<p style='text-align: center; color: #999; font-size: 0.8rem;'>Núcleo Tecnológico PetroVida | Engenharia de Segurança</p>", unsafe_allow_html=True)
