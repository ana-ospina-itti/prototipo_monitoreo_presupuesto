# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import io

# # --- Configuración de la Página y Constantes Financieras ---
# st.set_page_config(
#     page_title="Monitor de Presupuesto Mensual",
#     page_icon="🇬🇵",
#     layout="wide"
# )

# # --- CONSTANTES FINANCIERAS (EN GUARANÍES) ---
# INGRESO_FIJO_MENSUAL = 5300000

# # Gastos Fijos Mensuales
# GASTOS_FIJOS = {
#     'Hipoteca': 1800000,
#     'Plan Celular': 89000,
#     'ANDE': 200000,
#     'Netflix': 70000,
#     'Seguros Asepasa': 150000,
#     'Ahorro': 530000  # Meta de ahorro tratada como un gasto fijo
# }

# # Límites para Gastos Variables Mensuales
# LIMITES_GASTOS_VARIABLES = {
#     'Restaurante y Café': 400000,
#     'Mercado': 500000,
#     'Transporte Apps': 300000,
#     'Entretenimiento': 350000,
#     'Peluquería': 100000
# }

# # --- Funciones Auxiliares ---

# def process_gastos_data(df_gastos):
#     """
#     Procesa el dataframe de gastos.
#     - Convierte la columna de fecha a formato datetime.
#     - Extrae el mes y el año para facilitar el filtrado.
#     """
#     if df_gastos is not None and not df_gastos.empty:
#         df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'], errors='coerce')
#         df_gastos.dropna(subset=['fecha'], inplace=True)
#         df_gastos['mes_año'] = df_gastos['fecha'].dt.to_period('M').astype(str)
#     return df_gastos

# def create_sample_data():
#     """
#     Crea un dataframe de gastos de ejemplo para la demostración.
#     """
#     gastos_data = {
#         'monto compra': [
#             # Mayo 2024
#             150000, 120000, 450000, 80000, 200000, 90000, 100000, 50000,
#             # Junio 2024
#             180000, 90000, 550000, 120000, 400000, 110000, 150000
#         ],
#         'fecha': [
#             # Mayo 2024
#             '2024-05-03', '2024-05-08', '2024-05-10', '2024-05-15', '2024-05-18', '2024-05-22', '2024-05-25', '2024-05-28',
#             # Junio 2024
#             '2024-06-02', '2024-06-05', '2024-06-11', '2024-06-16', '2024-06-20', '2024-06-24', '2024-06-28'
#         ],
#         'categoría': [
#             # Mayo 2024
#             'Restaurante y Café', 'Transporte Apps', 'Mercado', 'Peluquería', 'Entretenimiento', 'Restaurante y Café', 'Transporte Apps', 'Mercado',
#             # Junio 2024
#             'Restaurante y Café', 'Transporte Apps', 'Mercado', 'Peluquería', 'Entretenimiento', 'Restaurante y Café', 'Mercado'
#         ],
#         'receptor de la compra': [
#             # Mayo 2024
#             'Café del Centro', 'Uber', 'Superseis', 'Peluquería Estilo', 'CineMar', 'La Pizzería', 'Bolt', 'Stock',
#             # Junio 2024
#             'Lido Bar', 'Uber', 'Superseis', 'Barbería Don José', 'Teatro Municipal', 'El Bodegón', 'Casa Rica'
#         ]
#     }
#     return pd.DataFrame(gastos_data)

# # --- Interfaz de Usuario (Sidebar) ---
# st.sidebar.header("📂 Cargar Archivo de Gastos")
# st.sidebar.info(
#     "Sube tu archivo CSV con los gastos variables del mes. "
#     "Si no subes nada, la aplicación usará datos de ejemplo."
# )

# uploaded_gastos = st.sidebar.file_uploader(
#     "Carga tu CSV de Gastos Variables",
#     type=['csv']
# )

# # --- Lógica Principal de la Aplicación ---
# if uploaded_gastos is not None:
#     df_gastos_base = pd.read_csv(uploaded_gastos)
# else:
#     df_gastos_base = create_sample_data()

# df_gastos_base = process_gastos_data(df_gastos_base)

