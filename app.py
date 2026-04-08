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
        color: #D4AF37 !important;
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

# --- БОКОВАЯ ПАНЕЛЬ ---
st.sidebar.header("📍 Конфигуратор")

# 1. Формат клуба и трафик
st.sidebar.subheader("🎲 Формат клуба")
club_format = st.sidebar.selectbox(
    "Выберите формат",
    ["STRAIGHT (5–10 столов)", "FULL HOUSE (11–24 стола)", "ROYAL FLASH (25+ столов)"]
)

# Задаём диапазон входов в зависимости от формата
if club_format.startswith("STRAIGHT"):
    min_visits, max_visits, default_visits = 800, 2000, 1400
elif club_format.startswith("FULL HOUSE"):
    min_visits, max_visits, default_visits = 2000, 4500, 3200
else:  # ROYAL FLASH
    min_visits, max_visits, default_visits = 4000, 8000, 6000

vkhody = st.sidebar.slider(
    "🚪 Количество входов в месяц",
    min_value=min_visits,
    max_value=max_visits,
    value=default_visits,
    step=50
)
vkhody_price = st.sidebar.number_input("🎫 Средний чек (вход), руб.", value=1000, step=100)


# 3. Доп. услуги
st.sidebar.subheader("🍷 Доп. услуги")
bar_conv = st.sidebar.slider("Конверсия в бар, %", 0, 100, 35) / 100
bar_check = st.sidebar.number_input("Средний чек бара, руб.", value=900, step=100)

hookah_conv = st.sidebar.slider("Конверсия в кальяны, %", 0, 100, 15) / 100
hookah_check = st.sidebar.number_input("Средний чек кальяна, руб.", value=1200, step=100)

# --- 4. ПОСТОЯННЫЕ РАСХОДЫ (сгруппированы) ---
st.sidebar.subheader("🏠 Постоянные расходы")

# Аренда
rent = st.sidebar.number_input("Аренда + коммунальные платежи, руб.", value=200000, step=10000)

# 2. Маркетинг (CAC)
st.sidebar.subheader("📢 Маркетинг")
cac = st.sidebar.slider("Стоимость привлечения 1 гостя (CAC), руб.", 0, 1500, 350, step=50)
marketing_budget = vkhody * cac
st.sidebar.caption(f"Бюджет на маркетинг: {marketing_budget:,.0f} ₽".replace(",", " "))

# ФОТ с детализацией в expander
st.sidebar.subheader("👥 Персонал")
col_a, col_b = st.sidebar.columns(2)
with col_a:
    num_dilers = st.number_input("Дилеров", min_value=1, value=6)
    num_tour_manager = st.number_input("Турнирных менеджеров", min_value=1, value=2)
    num_senior_manager = st.number_input("Старших турнирных менеджеров", min_value=0, value=1)
with col_b:
    rate_diler = st.number_input("Ставка дилера/час", value=350)
    rate_tour_manager = st.number_input("Ставка турнирного менеджера/час", value=250)
    rate_senior = st.number_input("Ставка старшего менеджера/час", value=400)

hours_per_month = 165  # среднее кол-во часов в месяц
staff_total = (
    num_dilers * rate_diler * hours_per_month +
    num_tour_manager * rate_tour_manager * hours_per_month +
    num_senior_manager * rate_senior * hours_per_month
)
st.sidebar.caption(f"ФОТ (всего): {staff_total:,.0f} ₽".replace(",", " "))

# Налоги (выбор режима внутри постоянных расходов)
tax_mode = st.sidebar.selectbox(
    "🧾 Налоговый режим",
    ["УСН 6% (Доходы)", "УСН 15% (Доходы - Расходы)"]
)

# Прочие расходы
other_opex = st.sidebar.slider("💡 Прочие расходы (уборка, охрана, материалы), руб.",
                               min_value=50000, max_value=500000, value=150000, step=10000)

# --- 5. УРОВЕНЬ ПОДДЕРЖКИ И РОЯЛТИ ---
st.sidebar.subheader("🤝 Уровень поддержки")
support_level = st.sidebar.selectbox(
    "Выберите пакет",
    ["Pro (роялти 10%)", "VIP (роялти 15%)", "Partner (50% от прибыли)"]
)
if "Pro" in support_level:
    base_roy = 0.10
elif "VIP" in support_level:
    base_roy = 0.15
else:
    base_roy = 0.0

if "Partner" not in support_level:
    royalty_percent = st.sidebar.slider("Роялти (ручная корректировка), %",
                                       0, 20, int(base_roy * 100), step=1) / 100
else:
    royalty_percent = 0.0
    st.sidebar.caption("При Partner роялти = 50% от чистой прибыли")

# ========== БЛОК ПЕРВИЧНЫХ ИНВЕСТИЦИЙ ==========
st.sidebar.subheader("💰 Первичные инвестиции")

inv_repair = st.sidebar.number_input("🔨 Ремонт и оснащение помещения, руб.", value=1_500_000, step=100_000)
inv_equip = st.sidebar.number_input("🎲 Закупка оборудования и комплектующих, руб.", value=2_000_000, step=100_000)
inv_deposit = st.sidebar.slider("🔐 Обеспечительный платёж, руб.",
                               min_value=500_000, max_value=1_000_000, value=1_000_000, step=50_000)
