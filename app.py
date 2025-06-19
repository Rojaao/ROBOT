import streamlit as st
from deriv_bot import DerivBot

st.set_page_config(page_title="Robô Deriv Estratégias", layout="centered")

st.title("🤖 Robô Deriv.com - Estratégias Automatizadas")

st.markdown("Configure os parâmetros abaixo e clique em **Iniciar Robô** para começar as operações.")

# Configurações
token = st.text_input("🔐 Token da API Deriv", type="password")
strategy = st.selectbox("🎯 Estratégia", ["0 Absoluto", "4 Acima", "4 Plus"])
stake = st.number_input("💵 Stake Inicial (USD)", min_value=0.35, value=1.00, step=0.01)
martingale = st.number_input("♻️ Fator Martingale", min_value=1.0, value=2.0, step=0.1)
max_losses = st.number_input("⛔ Máximo de Perdas Consecutivas", min_value=1, value=3, step=1)
max_loss = st.number_input("📉 Limite Máximo de Prejuízo (USD)", min_value=0.0, value=10.0, step=0.5)
target_profit = st.number_input("📈 Meta de Lucro (USD)", min_value=0.0, value=5.0, step=0.5)

start = st.button("🚀 Iniciar Robô")

# Execução fictícia (substituir com thread real para produção)
if start:
    if not token:
        st.error("Você precisa inserir seu token da API.")
    else:
        st.success("Robô iniciado com sucesso!")
        st.markdown(f"**Estratégia ativa:** `{strategy}`")
        st.markdown(f"**Stake Inicial:** ${stake:.2f}")
        st.markdown(f"**Martingale:** x{martingale}")
        st.markdown(f"**Limite de Perdas Consecutivas:** {max_losses}")
        st.markdown(f"**Loss Máximo:** ${max_loss:.2f}")
        st.markdown(f"**Meta de Lucro:** ${target_profit:.2f}")
        st.info("⚠️ O robô rodará em segundo plano. Esta interface ainda não executa operações reais.")
        # Aqui poderia ser rodado: bot = DerivBot(...) e bot.run()