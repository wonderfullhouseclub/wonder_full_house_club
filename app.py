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
/* ПЕРЕНОС НАПРАВО ТОЛЬКО ДЛЯ ДЕСКТОПА */
    @media (min-width: 768px) {
        [data-testid="stSidebar"] {
            left: auto !important;
            right: 0 !important;
            border-right: none !important;
            border-left: 3px solid #FF4C24 !important;
        }

        [data-testid="stAppViewContainer"] {
            flex-direction: row-reverse !important;
        }

        [data-testid="stSidebarCollapsedControl"] {
            left: auto !important;
            right: 10px !important;
            transform: scaleX(-1);
        }
    }

    /* ФИКС ДЛЯ МОБИЛОК (чтобы ничего не накладывалось) */
    @media (max-width: 767px) {
        [data-testid="stSidebar"] {
            border-right: 3px solid #FF4C24 !important;
            border-left: none !important;
        }
/* СКРЫВАЕМ КНОПКУ С КОТИКОМ (GITHUB) И КНОПКУ DEPLOY */
    #MainMenu, .stDeployButton, header {
        visibility: hidden;
        height: 0%;
    }

    /* УДАЛЯЕМ ЛИШНИЕ ОТСТУПЫ СВЕРХУ, КОТОРЫЕ ОСТАЛИСЬ ОТ ХЕДЕРА */
    .block-container {
        padding-top: 2rem !important;
    }

    /* СКРЫВАЕМ ИКОНКУ С КОТИКОМ В ПРАВОМ ВЕРХНЕМ УГЛУ */
    [data-testid="stStatusWidget"] {
        display: none !important;
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

# Настройки в зависимости от формата
if club_format.startswith("STRAIGHT"):
    min_v, max_v, def_v = 800, 5000, 2500
    default_dilers = 6
    default_tour_managers = 2
    default_equipment = 1_000_000
elif club_format.startswith("FULL HOUSE"):
    min_v, max_v, def_v = 2000, 9800, 4000
    default_dilers = 12
    default_tour_managers = 4
    default_equipment = 2_000_000
else:  # ROYAL FLASH
    min_v, max_v, def_v = 4000, 13000, 6000
    default_dilers = 25
    default_tour_managers = 6
    default_equipment = 3_000_000

vkhody = st.sidebar.slider("🚪 Количество входов в игру в месяц", min_v, max_v, def_v, step=50)
vkhody_price = st.sidebar.number_input("🎫 Средний чек (вход), руб.", value=850, step=50)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>🤝 Уровень поддержки</h3>", unsafe_allow_html=True)
support_level = st.sidebar.selectbox(
    "Выберите пакет",
    ["Pro (роялти 10%)", "VIP (роялти 15%)", "Partner (50% от прибыли)"]
)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>🍷 Доп. услуги</h3>", unsafe_allow_html=True)

# Кальян
hookah_conv = st.sidebar.slider("Конверсия в кальяны, %", 0, 100, 7) / 100
hookah_check = st.sidebar.number_input("Средний чек кальяна, руб.", value=1700, step=100)

# Бар
bar_conv = st.sidebar.slider("Конверсия в бар, %", 0, 100, 17) / 100
bar_check = st.sidebar.number_input("Средний чек бара, руб.", value=500, step=50)

# Кухня
kitchen_conv = st.sidebar.slider("Конверсия в кухню, %", 0, 100, 3) / 100
kitchen_check = st.sidebar.number_input("Средний чек кухни, руб.", value=600, step=50)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>🏠 Постоянные расходы</h3>", unsafe_allow_html=True)
rent = st.sidebar.number_input("Аренда + коммунальные платежи, руб.", value=200000, step=10000)

other_opex = st.sidebar.slider("💡 Операционные расходы, руб.",
                               min_value=100000, max_value=1500000, value=500000, step=50000)

marketing_budget = st.sidebar.slider("📢 Маркетинг, руб.",
                                     min_value=50000, max_value=1000000, value=300000, step=10000)

tax_mode = st.sidebar.selectbox(
    "🧾 Налоговый режим",
    ["УСН 6% (Доходы)", "УСН 15% (Доходы - Расходы)", "ОСНО (25% с прибыли, без НДС)"]
)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>👥 Персонал</h3>", unsafe_allow_html=True)
c1, c2 = st.sidebar.columns([2, 1])
with c1:
    num_dilers = st.number_input(
        "Дилеров",
        min_value=1,
        value=default_dilers,
        key=f"num_dilers_{club_format}"
    )
    num_tour = st.number_input(
        "Турнирных менеджеров",
        min_value=1,
        value=default_tour_managers,
        key=f"num_tour_{club_format}"
    )
    num_senior = st.number_input(
        "Старших менеджеров",
        min_value=0,
        value=1,
        key=f"num_senior_{club_format}"
    )
with c2:
    rate_diler = st.number_input("Ставка/час", value=350, key=f"rate_diler_{club_format}")
    rate_tour = st.number_input("Ставка/час", value=350, key=f"rate_tour_{club_format}")
    rate_senior = st.number_input("Ставка/час", value=400, key=f"rate_senior_{club_format}")

hours = 165
staff_total = (num_dilers * rate_diler * hours +
               num_tour * rate_tour * hours +
               num_senior * rate_senior * hours)
st.sidebar.markdown(f"<span style='color: #FFFFFF; font-weight: 600;'>Итого ФОТ: {staff_total:,.0f} ₽</span>".replace(",", " "), unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color: #FF4C24;'>💰 Первичные инвестиции</h3>", unsafe_allow_html=True)
inv_repair = st.sidebar.number_input("🔨 Ремонт и оснащение помещения, руб.", value=1_500_000, step=100_000)

inv_equip = st.sidebar.number_input(
    "🎲 Закупка оборудования и комплектующих, руб.",
    value=default_equipment,
    step=100_000,
    key=f"inv_equip_{club_format}"
)

inv_deposit = st.sidebar.slider("🔐 Обеспечительный платёж, руб.",
                               min_value=500_000, max_value=1_000_000, value=1_000_000, step=50_000)

inv_marketing = st.sidebar.number_input("📣 Маркетинговый бюджет на запуск, руб.", value=500_000, step=50_000)
total_investments = inv_repair + inv_equip + inv_deposit + inv_marketing
st.sidebar.markdown(f"<span id='total-investments-sidebar'>Общие инвестиции: {total_investments:,.0f} ₽</span>".replace(",", " "), unsafe_allow_html=True)

# ================== РАСЧЁТ (исправлен Partner) ==================
rev_vkhody = vkhody * vkhody_price
rev_kitchen = (vkhody * kitchen_conv) * kitchen_check
rev_bar = (vkhody * bar_conv) * bar_check
rev_hookah = (vkhody * hookah_conv) * hookah_check
total_revenue = rev_vkhody + rev_kitchen + rev_bar + rev_hookah

opex_before = rent + other_opex + marketing_budget + staff_total

# --- ИСПРАВЛЕННЫЙ БЛОК РАСЧЁТА РОЯЛТИ И НАЛОГА ---
if "Partner" in support_level:
    # Сначала считаем налог так, как будто роялти нет
    if tax_mode == "УСН 6% (Доходы)":
        tax_temp = total_revenue * 0.06
    elif tax_mode == "УСН 15% (Доходы - Расходы)":
        tax_temp = max(0, (total_revenue - opex_before) * 0.15)
    else:  # ОСНО
        tax_temp = max(0, (total_revenue - opex_before) * 0.25)
    
    # Чистая прибыль до партнёрского дележа
    net_before_split = total_revenue - opex_before - tax_temp
    royalty_sum = max(0, net_before_split * 0.5)   # 50% от чистой прибыли
    net_profit = net_before_split - royalty_sum     # оставшиеся 50% франчайзи
    tax_amount = tax_temp
else:
    # Pro / VIP
    if "Pro" in support_level:
        royalty_sum = total_revenue * 0.10
    else:  # VIP
        royalty_sum = total_revenue * 0.15

    if tax_mode == "УСН 6% (Доходы)":
        tax_amount = total_revenue * 0.06
    elif tax_mode == "УСН 15% (Доходы - Расходы)":
        tax_base = total_revenue - (opex_before + royalty_sum)
        tax_amount = max(0, tax_base * 0.15)
    else:  # ОСНО
        profit_before_tax = total_revenue - opex_before - royalty_sum
        tax_amount = max(0, profit_before_tax * 0.25)

    net_profit = total_revenue - opex_before - royalty_sum - tax_amount

# Общие расходы для детализации (включая роялти)
total_opex = opex_before + royalty_sum + tax_amount

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
col4.metric("🤝 Роялти", f"{royalty_sum:,.0f} ₽".replace(",", " "))

# ================== ГРАФИК ОКУПАЕМОСТИ С ПОЯСНЕНИЕМ ==================
st.markdown("<h3 style='color: #FF4C24;'>📈 Прогноз окупаемости инвестиций</h3>", unsafe_allow_html=True)

months = list(range(0, 13))
cash_flow = [-total_investments + (net_profit * m) for m in months]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=months,
    y=cash_flow,
    mode='lines+markers',
    name='Накопленная прибыль',
    line=dict(color='#FF4C24', width=4),
    marker=dict(color='#FFFFFF', size=8, line=dict(color='#FF4C24', width=2)),
    fill='tozeroy',
    fillcolor='rgba(255, 76, 36, 0.1)'
))
# Подчёркиваем, что чистая прибыль положительна уже с первого месяца
if net_profit > 0:
    fig.add_trace(go.Scatter(
        x=[1],
        y=[cash_flow[1]],
        mode='markers+text',
        marker=dict(color='#FF4C24', size=14, symbol='star', line=dict(color='white', width=1)),
        text=[" +₽ "],
        textposition="top center",
        textfont=dict(color="#1A1C23", size=12, family="Arial"),
        name="Прибыль с 1-го месяца",
        showlegend=False,
        hovertemplate='<b>Месяц 1</b><br>Чистая прибыль уже положительна!<extra></extra>'
    ))

