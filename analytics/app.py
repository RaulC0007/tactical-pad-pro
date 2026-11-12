# analytics/app.py
# Dashboard Streamlit para análisis de fútbol

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import ast

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Tactical Pad - Análisis de Fútbol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.title("⚽ Tactical Pad Pro - Análisis de Fútbol")
st.markdown("### Dashboard de Análisis con Datos Reales de StatsBomb")
st.markdown("---")

# ============================================
# RUTAS DE LOS DATOS
# ============================================
data_dir = Path(__file__).parent / "data" / "raw"
matches_file = data_dir / "champions_2019_matches.csv"
events_file = data_dir / "champions_2019_final_events.csv"
cy_file = data_dir / "cole_yorke_99_events.csv"

# ============================================
# CARGAR DATOS
# ============================================
@st.cache_data
def load_data():
    matches = pd.read_csv(matches_file)
    events = pd.read_csv(events_file)
    return matches, events

matches_df, events_df = load_data()

# ============================================
# SIDEBAR - NAVEGACIÓN
# ============================================
st.sidebar.title("🎯 Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "📊 Resumen del Partido",
        "⚽ Análisis de Eventos",
        "🎯 Mapa de Tiros",
        "👥 Comparación de Equipos",
        "👑 Cole & Yorke 98/99",
        "⚙️ Editor de Formaciones"
    ]
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
# FUNCIÓN AUXILIAR: DIBUJAR CANCHA
# ============================================
def draw_pitch(fig, x0=0, y0=0, x1=120, y1=80, layer='below'):
    """Dibuja una cancha de fútbol con layer='below' para que quede detrás."""
    # Fondo de la cancha
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                  line=dict(color="white", width=3), fillcolor="#1a472a", opacity=1,
                  layer=layer)
    # Línea de medio campo
    mid_x = (x0 + x1) / 2
    fig.add_shape(type="line", x0=mid_x, y0=y0, x1=mid_x, y1=y1,
                  line=dict(color="white", width=2), layer=layer)
    # Círculo central
    fig.add_shape(type="circle", x0=mid_x-10, y0=30, x1=mid_x+10, y1=50,
                  line=dict(color="white", width=2), layer=layer)
    # Área izquierda
    fig.add_shape(type="rect", x0=x0, y0=20, x1=x0+20, y1=60,
                  line=dict(color="white", width=2), layer=layer)
    # Área derecha
    fig.add_shape(type="rect", x0=x1-20, y0=20, x1=x1, y1=60,
                  line=dict(color="white", width=2), layer=layer)
    # Área pequeña izquierda
    fig.add_shape(type="rect", x0=x0, y0=30, x1=x0+8, y1=50,
                  line=dict(color="white", width=1.5), layer=layer)
    # Área pequeña derecha
    fig.add_shape(type="rect", x0=x1-8, y0=30, x1=x1, y1=50,
                  line=dict(color="white", width=1.5), layer=layer)
    return fig

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
        color_discrete_sequence=['#132257', '#C8102E']
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

    # PRIMERO: agregar los puntos (para que queden encima de la cancha)
    for idx, shot in shots.iterrows():
        if pd.notna(shot.get('location')):
            try:
                location = ast.literal_eval(shot['location'])
                x, y = location[0], location[1]

                color = '#FFD700' if shot.get('shot_outcome') == 'Goal' else '#FF4444'
                size = 18 if shot.get('shot_outcome') == 'Goal' else 10

                fig_shots.add_trace(go.Scatter(
                    x=[x], y=[y], mode='markers',
                    marker=dict(
                        size=size, color=color, symbol='circle',
                        line=dict(color='black', width=2)
                    ),
                    name=f"{shot.get('player', 'Unknown')} - {shot.get('shot_outcome', 'Unknown')}",
                    hovertext=f"Jugador: {shot.get('player', 'Unknown')}<br>Minuto: {shot.get('minute', 'N/A')}"
                ))
            except:
                pass

    # DESPUÉS: agregar la cancha con layer='below'
    draw_pitch(fig_shots)

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
        goals = len(shots[shots['shot_outcome'] == 'Goal']) if 'shot_outcome' in shots.columns else 0
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

        # PRIMERO: agregar los puntos (para que queden encima de la cancha)
        for idx, shot in shots.iterrows():
            try:
                location = ast.literal_eval(shot['location'])
                x, y = location[0], location[1]
                color = '#FFD700' if shot['shot_outcome'] == 'Goal' else '#FF4444'
                size = 18 if shot['shot_outcome'] == 'Goal' else 12

                legend_name = f"{shot['player']} - {shot['shot_outcome']}"

                fig_cy.add_trace(go.Scatter(
                    x=[x], y=[y], mode='markers',
                    marker=dict(size=size, color=color, symbol='circle',
                              line=dict(color='black', width=2)),
                    name=legend_name,
                    legendgroup=legend_name,
                    showlegend=(idx == 0),
                    hovertext=f"Jugador: {shot['player']}<br>Minuto: {shot['minute']}<br>Resultado: {shot['shot_outcome']}"
                ))
            except:
                pass

        # DESPUÉS: agregar la cancha con layer='below'
        fig_cy.add_shape(type="rect", x0=60, y0=0, x1=120, y1=80,
                         line=dict(color="white", width=3), fillcolor="#1a472a", opacity=1,
                         layer='below')
        fig_cy.add_shape(type="rect", x0=103.5, y0=21.1, x1=120, y1=58.9,
                         line=dict(color="white", width=2), fillcolor="none",
                         layer='below')

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
# PÁGINA 6: EDITOR DE FORMACIONES
# ============================================
elif page == "⚙️ Editor de Formaciones":
    st.header("⚙️ Editor de Formaciones Tácticas")
    st.markdown("Diseña la alineación de tu equipo con formaciones profesionales")

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

    fig_pitch = go.Figure()

    # Calcular posiciones de jugadores
    positions = []

    # Portero (amarillo brillante)
    positions.append({"x": 10, "y": 40, "label": "POR", "color": "#FFD700", "size": 40})

    # Defensores (azul brillante)
    def_count = formation.get("DEF", 4)
    for i in range(def_count):
        x = 30
        y = 15 + (i * (50 / (def_count - 1))) if def_count > 1 else 40
        positions.append({"x": x, "y": y, "label": f"DEF {i+1}", "color": "#3B82F6", "size": 40})

    # Mediocampistas (verde brillante)
    mid_count = formation.get("MID", 0)
    dm_count = formation.get("DM", 0)
    am_count = formation.get("AM", 0)

    if mid_count > 0:
        for i in range(mid_count):
            x = 60
            y = 15 + (i * (50 / (mid_count - 1))) if mid_count > 1 else 40
            positions.append({"x": x, "y": y, "label": f"MID {i+1}", "color": "#10B981", "size": 40})

    if dm_count > 0:
        for i in range(dm_count):
            x = 50
            y = 25 + (i * (30 / (dm_count - 1))) if dm_count > 1 else 40
            positions.append({"x": x, "y": y, "label": f"DM {i+1}", "color": "#8B5CF6", "size": 40})

    if am_count > 0:
        for i in range(am_count):
            x = 75
            y = 20 + (i * (40 / (am_count - 1))) if am_count > 1 else 40
            positions.append({"x": x, "y": y, "label": f"AM {i+1}", "color": "#EC4899", "size": 40})

    # Delanteros (rojo brillante)
    fwd_count = formation.get("FWD", 0)
    for i in range(fwd_count):
        x = 95
        y = 20 + (i * (40 / (fwd_count - 1))) if fwd_count > 1 else 40
        positions.append({"x": x, "y": y, "label": f"FWD {i+1}", "color": "#EF4444", "size": 40})

    # PRIMERO: agregar los jugadores (para que queden encima de la cancha)
    for pos in positions:
        fig_pitch.add_trace(go.Scatter(
            x=[pos["x"]], y=[pos["y"]],
            mode='markers+text',
            marker=dict(size=pos["size"], color=pos["color"], symbol='circle',
                       line=dict(color='white', width=3)),
            text=[pos["label"]],
            textposition='middle center',
            textfont=dict(color='white', size=12, weight='bold'),
            name=pos["label"],
            showlegend=False
        ))

    # DESPUÉS: agregar la cancha con layer='below'
    draw_pitch(fig_pitch)

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

    player_data = []
    for i, pos in enumerate(positions):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**{pos['label']}**")
        with col2:
            player_name = st.text_input(
                f"Jugador {pos['label']}",
                value=f"Jugador {i+1}",
                key=f"player_{i}"
            )
            player_data.append({"position": pos['label'], "player": player_name})

    if st.button("💾 Guardar Formación", type="primary"):
        st.session_state['saved_formation'] = {
            "formation": selected_formation,
            "players": player_data
        }
        st.success(f"✅ Formación {selected_formation} guardada exitosamente!")

    if 'saved_formation' in st.session_state:
        st.markdown("---")
        st.subheader("📋 Formación Guardada")
        saved = st.session_state['saved_formation']
        st.info(f"**Formación:** {saved['formation']}")

        for player in saved['players']:
            st.markdown(f"- **{player['position']}**: {player['player']}")

# ============================================
# FOOTER (SIEMPRE AL FINAL)
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>⚽ Tactical Pad Pro - Dashboard de Análisis de Fútbol</p>
    <p>Datos proporcionados por StatsBomb (Open Data)</p>
</div>
""", unsafe_allow_html=True)