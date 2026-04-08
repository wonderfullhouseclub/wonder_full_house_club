import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="Финансовая модель | Wonder Full House Club", layout="wide")

# --- ФИРМЕННЫЙ CSS (ЧЁРНЫЙ + ОРАНЖЕВЫЙ) ---
st.markdown("""
<style>
    /* Основной фон */
    .stApp {
        background-color: #ECF0ED;
    }
    /* Боковая панель */
    section[data-testid="stSidebar"] {
        background-color: #171717;
        border-right: 2px solid #FF4C24;
    }
    /* Заголовки */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        color: #FF4C24 !important;
    }    
        /* Цвет подписей к полям в боковой панели */
    section[data-testid="stSidebar"] label {
        color: #ECF0ED !important;
        font-weight: 500;
    }
    /* Кнопки */
    .stButton > button {
        background-color: #D4AF37;
        color: black;
        font-weight: bold;
        border-radius: 8px;
    }
    /* Метрики */
    div[data-testid="metric-container"] {
        background-color: #5F6367;
        border: 1px solid #5F6367;
        border-radius: 10px;
        padding: 10px;
    }   
    /* Цвет подписей (caption) в боковой панели */
    section[data-testid="stSidebar"] .stCaption {
        color: #D4AF37 !important;
        font-weight: 400;
    }
    /* Цвет выделенного жирного текста в боковой панели */
    section[data-testid="stSidebar"] strong {
        color: #FF4C24 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ЛОГОТИП ---
# Убедитесь, что файл logo.png лежит в репозитории рядом с app.py
st.image("logo.png", width=250)
st.markdown("""
<div style="line-height: 1.2;">
    <h1 style="margin: 0; padding: 0;">Финансовая модель</h1>
    <h1 style="margin: 0; padding: 0;">Вашего клуба спортивного покера</h1>
</div>
""", unsafe_allow_html=True)

# Добавьте небольшой отступ перед метриками
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# --- 1. ФОРМАТ КЛУБА ---
st.sidebar.subheader("🎲 Формат клуба")
club_format = st.sidebar.selectbox(
    "Выберите формат",
    ["STRAIGHT (5–10 столов)", "FULL HOUSE (11–24 стола)", "ROYAL FLASH (25+ столов)"]
)
if club_format.startswith("STRAIGHT"):
    min_v, max_v, def_v = 800, 2000, 1400
elif club_format.startswith("FULL HOUSE"):
    min_v, max_v, def_v = 2000, 4500, 3200
else:
    min_v, max_v, def_v = 4000, 8000, 6000

vkhody = st.sidebar.slider("🚪 Количество входов в месяц", min_v, max_v, def_v, step=50)
vkhody_price = st.sidebar.number_input("🎫 Средний чек (вход), руб.", value=1000, step=100)

# --- 2. УРОВЕНЬ ПОДДЕРЖКИ (перенесён выше) ---
st.sidebar.subheader("🤝 Уровень поддержки")
support_level = st.sidebar.selectbox(
    "Выберите пакет",
    ["Pro (роялти 10%)", "VIP (роялти 15%)", "Partner (50% от прибыли)"]
)
# Ставки роялти будут использоваться позже в расчётах

# --- 3. ДОП. УСЛУГИ ---
st.sidebar.subheader("🍷 Доп. услуги")
bar_conv = st.sidebar.slider("Конверсия в бар, %", 0, 100, 35) / 100
bar_check = st.sidebar.number_input("Средний чек бара, руб.", value=900, step=100)
hookah_conv = st.sidebar.slider("Конверсия в кальяны, %", 0, 100, 15) / 100
hookah_check = st.sidebar.number_input("Средний чек кальяна, руб.", value=1200, step=100)

# --- 4. ПОСТОЯННЫЕ РАСХОДЫ (переработаны) ---
st.sidebar.subheader("🏠 Постоянные расходы")

# Аренда
rent = st.sidebar.number_input("Аренда + коммунальные платежи, руб.", value=200000, step=10000)

# Операционные расходы
other_opex = st.sidebar.slider("💡 Операционные расходы (уборка, охрана, материалы), руб.",
                               min_value=100000, max_value=1500000, value=500000, step=50000)

# Маркетинг (общий бюджет, без CAC)
marketing_budget = st.sidebar.slider("📢 Маркетинговый бюджет, руб.",
                                     min_value=50000, max_value=1000000, value=200000, step=10000)

# Налоговый режим с выбором ИП/ООО
tax_mode = st.sidebar.selectbox(
    "🧾 Налоговый режим",
    ["УСН 6% (Доходы)", "УСН 15% (Доходы - Расходы)", "ОСНО (25% на прибыль, без НДС)"]
)

# --- 5. ПЕРСОНАЛ (компактный двухколоночный) ---
st.sidebar.subheader("👥 Персонал")
with st.sidebar.expander("Настроить ФОТ", expanded=False):
    c1, c2 = st.columns([2, 1])
    with c1:
        num_dilers = st.number_input("Дилеров", min_value=1, value=6)
        num_tour = st.number_input("Турнирных менеджеров", min_value=1, value=2)
        num_senior = st.number_input("Старших менеджеров", min_value=0, value=1)
    with c2:
        rate_diler = st.number_input("Ставка / час", value=350, key="rate_diler")
        rate_tour = st.number_input("Ставка / час", value=250, key="rate_tour")
        rate_senior = st.number_input("Ставка / час", value=400, key="rate_senior")
    hours = 165
    staff_total = (num_dilers * rate_diler * hours +
                   num_tour * rate_tour * hours +
                   num_senior * rate_senior * hours)
st.sidebar.caption(f"Итого ФОТ: {staff_total:,.0f} ₽".replace(",", " "))

# --- 6. ПЕРВИЧНЫЕ ИНВЕСТИЦИИ (без резервного фонда) ---
st.sidebar.subheader("💰 Первичные инвестиции")
inv_repair = st.sidebar.number_input("🔨 Ремонт и оснащение помещения, руб.", value=1_500_000, step=100_000)
inv_equip = st.sidebar.number_input("🎲 Закупка оборудования и комплектующих, руб.", value=2_000_000, step=100_000)
inv_deposit = st.sidebar.slider("🔐 Обеспечительный платёж, руб.",
                               min_value=500_000, max_value=1_000_000, value=1_000_000, step=50_000)
inv_marketing = st.sidebar.number_input("📣 Маркетинговый бюджет на запуск, руб.", value=300_000, step=50_000)

total_investments = inv_repair + inv_equip + inv_deposit + inv_marketing
st.sidebar.markdown(f"**Общие инвестиции: {total_investments:,.0f} ₽**".replace(",", " "))

# ================== РАСЧЁТ ==================
# Выручка
rev_vkhody = vkhody * vkhody_price
rev_bar = (vkhody * bar_conv) * bar_check
rev_hookah = (vkhody * hookah_conv) * hookah_check
total_revenue = rev_vkhody + rev_bar + rev_hookah  # убрали рекламу

# Операционные расходы до роялти и налогов
opex_before = rent + other_opex + marketing_budget + staff_total

# Роялти (без ручной корректировки)
if "Partner" in support_level:
    profit_before = total_revenue - opex_before
    royalty_sum = max(0, profit_before * 0.5)
else:
    if "Pro" in support_level:
        royalty_rate = 0.10
    else:  # VIP
        royalty_rate = 0.15
    royalty_sum = total_revenue * royalty_rate

# Налог (ИП или ООО — ставки одинаковые, просто для справки)
if tax_mode == "УСН 6% (Доходы)":
    tax_amount = total_revenue * 0.06
elif tax_mode == "УСН 15% (Доходы - Расходы)":
    tax_base = total_revenue - (opex_before + royalty_sum)
    tax_amount = max(0, tax_base * 0.15)
else:  # ОСНО
    profit_before_tax = total_revenue - opex_before - royalty_sum
    tax_amount = max(0, profit_before_tax * 0.25)

# Окупаемость
if net_profit > 0:
    payback_months = total_investments / net_profit
else:
    payback_months = float('inf')

# ================== МЕТРИКИ ==================
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Выручка", f"{total_revenue:,.0f} ₽".replace(",", " "))
col2.metric("📈 Чистая прибыль", f"{net_profit:,.0f} ₽".replace(",", " "),
            delta=f"{(net_profit/total_revenue)*100:.1f}% маржа" if total_revenue > 0 else "0%")
col3.metric("⏳ Окупаемость",
            f"{payback_months:.1f} мес." if payback_months != float('inf') else "> 5 лет")
col4.metric("⭐ Роялти (франчайзеру)", f"{royalty_sum:,.0f} ₽".replace(",", " "))

st.markdown("---")

# ================== ГРАФИК (один, структура выручки) ==================
st.subheader("🧩 Структура выручки")
labels = ['Вход в игру', 'Кальян', 'Бар']
values = [rev_vkhody, rev_hookah, rev_bar]
colors = ['#FF4C24', '#FF7A5C', '#CC3A1A']  # оттенки фирменного

fig_pie = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(colors=colors, line=dict(color='#1A1C23', width=2)),
    textinfo='percent+label',
    textfont=dict(color='white', size=15),
    hoverinfo='label+value+percent',
    hovertemplate='%{label}: %{value:,.0f} ₽ (%{percent})<extra></extra>'
)])
fig_pie.update_layout(
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font=dict(color='white'),
    showlegend=False,
    margin=dict(t=30, b=10, l=10, r=10),
    height=450
)
st.plotly_chart(fig_pie, use_container_width=True)

# --- ДЕТАЛИЗАЦИЯ РАСХОДОВ (сворачиваемый блок) ---
with st.expander("📋 Детализация расходов и инвестиций"):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("**Постоянные расходы (в месяц)**")
        st.write(f"Аренда + коммунальные: {rent:,.0f} ₽".replace(",", " "))
        st.write(f"Операционные расходы: {other_opex:,.0f} ₽".replace(",", " "))
        st.write(f"Маркетинг: {marketing_budget:,.0f} ₽".replace(",", " "))
        st.write(f"ФОТ: {staff_total:,.0f} ₽".replace(",", " "))
        st.write(f"Роялти: {royalty_sum:,.0f} ₽".replace(",", " "))
        st.write(f"Налог ({tax_mode}): {tax_amount:,.0f} ₽".replace(",", " "))
        st.write("---")
        st.write(f"**Итого пост. расходы: {total_opex:,.0f} ₽**".replace(",", " "))
    with col_d2:
        st.write("**Первичные инвестиции**")
        st.write(f"Ремонт и оснащение: {inv_repair:,.0f} ₽".replace(",", " "))
        st.write(f"Оборудование и комплектующие: {inv_equip:,.0f} ₽".replace(",", " "))
        st.write(f"Обеспечительный платёж: {inv_deposit:,.0f} ₽".replace(",", " "))
        st.write(f"Маркетинг на запуск: {inv_marketing:,.0f} ₽".replace(",", " "))
        st.write("---")
        st.write(f"**Общие инвестиции: {total_investments:,.0f} ₽**".replace(",", " "))