# # --- Cuerpo Principal de la Aplicación ---
# st.title("📊 Monitor de Presupuesto Mensual")
# st.markdown(f"Análisis basado en un **ingreso fijo mensual de Gs. {INGRESO_FIJO_MENSUAL:,.0f}**.")

# if not df_gastos_base.empty:
#     meses_disponibles = sorted(df_gastos_base['mes_año'].dropna().unique(), reverse=True)
    
#     if not meses_disponibles:
#         st.warning("No se encontraron datos con fechas válidas en el archivo.")
#     else:
#         selected_month = st.selectbox(
#             "Selecciona un mes para analizar:",
#             options=meses_disponibles
#         )

#         st.header(f"Análisis Detallado de {selected_month}")

#         # --- Filtrar datos para el mes seleccionado ---
#         gastos_mes_df = df_gastos_base[df_gastos_base['mes_año'] == selected_month].copy()

#         # --- Cálculos Financieros ---
#         total_gastos_fijos = sum(GASTOS_FIJOS.values())
#         total_gastos_variables = gastos_mes_df['monto compra'].sum()
#         total_gastos_generales = total_gastos_fijos + total_gastos_variables
#         ahorro_real = INGRESO_FIJO_MENSUAL - total_gastos_generales
#         meta_ahorro = GASTOS_FIJOS['Ahorro']
#         diferencia_ahorro = ahorro_real - meta_ahorro

#         # --- Resumen General (Métricas) ---
#         st.subheader("Resumen Financiero del Mes")
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("✅ Ingreso Fijo", f"Gs. {INGRESO_FIJO_MENSUAL:,.0f}")
#         col2.metric("❌ Gasto Total", f"Gs. {total_gastos_generales:,.0f}")
#         col3.metric("💰 Ahorro Real", f"Gs. {ahorro_real:,.0f}")
#         col4.metric(
#             "🎯 Meta de Ahorro",
#             f"Gs. {diferencia_ahorro:,.0f}",
#             help=f"Meta: Gs. {meta_ahorro:,.0f}. Un valor positivo significa que superaste la meta.",
#             delta_color="normal" if diferencia_ahorro >= 0 else "inverse"
#         )

#         st.divider()

#         # --- Análisis de Gastos Variables vs. Límites ---
#         st.subheader("Análisis de Gastos Variables vs. Límites")
        
#         gastos_por_categoria = gastos_mes_df.groupby('categoría')['monto compra'].sum()
        
#         cols_gastos = st.columns(len(LIMITES_GASTOS_VARIABLES))
        
#         for i, (categoria, limite) in enumerate(LIMITES_GASTOS_VARIABLES.items()):
#             with cols_gastos[i]:
#                 gasto_actual = gastos_por_categoria.get(categoria, 0)
#                 porcentaje = (gasto_actual / limite) * 100 if limite > 0 else 0
#                 color_barra = "green" if porcentaje <= 70 else "orange" if porcentaje <= 100 else "red"

#                 fig = go.Figure(go.Indicator(
#                     mode="gauge+number",
#                     value=gasto_actual,
#                     domain={'x': [0, 1], 'y': [0, 1]},
#                     title={'text': categoria, 'font': {'size': 16}},
#                     number={'prefix': "Gs. ", 'valueformat': ',.0f'},
#                     gauge={
#                         'axis': {'range': [None, limite], 'tickwidth': 1, 'tickcolor': "darkblue"},
#                         'bar': {'color': color_barra},
#                         'steps': [
#                             {'range': [0, limite * 0.7], 'color': 'lightgreen'},
#                             {'range': [limite * 0.7, limite], 'color': 'lightyellow'}
#                         ],
#                         'threshold': {
#                             'line': {'color': "red", 'width': 4},
#                             'thickness': 0.75,
#                             'value': limite
#                         }
#                     }
#                 ))
#                 fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
#                 st.plotly_chart(fig, use_container_width=True)

#         st.divider()

#         # --- Detalle Interactivo de Gastos ---
#         st.subheader("Explorar Gastos por Categoría")
        
