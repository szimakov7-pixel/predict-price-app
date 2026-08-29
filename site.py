import streamlit as st
import pandas as pd
import joblib

@st.cache_resource
def load_model():
    try:
        model = joblib.load('model_gb.pkl')
        return model
    except Exception as e:
        st.error(f"Ошибка загрузки модели: {e}")
        return None
    
model = load_model()

st.set_page_config(
    page_title="Прогноз стоимости квартиры",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 Прогнозирование стоимости квартиры")
st.markdown("**Округ ЮВАО (г. Москва)**")
st.markdown("---")

st.subheader("📋 Введите характеристики квартиры:")

col1, col2 = st.columns(2)

with col1:
    total_area = st.number_input(
        "Общая площадь (м²)", 
        min_value=20.0, max_value=150.0, value=55.0, step=1.0
    )
    living_area = st.number_input(
        "Жилая площадь (м²)", 
        min_value=10.0, max_value=100.0, value=30.0, step=1.0
    )
    rooms = st.number_input(
            "Количество комнат", 
            min_value=1, max_value=4, value=2, step=1
    )
    kitchen_area = st.number_input(
        "Площадь кухни (м²)", 
        min_value=4.0, max_value=30.0, value=10.0, step=1.0
    )
    
with col2:
    floor = st.number_input(
        "Этаж", 
        min_value=1, max_value=30, value=7
    )
    total_floors = st.number_input(
        "Этажность дома", 
        min_value=2, max_value=35, value=12
    )
    wall_type = st.selectbox(
        "Тип стен",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {1: "Панельный", 2: "Блочный", 3: "Монолитный", 
                               4: "Кирпичный", 5: "Монолитно-кирпичный"}[x]
    )
    renovation = st.selectbox(
        "Состояние ремонта",
        options=[0, 1, 2, 3],
        format_func=lambda x: {0: "Без ремонта", 1: "Косметический", 
                               2: "Евроремонт", 3: "Дизайнерский"}[x]
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    metro_mins = st.number_input(
        "Время до метро (мин)", 
        min_value=1, max_value=30, value=10
    )

with col4:
    st.markdown("**Наличие:**")
    has_balcon = st.checkbox("Балкон", value=False)
    has_loggia = st.checkbox("Лоджия", value=False)

if st.button("🚀 Рассчитать стоимость", type="primary"):
    if model is None:
        st.error("Модель не загружена. Проверьте файл model_gb.pkl")
    else:
        input_data = pd.DataFrame([{
            'total_area': total_area,
            'living_area': living_area,
            'rooms': rooms,
            'kitchen_area': kitchen_area,
            'floor': floor,
            'total_floors': total_floors,
            'wall_type': wall_type,
            'renovation': renovation,
            'metro_mins': metro_mins,
            'has_balcon': has_balcon,
            'has_loggia': has_loggia
        }])

        try:
            prediction = model.predict(input_data)[0]
            mae = 3.21  
            
            st.markdown("---")
            st.subheader("📊 Результат прогноза")
            
            st.markdown(
                f"""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; text-align: center;">
                    <h1 style="color: #2e8b57;">{prediction:.2f} млн руб.</h1>
                    <p style="color: #666;">Примерная рыночная стоимость</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.info(f"📊 С учётом средней ошибки модели (±{mae:.2f} млн руб.):")
            st.write(f"**{prediction - mae:.2f} — {prediction + mae:.2f} млн руб.**")
            
        except Exception as e:
            st.error(f"Ошибка при расчёте: {e}")