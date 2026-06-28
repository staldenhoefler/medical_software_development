"""Generate the figure for the Task 10 presentation from the Task 9 dataset.

Scientific question: Do tremors appear at different times and with different
intensities? We use the magnitude of the gyroscope signal as a tremor proxy
and plot it over time.
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA = '../09_data_collection_app/data/data.json'

with open(DATA, 'r') as f:
    records = json.load(f)

df = pd.json_normalize(records)
df.columns = [c.replace('data.', '') for c in df.columns]
df[['x', 'y', 'z']] = pd.DataFrame(df['data'].tolist(), index=df.index)
df = df.drop(columns=['data'])
df['t_rel'] = (df['timestamp'] - df['timestamp'].min()) / 1e9
df['magnitude'] = np.sqrt(df['x']**2 + df['y']**2 + df['z']**2)

# Gyroscope (sensorType 4): angular speed magnitude over time.
gyro = df[df['sensorType'] == 4].sort_values('t_rel')

# ---------------------------------------------------------------------------
# Sliding variance of the gyroscope magnitude.
# In production this window would span hours/days; on this short demo
# recording we use a few-second window to illustrate the idea.
# ---------------------------------------------------------------------------
WINDOW_S = 3.0  # sliding window length in seconds

g = gyro.set_index(pd.to_timedelta(gyro['t_rel'], unit='s'))
g['variance'] = g['magnitude'].rolling(f'{WINDOW_S}s').var()

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(gyro['t_rel'], gyro['magnitude'], color='0.7', lw=1,
        label='angular speed |ω|')
ax.plot(g['t_rel'], g['variance'], color='tab:red', lw=2,
        label=f'sliding variance ({WINDOW_S:g}s window)')
ax.set_xlabel('Time [s]')
ax.set_ylabel('|ω| [rad/s]  /  variance [(rad/s)$^2$]')
ax.set_title('Sliding variance of gyroscope magnitude')
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('figures/sliding_variance.pdf')
fig.savefig('figures/sliding_variance.png', dpi=150)

print(f"Sliding variance ({WINDOW_S:g}s): "
      f"max={g['variance'].max():.2f} at t={g['t_rel'][g['variance'].idxmax()]:.1f}s")