#         # Combinar categorías fijas y variables para el selector
#         categorias_fijas_df = pd.DataFrame(list(GASTOS_FIJOS.items()), columns=['categoría', 'monto compra'])
#         categorias_fijas_df['receptor de la compra'] = 'Gasto Fijo'
#         categorias_fijas_df['fecha'] = pd.to_datetime(f'{selected_month}-01')

#         df_completo_mes = pd.concat([gastos_mes_df, categorias_fijas_df[['fecha', 'categoría', 'receptor de la compra', 'monto compra']]])

#         # Selector de categoría
#         categoria_seleccionada = st.selectbox(
#             "Selecciona una categoría para ver el detalle:",
#             options=sorted(df_completo_mes['categoría'].unique())
#         )

#         if categoria_seleccionada:
#             st.write(f"**Detalles para: {categoria_seleccionada}**")
            
#             detalle_df = df_completo_mes[df_completo_mes['categoría'] == categoria_seleccionada]
            
#             # Formatear para mostrar
#             detalle_df_display = detalle_df[['fecha', 'receptor de la compra', 'monto compra']].copy()
#             detalle_df_display['fecha'] = detalle_df_display['fecha'].dt.strftime('%Y-%m-%d')
#             detalle_df_display['monto compra'] = detalle_df_display['monto compra'].apply(lambda x: f"Gs. {x:,.0f}")
            
#             st.dataframe(detalle_df_display.sort_values(by='fecha'), use_container_width=True)

# else:
#     st.error("No se pudieron cargar los datos. Verifica tu archivo CSV.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# --- Configuración de la Página y Constantes Financieras ---
st.set_page_config(
    page_title="Monitor de Presupuesto Mensual",
    page_icon="🇬🇵",
    layout="wide"
)

# --- CONSTANTES FINANCIERAS (EN GUARANÍES) ---
INGRESO_FIJO_MENSUAL = 5300000

# Gastos Fijos Mensuales
GASTOS_FIJOS = {
    'Hipoteca': 1800000,
    'Plan Celular': 89000,
    'ANDE': 200000,
    'Netflix': 70000,
    'Seguros Asepasa': 150000,
    'Ahorro': 530000  # Meta de ahorro tratada como un gasto fijo
}

# Límites para Gastos Variables Mensuales
LIMITES_GASTOS_VARIABLES = {
    'Restaurante y Café': 400000,
    'Mercado': 500000,
    'Transporte Apps': 300000,
    'Entretenimiento': 350000,
    'Peluquería': 100000
}

# --- Funciones Auxiliares ---

def process_gastos_data(df_gastos):
    """
    Procesa el dataframe de gastos.
    - Convierte la columna de fecha a formato datetime.
    - Extrae el mes y el año para facilitar el filtrado.
    """
    if df_gastos is not None and not df_gastos.empty:
        df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'], errors='coerce')
        df_gastos.dropna(subset=['fecha'], inplace=True)
        df_gastos['mes_año'] = df_gastos['fecha'].dt.to_period('M').astype(str)
    return df_gastos

def create_sample_data():
    """
    Crea un dataframe de gastos de ejemplo para la demostración.
    """
    gastos_data = {
        'monto compra': [
            # Mayo 2024
            150000, 120000, 450000, 80000, 200000, 90000, 100000, 50000,
            # Junio 2024
            180000, 90000, 550000, 120000, 400000, 110000, 150000
        ],
        'fecha': [
            # Mayo 2024
            '2024-05-03', '2024-05-08', '2024-05-10', '2024-05-15', '2024-05-18', '2024-05-22', '2024-05-25', '2024-05-28',
            # Junio 2024
            '2024-06-02', '2024-06-05', '2024-06-11', '2024-06-16', '2024-06-20', '2024-06-24', '2024-06-28'
        ],
        'categoría': [
            # Mayo 2024
            'Restaurante y Café', 'Transporte Apps', 'Mercado', 'Peluquería', 'Entretenimiento', 'Restaurante y Café', 'Transporte Apps', 'Mercado',
            # Junio 2024
            'Restaurante y Café', 'Transporte Apps', 'Mercado', 'Peluquería', 'Entretenimiento', 'Restaurante y Café', 'Mercado'
        ],
        'receptor de la compra': [
            # Mayo 2024
            'Café del Centro', 'Uber', 'Superseis', 'Peluquería Estilo', 'CineMar', 'La Pizzería', 'Bolt', 'Stock',
            # Junio 2024
            'Lido Bar', 'Uber', 'Superseis', 'Barbería Don José', 'Teatro Municipal', 'El Bodegón', 'Casa Rica'
        ]
    }
    return pd.DataFrame(gastos_data)

