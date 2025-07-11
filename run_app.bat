@echo off
echo Installing dependencies...
pip install streamlit openai pyperclip

echo.
echo Starting Streamlit app...
streamlit run app.py

pause
