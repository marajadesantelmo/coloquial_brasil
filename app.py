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
    initial_sidebar_state="expanded"
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
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "¡Hola! 👋 Soy tu traductor de español a portugués brasileño coloquial. Escribe cualquier frase en español y te la traduciré al estilo informal brasileño. ¡Vamos a empezar!"
    })

if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""

# Main title
st.markdown('<h1 class="main-header">🇪🇸 ➡️ 🇧🇷 Traductor a Portugués Brasileño Coloquial</h1>', unsafe_allow_html=True)

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
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Add copy button for assistant messages (translations)
            if message["role"] == "assistant" and message["content"] != st.session_state.messages[0]["content"]:
                if CLIPBOARD_AVAILABLE:
                    if st.button("📋 Copiar traducción", key=f"copy_{len(st.session_state.messages)}_{message['content'][:20]}"):
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
                    if st.button("📋 Copiar traducción", key=f"copy_latest_{len(st.session_state.messages)}"):
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

# Separator
st.markdown("---")

# Examples section
st.markdown("### 💡 Ejemplos de uso")

examples = [
    "¿Qué tal si vamos a tomar unas cervezas?",
    "Estoy súper cansado, no puedo más",
    "¡Qué genial! Me encanta esta canción",
    "¿Tienes ganas de salir a dar una vuelta?",
    "Está lloviendo a cántaros",
    "No me vengas con cuentos"
]

# Create example buttons
cols = st.columns(3)
for i, example in enumerate(examples):
    col_idx = i % 3
    with cols[col_idx]:
        if st.button(f"📝 {example[:20]}...", key=f"example_{i}", use_container_width=True):
            # Add example to chat
            st.session_state.messages.append({"role": "user", "content": example})
            
            # Get translation
            try:
                translation = get_llm_response(example)
                st.session_state.messages.append({"role": "assistant", "content": translation})
                st.session_state.last_translation = translation
                st.rerun()
            except Exception as e:
                error_msg = f"❌ Error al traducir: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Desarrollado con IA para traducciones naturales y coloquiales</p>
    <p><small>Tip: Las traducciones pueden variar según el contexto. ¡Experimenta con diferentes frases!</small></p>
</div>
""", unsafe_allow_html=True)

# Sidebar with additional info
with st.sidebar:
    st.markdown("## ℹ️ Información")
    st.markdown("""
    **¿Cómo funciona?**
    
    1. 💬 Escribe tu frase en el chat
    2. ⏎ Presiona Enter para enviar
    3. 🇧🇷 Obtén la traducción coloquial
    4. 📋 Copia al portapapeles si necesitas
    
    **Características:**
    - ✅ Interfaz de chat intuitiva
    - ✅ Traducciones naturales
    - ✅ Estilo coloquial brasileño
    - ✅ Expresiones cotidianas
    - ✅ Historial de conversación
    - ✅ Función copiar al portapapeles
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Consejos")
    st.markdown("""
    - Usa frases completas para mejores resultados
    - Incluye contexto cuando sea necesario
    - Prueba diferentes expresiones
    - Usa los ejemplos como punto de partida
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Estadísticas de la sesión")
    translation_count = len([msg for msg in st.session_state.messages if msg["role"] == "assistant"]) - 1
    st.metric("Traducciones realizadas", translation_count)
    
    if st.session_state.last_translation and CLIPBOARD_AVAILABLE:
        st.markdown("### 📋 Última traducción")
        if st.button("📋 Copiar última traducción", use_container_width=True):
            try:
                pyperclip.copy(st.session_state.last_translation)
                st.success("✅ ¡Copiado!")
            except Exception as e:
                st.error("❌ Error al copiar")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Desarrollado con IA para traducciones naturales y coloquiales</p>
    <p><small>Tip: Las traducciones pueden variar según el contexto. ¡Experimenta con diferentes frases!</small></p>
</div>
""", unsafe_allow_html=True)

# Sidebar with additional info
with st.sidebar:
    st.markdown("## ℹ️ Información")
    st.markdown("""
    **¿Cómo funciona?**
    
    1. 📝 Escribe tu frase en español
    2. 🔄 Haz clic en "Traducir"
    3. 🇧🇷 Obtén la traducción coloquial
    
    **Características:**
    - ✅ Traducciones naturales
    - ✅ Estilo coloquial brasileño
    - ✅ Expresiones cotidianas
    - ✅ Contexto conversacional
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Consejos")
    st.markdown("""
    - Usa frases completas para mejores resultados
    - Incluye contexto cuando sea necesario
    - Prueba diferentes expresiones
    """)