# --- Interfaz de Usuario (Sidebar) ---
st.sidebar.header("📂 Cargar Archivo de Gastos")
st.sidebar.info(
    "Sube tu archivo CSV con los gastos variables del mes. "
    "Si no subes nada, la aplicación usará datos de ejemplo."
)

uploaded_gastos = st.sidebar.file_uploader(
    "Carga tu CSV de Gastos Variables",
    type=['csv']
)

# --- Lógica Principal de la Aplicación ---
if uploaded_gastos is not None:
    df_gastos_base = pd.read_csv(uploaded_gastos)
else:
    df_gastos_base = create_sample_data()

df_gastos_base = process_gastos_data(df_gastos_base)

# --- Cuerpo Principal de la Aplicación ---
st.title("📊 Monitor de Presupuesto Mensual")
st.markdown(f"Análisis basado en un **ingreso fijo mensual de Gs. {INGRESO_FIJO_MENSUAL:,.0f}**.")

if not df_gastos_base.empty:
    meses_disponibles = sorted(df_gastos_base['mes_año'].dropna().unique(), reverse=True)
    
    if not meses_disponibles:
        st.warning("No se encontraron datos con fechas válidas en el archivo.")
    else:
        selected_months = st.multiselect(
            "Selecciona hasta 2 meses para analizar y comparar:",
            options=meses_disponibles,
            default=meses_disponibles[:min(2, len(meses_disponibles))],
            max_selections=2
        )

        if selected_months:
            # --- Vista Detallada por Mes ---
            cols = st.columns(len(selected_months))
            comparison_data = []

            for i, month in enumerate(selected_months):
                with cols[i]:
                    st.header(f"Análisis de {month}")

                    gastos_mes_df = df_gastos_base[df_gastos_base['mes_año'] == month].copy()
                    
                    total_gastos_fijos = sum(GASTOS_FIJOS.values())
                    total_gastos_variables = gastos_mes_df['monto compra'].sum()
                    total_gastos_generales = total_gastos_fijos + total_gastos_variables
                    ahorro_real = INGRESO_FIJO_MENSUAL - total_gastos_generales
                    meta_ahorro = GASTOS_FIJOS['Ahorro']
                    diferencia_ahorro = ahorro_real - meta_ahorro

                    # Guardar datos para la comparación
                    comparison_data.append({
                        'Mes': month,
                        'Gastos Fijos': total_gastos_fijos,
                        'Gastos Variables': total_gastos_variables,
                        'Ahorro Real': ahorro_real
                    })

                    st.subheader("Resumen Financiero")
                    st.metric("✅ Ingreso Fijo", f"Gs. {INGRESO_FIJO_MENSUAL:,.0f}")
                    st.metric("❌ Gasto Total", f"Gs. {total_gastos_generales:,.0f}")
                    st.metric("💰 Ahorro Real", f"Gs. {ahorro_real:,.0f}")
                    st.metric(
                        "🎯 Meta de Ahorro",
                        f"Gs. {diferencia_ahorro:,.0f}",
                        help=f"Meta: Gs. {meta_ahorro:,.0f}. Un valor positivo significa que superaste la meta.",
                        delta_color="normal" if diferencia_ahorro >= 0 else "inverse"
                    )

                    st.subheader("Gastos Variables vs. Límites")
                    gastos_por_categoria = gastos_mes_df.groupby('categoría')['monto compra'].sum()
                    
                    for categoria, limite in LIMITES_GASTOS_VARIABLES.items():
                        gasto_actual = gastos_por_categoria.get(categoria, 0)
                        color_barra = "green" if gasto_actual <= limite * 0.7 else "orange" if gasto_actual <= limite else "red"
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number", value=gasto_actual,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': categoria, 'font': {'size': 14}},
                            number={'prefix': "Gs. ", 'valueformat': ',.0f'},
                            gauge={'axis': {'range': [None, limite]}, 'bar': {'color': color_barra}}
                        ))
                        fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # --- Sección de Comparación ---
            if len(selected_months) == 2:
                st.header("🆚 Gráficos Comparativos")
                
                # Gráfico 1: Comparación de Gastos Totales y Ahorro
                df_comp = pd.DataFrame(comparison_data)
                df_melted = df_comp.melt(id_vars='Mes', value_vars=['Gastos Fijos', 'Gastos Variables', 'Ahorro Real'],
                                         var_name='Tipo', value_name='Monto')

                fig_comp_total = px.bar(
                    df_melted,
                    x='Mes', y='Monto', color='Tipo',
                    barmode='group',
                    title='Comparación General de Gastos y Ahorro',
                    text_auto='.2s',
                    labels={'Monto': 'Monto (Gs.)'}
                )
                fig_comp_total.update_traces(textangle=0, textposition="outside")
                st.plotly_chart(fig_comp_total, use_container_width=True)

                # Gráfico 2: Comparación de Gastos Variables por Categoría
                gastos_var_comp_list = []
                for month in selected_months:
                    gastos_mes_df = df_gastos_base[df_gastos_base['mes_año'] == month]
                    for categoria, limite in LIMITES_GASTOS_VARIABLES.items():
                        gasto_actual = gastos_mes_df[gastos_mes_df['categoría'] == categoria]['monto compra'].sum()
                        gastos_var_comp_list.append({
                            'Mes': month,
                            'Categoría': categoria,
                            'Gasto': gasto_actual
                        })
                df_gastos_var_comp = pd.DataFrame(gastos_var_comp_list)
                
                fig_comp_var = px.bar(
                    df_gastos_var_comp,
                    x='Categoría', y='Gasto', color='Mes',
                    barmode='group',
                    title='Comparación de Gastos Variables por Categoría',
                    text_auto='.2s',
                    labels={'Gasto': 'Gasto (Gs.)'}
                )
                fig_comp_var.update_traces(textangle=0, textposition="outside")
                st.plotly_chart(fig_comp_var, use_container_width=True)


            # --- Detalle Interactivo de Gastos ---
            st.header("🔍 Explorar Gastos por Categoría")
            
            # Usar un selectbox para elegir cuál de los meses seleccionados detallar
            month_to_detail = st.selectbox(
                "Selecciona un mes para ver el detalle de sus gastos:",
                options=selected_months
            )

            if month_to_detail:
                gastos_mes_df = df_gastos_base[df_gastos_base['mes_año'] == month_to_detail]
                categorias_fijas_df = pd.DataFrame(list(GASTOS_FIJOS.items()), columns=['categoría', 'monto compra'])
                categorias_fijas_df['receptor de la compra'] = 'Gasto Fijo'
                categorias_fijas_df['fecha'] = pd.to_datetime(f'{month_to_detail}-01')
                df_completo_mes = pd.concat([gastos_mes_df, categorias_fijas_df[['fecha', 'categoría', 'receptor de la compra', 'monto compra']]])

                categoria_seleccionada = st.selectbox(
                    "Selecciona una categoría para ver el detalle:",
                    options=sorted(df_completo_mes['categoría'].unique()),
                    key=f"detalle_{month_to_detail}" # Key única para evitar conflictos
                )

                if categoria_seleccionada:
                    st.write(f"**Detalles para: {categoria_seleccionada} en {month_to_detail}**")
                    detalle_df = df_completo_mes[df_completo_mes['categoría'] == categoria_seleccionada]
                    detalle_df_display = detalle_df[['fecha', 'receptor de la compra', 'monto compra']].copy()
                    detalle_df_display['fecha'] = detalle_df_display['fecha'].dt.strftime('%Y-%m-%d')
                    detalle_df_display['monto compra'] = detalle_df_display['monto compra'].apply(lambda x: f"Gs. {x:,.0f}")
                    st.dataframe(detalle_df_display.sort_values(by='fecha'), use_container_width=True)

else:
    st.error("No se pudieron cargar los datos. Verifica tu archivo CSV.")