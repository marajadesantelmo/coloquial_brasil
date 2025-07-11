import streamlit as st
import time
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
    }
    .translation-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 1rem 0;
    }
    .input-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin: 1rem 0;
    }
    .stTextArea > div > div > textarea {
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🇪🇸 ➡️ 🇧🇷 Traductor a Portugués Brasileño Coloquial</h1>', unsafe_allow_html=True)

# Description
st.markdown("""
**¡Bienvenido!** Esta aplicación traduce frases del español al portugués brasileño coloquial.
Perfecto para conversaciones informales y expresiones cotidianas.
""")

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Texto en Español")
    
    # Text input area
    user_input = st.text_area(
        "Escribe la frase que quieres traducir:",
        height=150,
        placeholder="Ejemplo: ¿Cómo estás? ¿Qué tal si vamos a tomar algo?",
        key="spanish_input"
    )
    
    # Translation button
    translate_button = st.button(
        "🔄 Traducir",
        type="primary",
        use_container_width=True
    )

with col2:
    st.markdown("### 🇧🇷 Traducción al Portugués Brasileño")
    
    # Translation output
    if translate_button and user_input.strip():
        with st.spinner("Traduciendo... ⏳"):
            try:
                # Get translation from LLM
                translation = get_llm_response(user_input.strip())
                
                # Display translation
                st.markdown(f'<div class="translation-box"><h4>Traducción:</h4><p style="font-size: 18px; font-weight: 500;">{translation}</p></div>', unsafe_allow_html=True)
                
                # Store in session state for persistence
                st.session_state.last_translation = translation
                st.session_state.last_input = user_input.strip()
                
            except Exception as e:
                st.error(f"❌ Error al traducir: {str(e)}")
                st.info("💡 Verifica tu conexión a internet e intenta nuevamente.")
    
    elif translate_button and not user_input.strip():
        st.warning("⚠️ Por favor, escribe algo para traducir.")
    
    # Show last translation if available
    elif hasattr(st.session_state, 'last_translation'):
        st.markdown(f'<div class="translation-box"><h4>Última traducción:</h4><p style="font-size: 16px; color: #666;"><em>"{st.session_state.last_input}"</em></p><p style="font-size: 18px; font-weight: 500;">{st.session_state.last_translation}</p></div>', unsafe_allow_html=True)

# Separator
st.markdown("---")

# Examples section
st.markdown("### 💡 Ejemplos de uso")

examples = [
    {
        "spanish": "¿Qué tal si vamos a tomar unas cervezas?",
        "portuguese": "Que tal se a gente for tomar umas cervejas?"
    },
    {
        "spanish": "Estoy súper cansado, no puedo más",
        "portuguese": "Tô super cansado, não aguento mais"
    },
    {
        "spanish": "¡Qué genial! Me encanta esta canción",
        "portuguese": "Que massa! Adoro essa música"
    }
]

# Create example buttons
col_ex1, col_ex2, col_ex3 = st.columns(3)

with col_ex1:
    if st.button("🍺 Ejemplo 1", use_container_width=True):
        st.session_state.spanish_input = examples[0]["spanish"]
        st.rerun()

with col_ex2:
    if st.button("😴 Ejemplo 2", use_container_width=True):
        st.session_state.spanish_input = examples[1]["spanish"]
        st.rerun()

with col_ex3:
    if st.button("🎵 Ejemplo 3", use_container_width=True):
        st.session_state.spanish_input = examples[2]["spanish"]
        st.rerun()

# Show examples
for i, example in enumerate(examples, 1):
    with st.expander(f"📌 Ejemplo {i}"):
        st.markdown(f"**Español:** {example['spanish']}")
        st.markdown(f"**Portugués:** {example['portuguese']}")

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