fig.add_hline(y=0, line_dash="dash", line_color="#1A1C23", line_width=2,
              annotation_text="Точка окупаемости",
              annotation_position="bottom right",
              annotation_font_size=12,
              annotation_font_color="#1A1C23")

if payback_months != float('inf') and payback_months <= 12:
    fig.add_vline(x=payback_months, line_width=1, line_dash="dot", line_color="gray")
    fig.add_annotation(
        x=payback_months, y=cash_flow[int(payback_months)],
        text=f"{payback_months:.1f} мес.",
        showarrow=True,
        arrowhead=1,
        ax=20,
        ay=-30,
        font=dict(color="#1A1C23", size=12),
        bgcolor="#FFFFFF",
        bordercolor="#FF4C24"
    )

fig.update_layout(
    xaxis_title="Месяц",
    yaxis_title="Накопленная прибыль, ₽",
    paper_bgcolor='#ECF0ED',
    plot_bgcolor='#ECF0ED',
    font=dict(color='#1A1C23'),
    hovermode='x unified',
    xaxis=dict(tickmode='linear', dtick=1, gridcolor='#D0D4D8'),
    yaxis=dict(gridcolor='#D0D4D8', zerolinecolor='#1A1C23'),
    margin=dict(t=30, b=40, l=60, r=20),
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# Пояснение о положительной чистой прибыли с первого месяца
if net_profit > 0:
    st.markdown(f"""
    <div style='background-color: #FFFFFF; border-left: 4px solid #FF4C24; padding: 15px; border-radius: 6px; margin-top: 20px;'>
        <span style='color: #1A1C23; font-size: 1.1rem;'>
            ✅ <strong>Чистая прибыль уже с первого месяца:</strong> {net_profit:,.0f} ₽<br>
            📉 Инвестиции начнут окупаться с первого месяца, а полный возврат произойдёт через <strong>{payback_months:.1f} мес.</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Текущие параметры показывают убыток. Попробуйте увеличить количество входов или снизить расходы.")


# --- ДЕТАЛИЗАЦИЯ (ДОБАВЛЕНА КУХНЯ) ---
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
