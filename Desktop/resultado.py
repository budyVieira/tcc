from joblib import load
import pandas as pd
import numpy as np


# Configurar para exibir todas as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Carregar o modelo treinado
model = load('modelo_init.joblib')

# Exemplo de dados de entrada para a previsão
data = pd.DataFrame({
    'Longitude': [-8.9227],
    'Latitude': [13.1858],
    'DiaSemana_encoded': [1],
    'Distrito_BAYVIEW': [0],
    'Distrito_CENTRAL': [0],
    'Distrito_INGLESIDE': [0],
    'Distrito_MISSION': [0],
    'Distrito_NORTHERN': [0],
    'Distrito_PARK': [0],
    'Distrito_RICHMOND': [0],
    'Distrito_SOUTHERN': [0],
    'Distrito_TARAVAL': [0],
    'Distrito_TENDERLOIN': [0],
    'Distrito_LUANDA': [1],
    'Ano': [2023],
    'Mes': [8],
    'Dia': [15],
    'Hora': [18],
    'Minuto': [55],

})


# Obter as probabilidades estimadas de cada estimador individual
probabilities = np.zeros((len(model.estimators_), len(model.classes_)))  # Array para armazenar as probabilidades
for i, estimator in enumerate(model.estimators_):
    probabilities[i] = estimator.predict_proba(data)

# Calcular a média das probabilidades estimadas
average_probability = np.mean(probabilities, axis=0)

# Obter a probabilidade para a classe de interesse (crime)
crime_probability = average_probability[model.classes_ == 1]
previsao = crime_probability[0] * 100
previsao = round(previsao, 2)
# Imprimir a probabilidade
print("Probabilidade de ocorrer um crime:", previsao, "%")


