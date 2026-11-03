# analytics/src/data/download_statsbomb.py
# Descarga datos reales de fútbol desde StatsBomb (Champions League 2018/2019)

import pandas as pd
from statsbombpy import sb
import os

# Crear carpeta de salida
output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
os.makedirs(output_dir, exist_ok=True)

print("⚽ Descargando datos de StatsBomb (datos abiertos gratuitos)...")

# 1. Obtener competiciones
competitions = sb.competitions()
print(f"\n📋 Competiciones disponibles: {len(competitions)}")

# 2. Filtrar Champions League 2018/2019
champions = competitions[
    (competitions["competition_name"] == "Champions League") & 
    (competitions["season_name"] == "2018/2019")
]
print(f"\n🏆 Champions League 2018/2019 encontrada: {len(champions)} registros")

if len(champions) > 0:
    competition_id = champions.iloc[0]["competition_id"]
    season_id = champions.iloc[0]["season_id"]
    print(f"competition_id: {competition_id}, season_id: {season_id}")
    
    # 3. Obtener partidos
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    print(f"\n⚽ Partidos encontrados: {len(matches)}")
    
    # 🔍 DEBUG: Mostrar columnas reales
    print(f"\n🔍 Columnas del DataFrame de partidos:")
    print(matches.columns.tolist())
    print(f"\nPrimer partido (todas las columnas):")
    print(matches.iloc[0])
    
    # 4. Guardar partidos en CSV (todas las columnas)
    matches_path = os.path.join(output_dir, "champions_2019_matches.csv")
    matches.to_csv(matches_path, index=False, encoding="utf-8")
    print(f"\n✅ Partidos guardados en: {matches_path}")
    
    # 5. Descargar eventos de la FINAL (Tottenham vs Liverpool, match_id 3788741)
    final_match_id = 3788741
    print(f"\n📊 Descargando eventos de la FINAL (Tottenham vs Liverpool)...")
    
    events = sb.events(match_id=final_match_id)
    print(f"Eventos descargados: {len(events)}")
    
    # 🔍 DEBUG: Mostrar columnas de eventos
    print(f"\n🔍 Columnas del DataFrame de eventos:")
    print(events.columns.tolist())
    print(f"\nTop 10 tipos de evento:")
    if 'type' in events.columns:
        print(events['type'].value_counts().head(10))
    
    # 6. Guardar eventos en CSV
    events_path = os.path.join(output_dir, "champions_2019_final_events.csv")
    events.to_csv(events_path, index=False, encoding="utf-8")
    print(f"\n✅ Eventos guardados en: {events_path}")
    
    # 7. Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DE DATOS DESCARGADOS")
    print("="*50)
    print(f"Partidos: {matches_path}")
    print(f"Eventos de la final: {events_path}")
    print(f"Total eventos: {len(events)}")
    
else:
    print("❌ No se encontró la Champions League 2018/2019")

print("\n🎉 ¡Descarga completada!")