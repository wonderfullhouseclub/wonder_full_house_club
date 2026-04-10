import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Финансовая модель клуба", layout="wide")

# 1. ЕДИНЫЙ БЛОК СТИЛЕЙ (Настройка внешнего вида)
st.markdown("""
<style>
    .stApp { background-color: #ECF0ED !important; }
    section[data-testid="stSidebar"] {
        background-color: #1A1C23 !important;
        border-right: 3px solid #FF4C24 !important;
    }
    /* Черный текст для всех, кроме оранжевых span */
    [data-testid="stMain"] *:not(span), .main *:not(span) {
        color: #1A1C23 !important;
        -webkit-text-fill-color: #1A1C23 !important;
    }
     /* ВОЗВРАЩАЕМ ОРАНЖЕВЫЙ ЗАГОЛОВКАМ В ОСНОВНОЙ ОБЛАСТИ */
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    .main h1,
    .main h2,
    .main h3,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3 {
        color: #FF4C24 !important;
        -webkit-text-fill-color: #FF4C24 !important;
    }
    /* Белый текст в сайдбаре */
    section[data-testid="stSidebar"] label p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] [data-testid^="stTickBar"] {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }
    /* Оранжевые заголовки и цифра в сайдбаре */
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
    div[data-testid="stThumbValue"] > div {
        color: #FF4C24 !important;
        font-weight: 900 !important;
    }
        /* ОРАНЖЕВЫЙ ЦВЕТ ДЛЯ ИТОГОВ В САЙДБАРЕ */
    #total-investments-sidebar {
        color: #FF4C24 !important;
        -webkit-text-fill-color: #FF4C24 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

st.image("logo.png", width=250)

# 2. ЛОКАЛЬНЫЙ ОРАНЖЕВЫЙ ЗАГОЛОВОК (В основном поле)
st.markdown("""
<div style="line-height: 1.2;">
    <h1 style="margin: 0; padding: 0; color: #FF4C24 !important; font-size: 2.5rem; font-weight: 800;">Финансовая модель</h1>
    <h1 style="margin: 0; padding: 0; color: #FF4C24 !important; font-size: 2.5rem; font-weight: 800;">Вашего клуба спортивного покера</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ================== БОКОВАЯ ПАНЕЛЬ ==================
st.sidebar.markdown("<h2 style='color: #FFFFFF;'>Параметры расчёта</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>🎲 Формат клуба</h3>", unsafe_allow_html=True)
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

# Слайдер с кастомной подписью
vkhody = st.sidebar.slider("🚪 Количество входов в месяц", min_v, max_v, def_v, step=50)

vkhody_price = st.sidebar.number_input("🎫 Средний чек (вход), руб.", value=1000, step=100)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>🤝 Уровень поддержки</h3>", unsafe_allow_html=True)
support_level = st.sidebar.selectbox(
    "Выберите пакет",
    ["Pro (роялти 10%)", "VIP (роялти 15%)", "Partner (50% от прибыли)"]
)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>🍷 Доп. услуги</h3>", unsafe_allow_html=True)
bar_conv = st.sidebar.slider("Конверсия в бар, %", 0, 100, 35) / 100

bar_check = st.sidebar.number_input("Средний чек бара, руб.", value=900, step=100)

hookah_conv = st.sidebar.slider("Конверсия в кальяны, %", 0, 100, 15) / 100

hookah_check = st.sidebar.number_input("Средний чек кальяна, руб.", value=1200, step=100)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>🏠 Постоянные расходы</h3>", unsafe_allow_html=True)
rent = st.sidebar.number_input("Аренда + коммунальные платежи, руб.", value=200000, step=10000)

other_opex = st.sidebar.slider("💡 Операционные расходы, руб.",
                               min_value=100000, max_value=1500000, value=500000, step=50000)

marketing_budget = st.sidebar.slider("📢 Маркетинг, руб.",
                                     min_value=50000, max_value=1000000, value=200000, step=10000)

tax_mode = st.sidebar.selectbox(
    "🧾 Налоговый режим",
    ["УСН 6% (Доходы)", "УСН 15% (Доходы - Расходы)", "ОСНО (25% с прибыли, без НДС)"]
)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>👥 Персонал</h3>", unsafe_allow_html=True)
c1, c2 = st.sidebar.columns([2, 1])
with c1:
    num_dilers = st.number_input("Дилеров", min_value=1, value=6, key="num_dilers")
    num_tour = st.number_input("Турнирных менеджеров", min_value=1, value=2, key="num_tour")
    num_senior = st.number_input("Старших менеджеров", min_value=0, value=1, key="num_senior")
with c2:
    rate_diler = st.number_input("Ставка/час", value=350, key="rate_diler")
    rate_tour = st.number_input("Ставка/час", value=250, key="rate_tour")
    rate_senior = st.number_input("Ставка/час", value=400, key="rate_senior")
hours = 165
staff_total = (num_dilers * rate_diler * hours +
               num_tour * rate_tour * hours +
               num_senior * rate_senior * hours)
st.sidebar.markdown(f"<span style='color: #FFFFFF; font-weight: 600;'>Итого ФОТ: {staff_total:,.0f} ₽</span>".replace(",", " "), unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>💰 Первичные инвестиции</h3>", unsafe_allow_html=True)
inv_repair = st.sidebar.number_input("🔨 Ремонт и оснащение помещения, руб.", value=1_500_000, step=100_000)
inv_equip = st.sidebar.number_input("🎲 Закупка оборудования и комплектующих, руб.", value=2_000_000, step=100_000)

inv_deposit = st.sidebar.slider("🔐 Обеспечительный платёж, руб.",
                               min_value=500_000, max_value=1_000_000, value=1_000_000, step=50_000)

inv_marketing = st.sidebar.number_input("📣 Маркетинговый бюджет на запуск, руб.", value=300_000, step=50_000)
total_investments = inv_repair + inv_equip + inv_deposit + inv_marketing
st.sidebar.markdown(f"<span id='total-investments-sidebar'>Общие инвестиции: {total_investments:,.0f} ₽</span>".replace(",", " "), unsafe_allow_html=True)

# ================== РАСЧЁТ ==================
rev_vkhody = vkhody * vkhody_price
rev_bar = (vkhody * bar_conv) * bar_check
rev_hookah = (vkhody * hookah_conv) * hookah_check
total_revenue = rev_vkhody + rev_bar + rev_hookah

opex_before = rent + other_opex + marketing_budget + staff_total

if "Partner" in support_level:
    profit_before = total_revenue - opex_before
    royalty_sum = max(0, profit_before * 0.5)
elif "Pro" in support_level:
    royalty_sum = total_revenue * 0.10
else:
    royalty_sum = total_revenue * 0.15

if tax_mode == "УСН 6% (Доходы)":
    tax_amount = total_revenue * 0.06
elif tax_mode == "УСН 15% (Доходы - Расходы)":
    tax_base = total_revenue - (opex_before + royalty_sum)
    tax_amount = max(0, tax_base * 0.15)
else:
    profit_before_tax = total_revenue - opex_before - royalty_sum
    tax_amount = max(0, profit_before_tax * 0.25)

total_opex = opex_before + royalty_sum + tax_amount
net_profit = total_revenue - total_opex

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
col4.metric("🤝 Роялти", f"{royalty_sum:,.0f} ₽".replace(",", " "))

st.markdown(
    "<h3 style='color: #FF4C24;'>📊 Инвестиционная аналитика</h3>",
    unsafe_allow_html=True
)

col_left, col_right = st.columns([1.6, 1])

# ================================
# ГРАФИК ОКУПАЕМОСТИ
# ================================
with col_left:
    st.subheader("Прогноз окупаемости")

    months = list(range(0, 25))
    cumulative_cashflow = [-total_investments + net_profit * m for m in months]

    fig_cf = go.Figure()
    fig_cf.add_trace(go.Scatter(
        x=months,
        y=cumulative_cashflow,
        mode='lines+markers',
        name='Накопленный денежный поток',
        line=dict(color='#FF4C24', width=4),
        marker=dict(size=6)
    ))

    fig_cf.add_hline(y=0, line_dash="dash", line_color="gray")

    fig_cf.update_layout(
        paper_bgcolor='#ECF0ED',
        plot_bgcolor='#FFFFFF',
        xaxis_title="Месяцы",
        yaxis_title="Баланс, ₽",
        margin=dict(l=10, r=10, t=30, b=10),
        height=420
    )

    st.plotly_chart(fig_cf, use_container_width=True)

# ================================
# СТРУКТУРА ВЫРУЧКИ
# ================================
with col_right:
    st.subheader("Структура выручки")

    labels = ['Вход в игру', 'Бар', 'Кальян']
    values = [rev_vkhody, rev_bar, rev_hookah]
    colors = ['#FF4C24', '#FF7A5C', '#CC3A1A']

    fig_rev = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors),
        textinfo='percent',
        hovertemplate='%{label}: %{value:,.0f} ₽<extra></extra>'
    )])

    fig_rev.update_layout(
        paper_bgcolor='#ECF0ED',
        margin=dict(l=10, r=10, t=30, b=10),
        height=420,
        showlegend=True
    )

    st.plotly_chart(fig_rev, use_container_width=True)

# ================================
# ЮНИТ-ЭКОНОМИКА
# ================================
st.markdown(
    "<h3 style='color: #FF4C24;'>📈 Юнит-экономика</h3>",
    unsafe_allow_html=True
)

avg_revenue_per_guest = total_revenue / vkhody if vkhody else 0
profit_margin = (net_profit / total_revenue * 100) if total_revenue else 0
opex_ratio = (total_opex / total_revenue * 100) if total_revenue else 0
tax_ratio = (tax_amount / total_revenue * 100) if total_revenue else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Доход на гостя", f"{avg_revenue_per_guest:,.0f} ₽".replace(",", " "))
col2.metric("Маржинальность", f"{profit_margin:.1f}%")
col3.metric("Доля расходов", f"{opex_ratio:.1f}%")
col4.metric("Налоговая нагрузка", f"{tax_ratio:.1f}%")

# --- ДЕТАЛИЗАЦИЯ ---
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
