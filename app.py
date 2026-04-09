import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Настройка страницы
st.set_page_config(page_title="Franchise Calculator | Спортивный Покер", layout="wide")

# --- ФИРМЕННЫЙ CSS (из самого начала) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    section[data-testid="stSidebar"] {
        background-color: #1A1C23;
        border-right: 2px solid #D4AF37;
    }
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 { color: #D4AF37 !important; }
    section[data-testid="stSidebar"] label {
        color: #D4AF37 !important;
        font-weight: 500;
    }
    .stButton > button {
        background-color: #D4AF37;
        color: black;
        font-weight: bold;
        border-radius: 8px;
    }
    div[data-testid="metric-container"] {
        background-color: #1E222A;
        border: 1px solid #D4AF37;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Логотип
st.image("logo.png", width=250)

st.title("Калькулятор прибыльности франшизы")
st.markdown("---")

# --- БОКОВАЯ ПАНЕЛЬ ---
st.sidebar.header("📍 Параметры локации")

# 1. Трафик и продажи
vkhody = st.sidebar.slider("Количество входов игру в месяц", 500, 5000, 3000)
vkhody_price = st.sidebar.number_input("Средний чек (вход), руб.", value=1000)

# 2. Дополнительные услуги
st.sidebar.subheader("🍷 Доп. услуги")
bar_conv = st.sidebar.slider("Конверсия в бар, %", 0, 100, 40) / 100
bar_check = st.sidebar.number_input("Средний чек бара, руб.", value=900)
hookah_conv = st.sidebar.slider("Конверсия в кальяны, %", 0, 100, 15) / 100
hookah_check = st.sidebar.number_input("Средний чек кальяна, руб.", value=1200)

# 3. Расходы
st.sidebar.subheader("💸 Расходы и налоги")
rent = st.sidebar.number_input("Аренда + Коммуналка, руб.", value=200000)
marketing = st.sidebar.number_input("Маркетинг, руб.", value=350000)
staff_total = st.sidebar.number_input("ФОТ (весь персонал), руб.", value=1257000)
royalty_percent = st.sidebar.slider("Роялти (от выручки), %", 0, 10, 5) / 100

# 4. Инвестиции
investments = st.sidebar.number_input("Общие инвестиции, руб.", value=4000000)

# --- ЛОГИКА РАСЧЕТА ---
rev_vkhody = vkhody * vkhody_price
rev_bar = (vkhody * bar_conv) * bar_check
rev_hookah = (vkhody * hookah_conv) * hookah_check
total_revenue = rev_vkhody + rev_bar + rev_hookah + 50000  # +50к реклама

royalty_sum = total_revenue * royalty_percent
tax_usn = total_revenue * 0.06

total_opex = rent + marketing + staff_total + 500000 + royalty_sum
net_profit = total_revenue - tax_usn - total_opex

# --- МЕТРИКИ ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Выручка", f"{total_revenue:,.0f} ₽")
col2.metric("Чистая прибыль", f"{net_profit:,.0f} ₽", delta=f"{(net_profit/total_revenue)*100:.1f}% маржа")
col3.metric("Окупаемость", f"{investments/net_profit if net_profit > 0 else 0:.1f} мес.")
col4.metric("Роялти (вам)", f"{royalty_sum:,.0f} ₽")

st.markdown("---")

# --- ГРАФИК СТРУКТУРЫ ВЫРУЧКИ ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("Структура выручки")
    labels = ['Входы', 'Бар', 'Кальяны', 'Реклама']
    values = [rev_vkhody, rev_bar, rev_hookah, 50000]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Прогноз окупаемости")
    months = list(range(13))
    cash_flow = [-investments + (net_profit * m) for m in months]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=months, y=cash_flow, mode='lines+markers', name='Cash Flow'))
    fig2.add_hline(y=0, line_dash="dash", line_color="red")
    fig2.update_layout(xaxis_title="Месяцы", yaxis_title="Баланс, ₽")
    st.plotly_chart(fig2, use_container_width=True)