inv_marketing = st.sidebar.number_input("📣 Маркетинговый бюджет на запуск, руб.", value=300_000, step=50_000)
inv_reserve = st.sidebar.number_input("💼 Резервный фонд на первые 3 месяца, руб.", value=500_000, step=50_000)

total_investments = inv_repair + inv_equip + inv_deposit + inv_marketing + inv_reserve
st.sidebar.markdown(f"**Общие инвестиции: {total_investments:,.0f} ₽**".replace(",", " "))

# ================== РАСЧЁТ ==================
# Выручка
rev_vkhody = vkhody * vkhody_price
rev_bar = (vkhody * bar_conv) * bar_check
rev_hookah = (vkhody * hookah_conv) * hookah_check
rev_ads = 50000
total_revenue = rev_vkhody + rev_bar + rev_hookah + rev_ads

# Операционные расходы до роялти и налогов
opex_before = rent + marketing_budget + staff_total + other_opex

# Роялти
if "Partner" in support_level:
    profit_before = total_revenue - opex_before
    royalty_sum = max(0, profit_before * 0.5)
else:
    royalty_sum = total_revenue * royalty_percent

# Налог
if tax_mode == "УСН 6% (Доходы)":
    tax_amount = total_revenue * 0.06
else:
    tax_base = total_revenue - (opex_before + royalty_sum)
    tax_amount = max(0, tax_base * 0.15)

total_opex = opex_before + royalty_sum + tax_amount
net_profit = total_revenue - total_opex

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
col4.metric("Роялти", f"{royalty_sum:,.0f} ₽".replace(",", " "))

st.markdown("---")

# ================== ГРАФИКИ ==================
c1, c2 = st.columns(2)

with c1:
    st.subheader("🧩 Структура выручки")
    labels = ['Входы', 'Бар', 'Кальяны', 'Реклама']
    values = [rev_vkhody, rev_bar, rev_hookah, rev_ads]
    colors = ['#D4AF37', '#B8860B', '#CD7F32', '#C5A059']
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=.4,
        marker=dict(colors=colors, line=dict(color='#1A1C23', width=2)),
        textinfo='percent+label', textfont=dict(color='white', size=14)
    )])
    fig_pie.update_layout(
        paper_bgcolor='#0E1117', plot_bgcolor='#0E1117',
        font=dict(color='white'), showlegend=False, margin=dict(t=30, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("📉 Прогноз движения денег")
    months = list(range(13))
    cash_flow = [-total_investments + (net_profit * m) for m in months]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=months, y=cash_flow, mode='lines+markers', name='Баланс',
        line=dict(color='#D4AF37', width=4),
        marker=dict(color='#FFFFFF', size=8, line=dict(color='#D4AF37', width=2)),
        fill='tozeroy', fillcolor='rgba(180,0,0,0.2)'
    ))
    fig_line.add_hline(y=0, line_dash="dash", line_color="#FF4B4B", line_width=2,
                       annotation_text="Окупаемость", annotation_position="bottom right",
                       annotation_font_size=12, annotation_font_color="#FF4B4B")
    fig_line.update_layout(
        xaxis_title="Месяц", yaxis_title="Накопленная прибыль, ₽",
        paper_bgcolor='#0E1117', plot_bgcolor='#0E1117', font=dict(color='white'),
        hovermode='x unified', xaxis=dict(gridcolor='#2A2E38', tickmode='linear', dtick=1),
        yaxis=dict(gridcolor='#2A2E38', zerolinecolor='#2A2E38'),
        margin=dict(t=30, b=40, l=60, r=20)
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- ДЕТАЛИЗАЦИЯ РАСХОДОВ (сворачиваемый блок) ---
with st.expander("📋 Детализация расходов и инвестиций"):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("**Постоянные расходы**")
        st.write(f"Аренда + коммунальные: {rent:,.0f} ₽".replace(",", " "))
        st.write(f"ФОТ: {staff_total:,.0f} ₽".replace(",", " "))
        st.write(f"Маркетинг (CAC): {marketing_budget:,.0f} ₽".replace(",", " "))
        st.write(f"Прочие расходы: {other_opex:,.0f} ₽".replace(",", " "))
        st.write(f"Роялти: {royalty_sum:,.0f} ₽".replace(",", " "))
        st.write(f"Налог ({tax_mode}): {tax_amount:,.0f} ₽".replace(",", " "))
    with col_d2:
        st.write("**Первичные инвестиции**")
        st.write(f"Ремонт и оснащение: {inv_repair:,.0f} ₽".replace(",", " "))
        st.write(f"Оборудование и комплектующие: {inv_equip:,.0f} ₽".replace(",", " "))
        st.write(f"Обеспечительный платёж: {inv_deposit:,.0f} ₽".replace(",", " "))
        st.write(f"Маркетинг на запуск: {inv_marketing:,.0f} ₽".replace(",", " "))
        st.write(f"Резервный фонд: {inv_reserve:,.0f} ₽".replace(",", " "))
        st.write("---")
        st.write(f"**Общие инвестиции: {total_investments:,.0f} ₽**".replace(",", " "))
        
