import streamlit as st
import time
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    st.warning("⚠️ Para usar la función de copiar al portapapeles, instala: pip install pyperclip")

from llm_connector import get_llm_response

# Page configuration
st.set_page_config(
    page_title="Traductor Español-Portugués Brasileño",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        color: #2E8B57;
        border-bottom: 2px solid #2E8B57;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #fafafa;
    }
    .copy-button {
        background-color: #2E8B57;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 0.5rem;
    }
    .copy-button:hover {
        background-color: #236B47;
    }
    
    /* Chat message styling for better contrast */
    .stChatMessage {
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* User messages - dark blue background */
    .stChatMessage[data-testid="chat-message-user"] {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border-left: 4px solid #3b82f6;
    }
    
    /* Assistant messages - dark green background */
    .stChatMessage[data-testid="chat-message-assistant"] {
        background-color: #1f2d23 !important;
        color: #ffffff !important;
        border-left: 4px solid #10b981;
    }
    
    /* Ensure text in chat messages is white */
    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #ffffff !important;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > div > div {
        background-color: #f8f9fa;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
    }
    
    /* Button styling in chat messages */
    .stChatMessage .stButton > button {
        background-color: #2E8B57;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.4rem 0.8rem;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .stChatMessage .stButton > button:hover {
        background-color: #236B47;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "¡Hola! 👋 Soy tu traductor de español a portugués brasileño coloquial. Escribe cualquier frase en español y te la traduciré al estilo informal brasileño."
    })

if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""

# Main title
st.markdown('<h1 class="main-header"> Bate-Papo </h1>', unsafe_allow_html=True)
st.markdown('<h2>Traductor a Portugués Brasileño Coloquial</h2>', unsafe_allow_html=True)

# Description
st.markdown("""
**¡Bienvenido!** Chatea conmigo para traducir frases del español al portugués brasileño coloquial.
Perfecto para conversaciones informales y expresiones cotidianas.
""")

# Chat interface
st.markdown("### 💬 Chat de Traducción")

# Display chat messages
chat_container = st.container()
with chat_container:
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Add copy button for assistant messages (translations)
            if message["role"] == "assistant" and message["content"] != st.session_state.messages[0]["content"]:
                if CLIPBOARD_AVAILABLE:
                    if st.button("📋 Copiar traducción", key=f"copy_msg_{idx}_{hash(message['content']) % 10000}"):
                        try:
                            pyperclip.copy(message["content"])
                            st.success("✅ ¡Traducción copiada al portapapeles!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error("❌ Error al copiar al portapapeles")
                else:
                    st.info("💡 Instala pyperclip para copiar al portapapeles: `pip install pyperclip`")

# Chat input
if prompt := st.chat_input("Escribe aquí tu frase en español..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display translation
    with st.chat_message("assistant"):
        with st.spinner("Traduciendo... ⏳"):
            try:
                translation = get_llm_response(prompt)
                st.markdown(translation)
                
                # Store latest translation
                st.session_state.last_translation = translation
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": translation})
                
                # Add copy button for the latest translation
                if CLIPBOARD_AVAILABLE:
                    if st.button("📋 Copiar traducción", key=f"copy_latest_{len(st.session_state.messages)}_{hash(translation) % 10000}"):
                        try:
                            pyperclip.copy(translation)
                            st.success("✅ ¡Traducción copiada al portapapeles!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error("❌ Error al copiar al portapapeles")
                else:
                    st.info("💡 Instala pyperclip para copiar: `pip install pyperclip`")
                
            except Exception as e:
                error_msg = f"❌ Error al traducir: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Clear chat button
if len(st.session_state.messages) > 1:
    if st.button("🗑️ Limpiar chat", type="secondary"):
        st.session_state.messages = [st.session_state.messages[0]]  # Keep only the initial message
        st.session_state.last_translation = ""
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Desarrollado con IA para traducciones naturales y coloquiales</p>
    <p><small>Tip: Las traducciones pueden variar según el contexto. ¡Experimenta con diferentes frases!</small></p>
</div>
""", unsafe_allow_html=True)