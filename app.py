import streamlit as st
import google.generativeai as genai

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Regista AI", page_icon="🎬", layout="centered")

# --- RECUPERO CHIAVI E PROMPT (DAI SEGRETI) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    system_prompt_base = st.secrets["SYSTEM_PROMPT"]
except FileNotFoundError:
    st.error("Errore: Chiavi non trovate. Configura i 'Secrets' su Streamlit Cloud.")
    st.stop()

genai.configure(api_key=api_key)

# --- STILE CSS ---
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 16px; font-family: sans-serif;}
    .stButton button {width: 100%; background-color: #FF4B4B; color: white; font-weight: bold;}
    div[data-testid="stMarkdownContainer"] h1 {font-family: 'Courier New', monospace;}
    </style>
    """, unsafe_allow_html=True)

# --- INTERFACCIA ---
st.title("🎬 V-KIT: REGISTA")
st.markdown("**Powered by Granello Protocol** | *Status: ONLINE*")

with st.expander("ℹ️ Istruzioni e Modalità"):
    st.markdown("""
    Questo sistema simula un Direttore Creativo esperto.
    - **Sii diretto.**
    - **Usa i selettori** per cambiare l'umore del Regista.
    """)

# Selettore Modalità
mode = st.selectbox("Imposta Tono Regista:", 
    ["DEFAULT (Creativo Autorevole)", 
     "MODE: SERGEANT (Duro/Disciplina)", 
     "MODE: MENTOR (Empatico/Guida)", 
     "MODE: BRAINSTORM (Caotico/Idee)"])

# Input
user_input = st.text_area("Il tuo Brief / Domanda:", height=150, placeholder="Es: Il cliente vuole il logo più grande, come rispondo senza insultarlo?")

# Logica di Esecuzione
if st.button("CIAK - Genera Risposta"):
    if not user_input:
        st.warning("Silenzio sul set. Scrivi qualcosa prima di girare.")
    else:
        with st.spinner("Il Regista sta elaborando la scena..."):
            try:
                # Costruzione Prompt Dinamico
                full_prompt = f"""
                {system_prompt_base}
                
                [IMPOSTAZIONI ATTUALI]
                L'utente ha scelto il tono: {mode}
                
                [INPUT UTENTE]
                {user_input}
                """
                
                # Chiamata a Gemini (Flash è veloce ed economico)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(full_prompt)
                
                # Output
                st.markdown("### 📝 Risposta:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Errore tecnico: {e}")

st.markdown("---")
st.caption("🔒 Private System - Non distribuire questo link pubblicamente.")
