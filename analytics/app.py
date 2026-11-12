# analytics/app.py
# Tactical Pad Pro - Dashboard Profesional de Análisis de Fútbol

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

# ============================================
# CONFIGURACIÓN DE TEMA PROFESIONAL
# ============================================
st.set_page_config(
    page_title="Tactical Pad Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema premium
st.markdown("""
<style>
    /* Fondo principal */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f1429 0%, #1a1f3a 100%);
    }
    
    /* Métricas */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 14px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #fbbf24 !important;
        font-size: 32px !important;
        font-weight: bold !important;
    }
    
    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Selectboxes */
    .stSelectbox>div>div {
        background: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    /* Info boxes */
    .stAlert {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #0f172a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 6px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CARGA DE DATOS
# ============================================
data_dir = Path(__file__).parent / "data" / "raw"
matches_file = data_dir / "champions_2019_matches.csv"
events_file = data_dir / "champions_2019_final_events.csv"
cy_file = data_dir / "cole_yorke_99_events.csv"

@st.cache_data
def load_data():
    matches = pd.read_csv(matches_file)
    events = pd.read_csv(events_file)
    return matches, events

matches_df, events_df = load_data()

# ============================================
# HEADER PROFESIONAL
# ============================================
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.markdown("<h1 style='font-size: 48px; margin: 0;'>⚽</h1>", unsafe_allow_html=True)

with col_title:
    st.title("Tactical Pad Pro")
    st.markdown("<p style='color: #94a3b8; font-size: 16px; margin-top: -10px;'>Dashboard Profesional de Análisis de Fútbol</p>", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# SIDEBAR CON NAVEGACIÓN PREMIUM
# ============================================
st.sidebar.markdown("<h2 style='color: #fbbf24; font-size: 24px;'>🎯 Navegación</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #64748b; font-size: 12px;'>Selecciona una sección</p>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "📊 Resumen del Partido",
        "⚽ Análisis de Eventos", 
        "🎯 Mapa de Tiros",
        "👥 Comparación de Equipos",
        "👑 Cole & Yorke 98/99",
        "⚙️ Editor de Formaciones"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #fbbf24;'>📋 Info del Partido</h3>", unsafe_allow_html=True)
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
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Eventos", f"{len(events_df):,}", delta="+12%")
    
    with col2:
        st.metric("Pases Completados", f"{len(events_df[events_df['type'] == 'Pass']):,}", delta="+8%")
    
    with col3:
        st.metric("Tiros al Arco", f"{len(events_df[events_df['type'] == 'Shot']):,}", delta="+5%")
    
    st.markdown("---")
    
    # Gráfico de distribución
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
    fig.update_layout(
        height=500,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Timeline
    st.subheader("⏱️ Timeline de Eventos por Minuto")
    events_by_minute = events_df.groupby('minute').size().reset_index(name='count')
    
    fig_timeline = px.line(
        events_by_minute,
        x='minute',
        y='count',
        labels={'minute': 'Minuto', 'count': 'Número de Eventos'},
        title='Eventos por Minuto del Partido'
    )
    fig_timeline.update_traces(line_color='#fbbf24', line_width=3)
    fig_timeline.update_layout(
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155')
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# ============================================
# PÁGINA 2: ANÁLISIS DE EVENTOS
# ============================================
elif page == "⚽ Análisis de Eventos":
    st.header("⚽ Análisis Detallado de Eventos")
    
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
    
    filtered_events = events_df.copy()
    
    if selected_team != "Todos":
        filtered_events = filtered_events[filtered_events['team'] == selected_team]
    
    if selected_event != "Todos":
        filtered_events = filtered_events[filtered_events['type'] == selected_event]
    
    st.markdown(f"**Eventos filtrados:** {len(filtered_events):,}")
    
    st.subheader("📊 Eventos por Equipo")
    team_events = filtered_events['team'].value_counts()
    
    fig_teams = px.pie(
        values=team_events.values,
        names=team_events.index,
        title='Distribución de Eventos por Equipo',
        color_discrete_sequence=['#3b82f6', '#ef4444']
    )
    fig_teams.update_layout(
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='white')
    )
    st.plotly_chart(fig_teams, use_container_width=True)
    
    st.subheader("📋 Tabla de Eventos (últimos 50)")
    display_cols = ['minute', 'second', 'type', 'player', 'team']
    st.dataframe(filtered_events[display_cols].tail(50), use_container_width=True)

# ============================================
# PÁGINA 3: MAPA DE TIROS
# ============================================
elif page == "🎯 Mapa de Tiros":
    st.header("🎯 Mapa de Tiros - Final Champions 2019")
    
    shots = events_df[events_df['type'] == 'Shot'].copy()
    st.markdown(f"**Total de tiros en el partido:** {len(shots)}")
    
    team_filter = st.radio(
        "Selecciona equipo:",
        ["Todos", "Tottenham Hotspur", "Liverpool"],
        horizontal=True
    )
    
    if team_filter != "Todos":
        shots = shots[shots['team'] == team_filter]
    
    fig_shots = go.Figure()
    
    fig_shots.add_shape(
        type="rect",
        x0=0, y0=0, x1=120, y1=80,
        line=dict(color="white", width=2),
        fillcolor="#1a472a",
        opacity=0.8
    )
    
    for idx, shot in shots.iterrows():
        if pd.notna(shot.get('location')):
            try:
                import ast
                location = ast.literal_eval(shot['location'])
                x, y = location[0], location[1]
                
                color = '#fbbf24' if shot.get('shot_outcome') == 'Goal' else '#ef4444'
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
        plot_bgcolor='#1a472a',
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig_shots, use_container_width=True)
    
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
    
    team_stats = events_df.groupby('team').size().reset_index(name='total_events')
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
            color_discrete_map={'Tottenham Hotspur': '#3b82f6', 'Liverpool': '#ef4444'}
        )
        fig_total.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white')
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
            color_discrete_map={'Tottenham Hotspur': '#3b82f6', 'Liverpool': '#ef4444'}
        )
        fig_comparison.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white')
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Tabla Comparativa Detallada")
    pivot_table = event_by_team.pivot(index='type', columns='team', values='count').fillna(0).astype(int)
    st.dataframe(pivot_table, use_container_width=True)

# ============================================
# PÁGINA 5: COLE & YORKE 98/99
# ============================================
elif page == "👑 Cole & Yorke 98/99":
    st.header("👑 La Dupla Legendaria: Andy Cole & Dwight Yorke (1998/1999)")
    st.markdown("Protagonistas del Triplete del Manchester United. Datos históricos reconstruidos a nivel de evento.")
    
    if cy_file.exists():
        cy_df = pd.read_csv(cy_file)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Goles de Yorke", 18)
        with col2:
            st.metric("Goles de Cole", 17)
        with col3:
            st.metric("Pases entre ellos", len(cy_df[cy_df['type'] == 'Pass']))
        
        st.markdown("---")
        st.subheader("🎯 Mapa de Tiros de la Dupla")
        
        shots = cy_df[cy_df['type'] == 'Shot']
        
        fig_cy = go.Figure()
        
        fig_cy.add_shape(type="rect", x0=60, y0=0, x1=120, y1=80,
                         line=dict(color="white", width=2), fillcolor="#1a472a", opacity=0.8)
        fig_cy.add_shape(type="rect", x0=103.5, y0=21.1, x1=120, y1=58.9,
                         line=dict(color="white", width=2))
        
        for idx, shot in shots.iterrows():
            try:
                import ast
                location = ast.literal_eval(shot['location'])
                x, y = location[0], location[1]
                color = '#fbbf24' if shot['shot_outcome'] == 'Goal' else '#ef4444'
                size = 12 if shot['shot_outcome'] == 'Goal' else 6

                legend_name = f"{shot['player']} - {shot['shot_outcome']}"

                fig_cy.add_trace(go.Scatter(
                    x=[x], y=[y], mode='markers',
                    marker=dict(size=size, color=color, symbol='circle', line=dict(color='black', width=1)),
                    name=legend_name,
                    legendgroup=legend_name,
                    showlegend=(idx == 0),
                    hovertext=f"Jugador: {shot['player']}<br>Minuto: {shot['minute']}<br>Resultado: {shot['shot_outcome']}"
                ))
            except:
                pass
                
        fig_cy.update_layout(
            title='Ubicación de los 35 goles y tiros de Cole & Yorke',
            xaxis=dict(range=[60, 120], showgrid=False, zeroline=False),
            yaxis=dict(range=[0, 80], showgrid=False, zeroline=False),
            plot_bgcolor='#1a472a',
            height=500,
            showlegend=True
        )
        st.plotly_chart(fig_cy, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🔗 Red de Pases entre la Dupla")
        st.info("En esta reconstrucción, se simularon 80 combinaciones directas de pase entre ambos delanteros, reflejando su química en el último tercio de la cancha.")
        
        pass_df = cy_df[cy_df['type'] == 'Pass']
        st.dataframe(pass_df[['minute', 'player', 'pass_recipient']].head(20), use_container_width=True)
        
    else:
        st.warning("⚠️ No se encontró el archivo 'cole_yorke_99_events.csv'. Ejecuta primero el script de generación.")

# ============================================
# PÁGINA 6: EDITOR DE FORMACIONES (NUEVA)
# ============================================
elif page == "⚙️ Editor de Formaciones":
    st.header("⚙️ Editor de Formaciones Tácticas")
    st.markdown("Diseña la alineación de tu equipo con formaciones profesionales")
    
    # Selector de formación
    formations = {
        "4-3-3": {"DEF": 4, "MID": 3, "FWD": 3},
        "4-4-2": {"DEF": 4, "MID": 4, "FWD": 2},
        "3-5-2": {"DEF": 3, "MID": 5, "FWD": 2},
        "5-2-2-1": {"DEF": 5, "MID": 2, "AM": 2, "FWD": 1},
        "4-2-3-1": {"DEF": 4, "DM": 2, "AM": 3, "FWD": 1}
    }
    
    selected_formation = st.selectbox(
        "Selecciona una formación:",
        list(formations.keys()),
        index=0
    )
    
    formation = formations[selected_formation]
    
    # Visualización de la cancha
    fig_pitch = go.Figure()
    
    # Dibujar cancha
    fig_pitch.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80,
                        line=dict(color="white", width=3), fillcolor="#1a472a", opacity=0.9)
    
    # Línea de medio campo
    fig_pitch.add_shape(type="line", x0=60, y0=0, x1=60, y1=80,
                        line=dict(color="white", width=2))
    
    # Círculo central
    fig_pitch.add_shape(type="circle", x0=50, y0=30, x1=70, y1=50,
                        line=dict(color="white", width=2))
    
    # Áreas
    fig_pitch.add_shape(type="rect", x0=0, y0=20, x1=20, y1=60,
                        line=dict(color="white", width=2))
    fig_pitch.add_shape(type="rect", x0=100, y0=20, x1=120, y1=60,
                        line=dict(color="white", width=2))
    
    # Posiciones de jugadores según formación
    positions = []
    
    # Portero
    positions.append({"x": 10, "y": 40, "label": "POR", "color": "#fbbf24"})
    
    # Defensores
    def_count = formation.get("DEF", 4)
    for i in range(def_count):
        x = 30
        y = 15 + (i * (50 / (def_count - 1))) if def_count > 1 else 40
        positions.append({"x": x, "y": y, "label": f"DEF {i+1}", "color": "#3b82f6"})
    
    # Mediocampistas
    mid_count = formation.get("MID", 0)
    dm_count = formation.get("DM", 0)
    am_count = formation.get("AM", 0)
    
    if mid_count > 0:
        for i in range(mid_count):
            x = 60
            y = 15 + (i * (50 / (mid_count - 1))) if mid_count > 1 else 40
            positions.append({"x": x, "y": y, "label": f"MID {i+1}", "color": "#10b981"})
    
    if dm_count > 0:
        for i in range(dm_count):
            x = 50
            y = 25 + (i * (30 / (dm_count - 1))) if dm_count > 1 else 40
            positions.append({"x": x, "y": y, "label": f"DM {i+1}", "color": "#8b5cf6"})
    
    if am_count > 0:
        for i in range(am_count):
            x = 75
            y = 20 + (i * (40 / (am_count - 1))) if am_count > 1 else 40
            positions.append({"x": x, "y": y, "label": f"AM {i+1}", "color": "#ec4899"})
    
    # Delanteros
    fwd_count = formation.get("FWD", 0)
    for i in range(fwd_count):
        x = 95
        y = 20 + (i * (40 / (fwd_count - 1))) if fwd_count > 1 else 40
        positions.append({"x": x, "y": y, "label": f"FWD {i+1}", "color": "#ef4444"})
    
    # Agregar jugadores a la cancha
    for pos in positions:
        fig_pitch.add_trace(go.Scatter(
            x=[pos["x"]], y=[pos["y"]],
            mode='markers+text',
            marker=dict(size=30, color=pos["color"], symbol='circle',
                       line=dict(color='white', width=2)),
            text=[pos["label"]],
            textposition='middle center',
            textfont=dict(color='white', size=10, weight='bold'),
            name=pos["label"],
            showlegend=False
        ))
    
    fig_pitch.update_layout(
        title=f'Formación {selected_formation}',
        xaxis=dict(range=[0, 120], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 80], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='#1a472a',
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig_pitch, use_container_width=True)
    
    # Editor de jugadores
    st.markdown("---")
    st.subheader("👥 Alineación de Jugadores")
    
    num_players = sum(formation.values()) + 1  # +1 para el portero
    
    player_data = []
    for i, pos in enumerate(positions):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**{pos['label']}**")
        with col2:
            player_name = st.text_input(f"Jugador {pos['label']}", value=f"Jugador {i+1}", key=f"player_{i}")
            player_data.append({"position": pos['label'], "player": player_name})
    
    # Guardar formación
    if st.button("💾 Guardar Formación", type="primary"):
        st.session_state['saved_formation'] = {
            "formation": selected_formation,
            "players": player_data
        }
        st.success(f"✅ Formación {selected_formation} guardada exitosamente!")
    
    # Mostrar formación guardada
    if 'saved_formation' in st.session_state:
        st.markdown("---")
        st.subheader("📋 Formación Guardada")
        saved = st.session_state['saved_formation']
        st.info(f"**Formación:** {saved['formation']}")
        
        for player in saved['players']:
            st.markdown(f"- **{player['position']}**: {player['player']}")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 20px;'>
    <p style='font-size: 14px;'>⚽ Tactical Pad Pro - Dashboard Profesional de Análisis de Fútbol</p>
    <p style='font-size: 12px;'>Datos proporcionados por StatsBomb (Open Data)</p>
    <p style='font-size: 11px; margin-top: 10px;'>Desarrollado con Streamlit, Plotly y Python</p>
</div>
""", unsafe_allow_html=True)