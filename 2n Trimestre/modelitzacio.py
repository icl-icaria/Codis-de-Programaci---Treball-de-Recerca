import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def obtenir_dades():
    '''Llegeix el fitxer CSV i el prepara per a treballar amb les conversions necessàries.
    return:
        - df:dataFrame
    '''
    nom_fitxer = 'dades_diaries_2024-04_06.csv'
    df = pd.read_csv(nom_fitxer)
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)

    # Diferència pressió amb el dia anterior
    df['Diferència pressió'] = df['Pressió atmosfèrica'].diff()

    # Reordenar les columnes i afegir unitats
    df = df[['Temperatura',
             'Humitat',
             'Pressió atmosfèrica',
             'Precipitació'
             ]]

    # Afegir unitats a les etiquetes de les columnes
    df.columns = ['Temperatura (ºC)', 
                  'Humitat (%)', 
                  'Pressió atmosfèrica (hPa)', 
                  'Precipitació (mm)']

    # Elimina les files amb valors no numèrics
    df.dropna(inplace=True)

    return df


def matriu_punts(df):
    '''Crea i mostra la matriu de dispersió de les dades que estan en un DataFrame'''

    sns.pairplot(df, kind="reg",
                 plot_kws=dict(scatter_kws=dict(s=0.5)))
    plt.show()


def matriu_correlacio(df):
    '''Crea i mostra la matriu de correlació entre les dades'''

    corr = df.corr(method="pearson")
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.xticks(rotation=0, ha='center')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()


def entrenar_model(df):
    ''' Crea y entrena un model de regressió lineal multivariable'''

    model = linear_model.LinearRegression()

    # Divisió de les dades en train y test
    x = df[['Temperatura (ºC)',
            'Humitat (%)',
            'Pressió atmosfèrica (hPa)'
            ]]
    y = df['Precipitació (mm)']
    x_train, x_test, y_train, y_test = train_test_split(
                                            x,
                                            y,
                                            train_size=0.8
                                            )

    # Entrena (ajusta) el model a les dades d'entrenament (train)
    model = model.fit(x_train, y_train)

    # Càlcul de l'arrel del error quadràtic mig
    y_predicted = model.predict(x_test)
    rmse = mean_squared_error(y_test, y_predicted, squared=False)
    print(f"L'error RMSE del model és: {rmse:.2f}")

    # Càlcul del coeficient de correlació R2
    r2 = model.score(x_test, y_test)
    print(f"R2 Score value: {r2:.4f}")

    return model, r2


if __name__ == '__main__':
    df = obtenir_dades()
    matriu_punts(df)
    matriu_correlacio(df)
    model, r2 = entrenar_model(df)
