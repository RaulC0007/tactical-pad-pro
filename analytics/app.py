# analytics/app.py
# Dashboard Streamlit para análisis de fútbol

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Tactical Pad - Análisis de Fútbol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("⚽ Tactical Pad Pro - Análisis de Fútbol")
st.markdown("### Dashboard de Análisis con Datos Reales de StatsBomb")
st.markdown("---")

# Rutas de los datos
data_dir = Path(__file__).parent / "data" / "raw"
matches_file = data_dir / "champions_2019_matches.csv"
events_file = data_dir / "champions_2019_final_events.csv"

# Cargar datos
@st.cache_data
def load_data():
    matches = pd.read_csv(matches_file)
    events = pd.read_csv(events_file)
    return matches, events

matches_df, events_df = load_data()

# Sidebar - Navegación
st.sidebar.title("🎯 Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["📊 Resumen del Partido", "⚽ Análisis de Eventos", "🎯 Mapa de Tiros", "👥 Comparación de Equipos", "👑 Cole & Yorke 98/99"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Info del Partido")
st.sidebar.info(f"""
**Competición:** Champions League 2018/2019  
**Fase:** Final  
**Estadio:** Estadio Cívitas Metropolitano  
**Árbitro:** Daniele Orsato  
**Total Eventos:** {len(events_df):,}
""")

# ============================================
# PÁGINA 1: RESUMEN DEL PARTIDO
# ============================================
if page == "📊 Resumen del Partido":
    st.header("📊 Resumen del Partido")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Eventos", f"{len(events_df):,}")
    
    with col2:
        st.metric("Pases Completados", f"{len(events_df[events_df['type'] == 'Pass']):,}")
    
    with col3:
        st.metric("Tiros al Arco", f"{len(events_df[events_df['type'] == 'Shot']):,}")
    
    st.markdown("---")
    
    # Distribución de eventos por tipo
    st.subheader("📈 Distribución de Eventos por Tipo")
    event_counts = events_df['type'].value_counts().head(10)
    
    fig = px.bar(
        x=event_counts.values,
        y=event_counts.index,
        orientation='h',
        labels={'x': 'Cantidad', 'y': 'Tipo de Evento'},
        color=event_counts.values,
        color_continuous_scale='Viridis',
        title='Top 10 Tipos de Eventos en la Final'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Timeline de eventos
    st.subheader("⏱️ Timeline de Eventos por Minuto")
    events_by_minute = events_df.groupby('minute').size().reset_index(name='count')
    
    fig_timeline = px.line(
        events_by_minute,
        x='minute',
        y='count',
        labels={'minute': 'Minuto', 'count': 'Número de Eventos'},
        title='Eventos por Minuto del Partido'
    )
    fig_timeline.update_traces(line_color='#FF6B35', line_width=3)
    st.plotly_chart(fig_timeline, use_container_width=True)

# ============================================
# PÁGINA 2: ANÁLISIS DE EVENTOS
# ============================================
elif page == "⚽ Análisis de Eventos":
    st.header("⚽ Análisis Detallado de Eventos")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        selected_team = st.selectbox(
            "Filtrar por equipo:",
            ["Todos", "Tottenham Hotspur", "Liverpool"]
        )
    
    with col2:
        selected_event = st.selectbox(
            "Filtrar por tipo de evento:",
            ["Todos"] + events_df['type'].value_counts().head(10).index.tolist()
        )
    
    # Aplicar filtros
    filtered_events = events_df.copy()
    
    if selected_team != "Todos":
        filtered_events = filtered_events[filtered_events['team'] == selected_team]
    
    if selected_event != "Todos":
        filtered_events = filtered_events[filtered_events['type'] == selected_event]
    
    st.markdown(f"**Eventos filtrados:** {len(filtered_events):,}")
    
    # Gráfico de eventos por equipo
    st.subheader("📊 Eventos por Equipo")
    team_events = filtered_events['team'].value_counts()
    
    fig_teams = px.pie(
        values=team_events.values,
        names=team_events.index,
        title='Distribución de Eventos por Equipo',
        color_discrete_sequence=['#132257', '#C8102E']
    )
    st.plotly_chart(fig_teams, use_container_width=True)
    
    # Tabla de eventos
    st.subheader("📋 Tabla de Eventos (últimos 50)")
    display_cols = ['minute', 'second', 'type', 'player', 'team']
    st.dataframe(filtered_events[display_cols].tail(50), use_container_width=True)

# ============================================
# PÁGINA 3: MAPA DE TIROS
# ============================================
elif page == "🎯 Mapa de Tiros":
    st.header("🎯 Mapa de Tiros - Final Champions 2019")
    
    # Filtrar solo tiros
    shots = events_df[events_df['type'] == 'Shot'].copy()
    
    st.markdown(f"**Total de tiros en el partido:** {len(shots)}")
    
    # Selector de equipo
    team_filter = st.radio(
        "Selecciona equipo:",
        ["Todos", "Tottenham Hotspur", "Liverpool"],
        horizontal=True
    )
    
    if team_filter != "Todos":
        shots = shots[shots['team'] == team_filter]
    
    # Crear mapa de tiros
    fig_shots = go.Figure()
    
    # Dibujar cancha (simplificada)
    fig_shots.add_shape(
        type="rect",
        x0=0, y0=0, x1=120, y1=80,
        line=dict(color="white", width=2),
        fillcolor="green",
        opacity=0.3
    )
    
    # Agregar tiros
    for idx, shot in shots.iterrows():
        if pd.notna(shot.get('location')):
            # La ubicación viene como string "[x, y]"
            try:
                import ast
                location = ast.literal_eval(shot['location'])
                x, y = location[0], location[1]
                
                color = '#FFD700' if shot.get('shot_outcome') == 'Goal' else '#FF4444'
                size = 15 if shot.get('shot_outcome') == 'Goal' else 8
                
                fig_shots.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    marker=dict(
                        size=size,
                        color=color,
                        symbol='circle',
                        line=dict(color='black', width=1)
                    ),
                    name=f"{shot.get('player', 'Unknown')} - {shot.get('shot_outcome', 'Unknown')}",
                    hovertext=f"Jugador: {shot.get('player', 'Unknown')}<br>Minuto: {shot.get('minute', 'N/A')}"
                ))
            except:
                pass
    
    fig_shots.update_layout(
        title='Mapa de Tiros - Final Champions League 2019',
        xaxis=dict(range=[0, 120], showgrid=False, zeroline=False),
        yaxis=dict(range=[0, 80], showgrid=False, zeroline=False),
        plot_bgcolor='green',
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig_shots, use_container_width=True)
    
    # Estadísticas de tiros
    st.subheader("📊 Estadísticas de Tiros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tiros", len(shots))
    
    with col2:
        goals = len(shots[shots.get('shot_outcome', pd.Series()) == 'Goal']) if 'shot_outcome' in shots.columns else 0
        st.metric("Goles", goals)
    
    with col3:
        if len(shots) > 0:
            precision = (goals / len(shots) * 100) if 'shot_outcome' in shots.columns else 0
            st.metric("Precisión", f"{precision:.1f}%")

