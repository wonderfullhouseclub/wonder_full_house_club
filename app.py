import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Франшиза Покер | Калькулятор", layout="wide")

# --- ЛОГОТИП (Замените URL на ссылку вашего логотипа) ---
st.image("https://i.ibb.co/0jQr3LQ/placeholder-logo.png", width=200) 
# Если картинка лежит локально в папке с app.py, напишите: st.image("logo.png", width=200)

st.title("📊 Калькулятор прибыльности франшизы «Спортивный Покер»")
st.markdown("---")

# --- БОКОВАЯ ПАНЕЛЬ ---
st.sidebar.header("📍 Параметры вашей точки")

# 1. Основные показатели
vkhody = st.sidebar.slider("🚪 Количество входов в месяц", 500, 5000, 2500, step=100)
vkhody_price = st.sidebar.number_input("🎫 Средний чек (вход), руб.", value=1000, step=100)

# 2. Маркетинг (CAC)
st.sidebar.subheader("📢 Маркетинг")
cac = st.sidebar.slider("Стоимость привлечения 1 гостя (CAC), руб.", 0, 1500, 350, step=50)
marketing_budget = vkhody * cac  # Автоматический расчет бюджета
st.sidebar.caption(f"Бюджет на маркетинг: {marketing_budget:,.0f} ₽".replace(",", " "))

# 3. Доп. услуги
st.sidebar.subheader("🍷 Доп. услуги")
bar_conv = st.sidebar.slider("Конверсия в бар, %", 0, 100, 35) / 100
bar_check = st.sidebar.number_input("Средний чек бара, руб.", value=900, step=100)

hookah_conv = st.sidebar.slider("Конверсия в кальяны, %", 0, 100, 15) / 100
hookah_check = st.sidebar.number_input("Средний чек кальяна, руб.", value=1200, step=100)

# 4. Детализированный ФОТ
st.sidebar.subheader("👥 Персонал")
col_a, col_b = st.sidebar.columns(2)
with col_a:
    num_dilers = st.number_input("Дилеров", min_value=1, value=6)
    num_admin = st.number_input("Администраторов", min_value=1, value=2)
with col_b:
    rate_diler = st.number_input("Ставка дилера/час", value=350)
    rate_admin = st.number_input("Ставка админа/час", value=250)

hours_per_month = 165  # Среднее кол-во рабочих часов в месяц
staff_total = (num_dilers * rate_diler * hours_per_month) + (num_admin * rate_admin * hours_per_month)
st.sidebar.caption(f"ФОТ (всего): {staff_total:,.0f} ₽".replace(",", " "))

# 5. Прочие расходы
st.sidebar.subheader("🏠 Постоянные расходы")
rent = st.sidebar.number_input("Аренда + Коммуналка, руб.", value=200000, step=10000)
royalty_percent = st.sidebar.slider("Роялти (от выручки), %", 0, 10, 5) / 100

# 6. НАЛОГОВЫЙ РЕЖИМ
st.sidebar.subheader("🧾 Налоги")
tax_mode = st.sidebar.selectbox(
    "Режим налогообложения",
    ["УСН 6% (Доходы)", "УСН 15% (Доходы - Расходы)", "Патент (фикс)"]
)

if tax_mode == "Патент (фикс)":
    patent_cost = st.sidebar.number_input("Стоимость патента в месяц", value=15000, step=1000)
else:
    patent_cost = 0

# Инвестиции
investments = st.sidebar.number_input("💰 Общие инвестиции, руб.", value=4_000_000, step=100_000)

# --- РАСЧЕТЫ ---
# Выручка
rev_vkhody = vkhody * vkhody_price
rev_bar = (vkhody * bar_conv) * bar_check
rev_hookah = (vkhody * hookah_conv) * hookah_check
rev_ads = 50000  # Фиксированный доход от рекламы
total_revenue = rev_vkhody + rev_bar + rev_hookah + rev_ads

# Расходы (без налогов)
royalty_sum = total_revenue * royalty_percent
other_opex = 500000  # Прочие операционные расходы (охрана, эквайринг и т.д.)
opex_without_tax = rent + marketing_budget + staff_total + other_opex + royalty_sum

# Расчет налога
if tax_mode == "УСН 6% (Доходы)":
    tax_amount = total_revenue * 0.06
elif tax_mode == "УСН 15% (Доходы - Расходы)":
    # При УСН 15% можно учесть почти все расходы (кроме рекламы? Для простоты считаем все)
    tax_base = total_revenue - opex_without_tax
    tax_amount = max(0, tax_base * 0.15)  # Налог не может быть отрицательным
else:  # Патент
    tax_amount = patent_cost

total_opex = opex_without_tax + tax_amount
net_profit = total_revenue - total_opex

# Окупаемость
if net_profit > 0:
    payback_months = investments / net_profit
else:
    payback_months = float('inf')

# --- ОТОБРАЖЕНИЕ ВЕРХНИХ МЕТРИК ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Выручка", f"{total_revenue:,.0f} ₽".replace(",", " "))
col2.metric("📈 Чистая прибыль", f"{net_profit:,.0f} ₽".replace(",", " "), 
            delta=f"{(net_profit/total_revenue)*100:.1f}% маржа" if total_revenue > 0 else "0%")
col3.metric("⏳ Окупаемость", 
            f"{payback_months:.1f} мес." if payback_months != float('inf') else "> 5 лет")
col4.metric("👑 Роялти (франчайзеру)", f"{royalty_sum:,.0f} ₽".replace(",", " "))

st.markdown("---")

# --- ГРАФИКИ ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("🧩 Структура выручки")
    labels = ['Входы', 'Бар', 'Кальяны', 'Реклама']
    values = [rev_vkhody, rev_bar, rev_hookah, rev_ads]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("📉 Прогноз движения денег")
    months = list(range(13))
    cash_flow = [-investments + (net_profit * m) for m in months]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=months, y=cash_flow, mode='lines+markers', name='Баланс'))
    fig_line.add_hline(y=0, line_dash="dash", line_color="red")
    fig_line.update_layout(xaxis_title="Месяц", yaxis_title="Накопленная прибыль, ₽")
    st.plotly_chart(fig_line, use_container_width=True)

# --- ДЕТАЛЬНАЯ ТАБЛИЦА (опционально) ---
with st.expander("📋 Детализация расходов"):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("**Статья расходов**")
        st.write(f"Аренда: {rent:,.0f} ₽".replace(",", " "))
        st.write(f"Маркетинг (CAC): {marketing_budget:,.0f} ₽".replace(",", " "))
        st.write(f"ФОТ: {staff_total:,.0f} ₽".replace(",", " "))
        st.write(f"Прочие ОПЕКС: {other_opex:,.0f} ₽".replace(",", " "))
        st.write(f"Роялти: {royalty_sum:,.0f} ₽".replace(",", " "))
    with col_d2:
        st.write("**Налоги**")
        st.write(f"Режим: {tax_mode}")
        st.write(f"Сумма налога: {tax_amount:,.0f} ₽".replace(",", " "))
        st.write("---")
        st.write(f"**Итого расходы: {total_opex:,.0f} ₽**".replace(",", " "))
