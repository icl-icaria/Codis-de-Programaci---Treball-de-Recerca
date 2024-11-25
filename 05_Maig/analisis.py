import pandas as pd
import matplotlib.pyplot as plt

# Importació de dades

df = pd.read_csv("dades_2024-05.csv", skiprows=[1])
# print(df.describe())
# print(df.dtypes)

# Dades de rellevància
# - Data com a índex
# - Conversió a nombre
df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace=True)

df.replace('---', 'NaN', inplace=True)
df['Outdoor temperature'] = df['Outdoor temperature'].astype(float)
df['Barometric pressure (Absolute)'] = df[
    'Barometric pressure (Absolute)'].astype(float)
df['Outdoor humidity'] = df['Outdoor humidity'].astype(float)
df['Daily rainfall'] = df['Daily rainfall'].astype(float)

# Dades diàries
df_diari = df[['Outdoor temperature',
               'Outdoor humidity',
               'Barometric pressure (Absolute)']].resample('D').mean()
df_diari['Precipitació'] = df[['Daily rainfall']].resample('D').max()


noves_columnes = {'Outdoor temperature': 'Temperatura',
                  'Outdoor humidity': 'Humitat',
                  'Barometric pressure (Absolute)': 'Pressió atmosfèrica'
                  }
df_diari = df_diari.rename(columns=noves_columnes)

df_diari.to_csv('dades_diaries_2024-05.csv')

temps = df_diari.index
temperatura = df_diari['Temperatura']
pressio = df_diari['Pressió atmosfèrica']
humitat = df_diari['Humitat']
pluja = df_diari['Precipitació']

# Gràfic
fig, eixos = plt.subplots(2, 2)
eixos[0, 0].plot(temps, temperatura)
eixos[0, 0].set(ylabel='Temperatura [°C]')
eixos[0, 1].plot(temps, pressio)
eixos[0, 1].set(ylabel='Pressió [hPa]')
eixos[1, 0].plot(temps, humitat)
eixos[1, 0].set(ylabel='Humitat relativa [%]')
eixos[1, 1].bar(temps, pluja)
eixos[1, 1].set(ylabel='Precipitació [mm]')

xmin = temps.min()
xmax = temps.max()

for ax in eixos.flat:
    ax.set_xticks([])
    ax.set_xlim([xmin, xmax])

fig.suptitle('Dates meteorològiques diàries')
plt.show()