# ============================================
# PÁGINA 4: COMPARACIÓN DE EQUIPOS
# ============================================
elif page == "👥 Comparación de Equipos":
    st.header("👥 Comparación: Tottenham vs Liverpool")
    
    # Eventos por equipo
    team_stats = events_df.groupby('team').size().reset_index(name='total_events')
    
    # Tipos de eventos por equipo
    event_by_team = events_df.groupby(['team', 'type']).size().reset_index(name='count')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Total de Eventos por Equipo")
        fig_total = px.bar(
            team_stats,
            x='team',
            y='total_events',
            labels={'team': 'Equipo', 'total_events': 'Total de Eventos'},
            color='team',
            color_discrete_map={'Tottenham Hotspur': '#132257', 'Liverpool': '#C8102E'}
        )
        st.plotly_chart(fig_total, use_container_width=True)
    
    with col2:
        st.subheader("📈 Comparación de Tipos de Eventos")
        top_events = events_df['type'].value_counts().head(5).index.tolist()
        comparison = event_by_team[event_by_team['type'].isin(top_events)]
        
        fig_comparison = px.bar(
            comparison,
            x='type',
            y='count',
            color='team',
            barmode='group',
            labels={'type': 'Tipo de Evento', 'count': 'Cantidad'},
            color_discrete_map={'Tottenham Hotspur': '#132257', 'Liverpool': '#C8102E'}
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    st.markdown("---")
    
    # Tabla comparativa detallada
    st.subheader("📋 Tabla Comparativa Detallada")
    pivot_table = event_by_team.pivot(index='type', columns='team', values='count').fillna(0).astype(int)
    st.dataframe(pivot_table, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>⚽ Tactical Pad Pro - Dashboard de Análisis de Fútbol</p>
    <p>Datos proporcionados por StatsBomb (Open Data)</p>
</div>
""", unsafe_allow_html=True)
