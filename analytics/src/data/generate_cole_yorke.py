# analytics/src/data/generate_cole_yorke.py
# Genera un dataset histórico realista de la dupla Cole & Yorke (Temporada 98/99)

import pandas as pd
import numpy as np
import os

output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
os.makedirs(output_dir, exist_ok=True)

events = []

# 1. Pases de Yorke a Cole (Simulando sus famosas 10 asistencias y combinaciones)
for _ in range(45):
    events.append({
        'minute': np.random.randint(1, 90),
        'type': 'Pass',
        'player': 'Dwight Yorke',
        'team': 'Manchester United',
        'pass_recipient': 'Andy Cole',
        'location': f"[{np.random.randint(50, 80)}, {np.random.randint(20, 60)}]"
    })

# 2. Pases de Cole a Yorke (Sus 8 asistencias y combinaciones)
for _ in range(35):
    events.append({
        'minute': np.random.randint(1, 90),
        'type': 'Pass',
        'player': 'Andy Cole',
        'team': 'Manchester United',
        'pass_recipient': 'Dwight Yorke',
        'location': f"[{np.random.randint(50, 80)}, {np.random.randint(20, 60)}]"
    })

# 3. Tiros de Yorke (18 goles + 25 tiros fallidos)
for _ in range(18):
    events.append({
        'minute': np.random.randint(1, 90),
        'type': 'Shot',
        'player': 'Dwight Yorke',
        'team': 'Manchester United',
        'shot_outcome': 'Goal',
        'location': f"[{np.random.randint(88, 115)}, {np.random.randint(30, 50)}]"
    })
for _ in range(25):
    events.append({
        'minute': np.random.randint(1, 90),
        'type': 'Shot',
        'player': 'Dwight Yorke',
        'team': 'Manchester United',
        'shot_outcome': 'Off Target',
        'location': f"[{np.random.randint(75, 115)}, {np.random.randint(10, 70)}]"
    })

# 4. Tiros de Cole (17 goles + 20 tiros atajados/fallidos)
for _ in range(17):
    events.append({
        'minute': np.random.randint(1, 90),
        'type': 'Shot',
        'player': 'Andy Cole',
        'team': 'Manchester United',
        'shot_outcome': 'Goal',
        'location': f"[{np.random.randint(88, 115)}, {np.random.randint(30, 50)}]"
    })
for _ in range(20):
    events.append({
        'minute': np.random.randint(1, 90),
        'type': 'Shot',
        'player': 'Andy Cole',
        'team': 'Manchester United',
        'shot_outcome': 'Saved',
        'location': f"[{np.random.randint(75, 115)}, {np.random.randint(10, 70)}]"
    })

# Crear DataFrame y guardar
df = pd.DataFrame(events)
file_path = os.path.join(output_dir, "cole_yorke_99_events.csv")
df.to_csv(file_path, index=False, encoding="utf-8")

print(f"✅ Dataset histórico generado con {len(df)} eventos.")
print(f"📁 Guardado en: {file_path}")
print(f"⚽ Goles simulados: Yorke (18), Cole (17)")
print(f"🔗 Pases entre ellos: {len(df[df['type'] == 'Pass'])}")