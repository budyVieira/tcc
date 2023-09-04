from joblib import load
import pandas as pd
import numpy as np
import json

# Configurar para exibir todas as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Carregar o modelo treinado
model = load('modelo_init.joblib')

# Exemplo de dados de entrada para a previsão
df = pd.read_csv('Dataset/crime_dataset_clean.csv', encoding='latin-1', low_memory=False)
df = df.drop(['Descricao', 'CrimeOcorreu', 'Categoria', 'Endereco', 'Data', 'DiaSemana'], axis=1)

# Obter as probabilidades estimadas de cada estimador individual
probabilities = np.zeros((len(model.estimators_), len(model.classes_)))  # Array para armazenar as probabilidades

zonas = []



for j in range(df.shape[0]):
    data = pd.DataFrame({
        'Longitude': [df.loc[j, "Longitude"]],
        'Latitude': [df.loc[j, "Latitude"]],
        'DiaSemana_encoded': [df.loc[j, "DiaSemana_encoded"]],
        'Distrito_BAYVIEW': [df.loc[j, "Distrito_BAYVIEW"]],
        'Distrito_CENTRAL': [df.loc[j, "Distrito_CENTRAL"]],
        'Distrito_INGLESIDE': [df.loc[j, "Distrito_INGLESIDE"]],
        'Distrito_MISSION': [df.loc[j, "Distrito_MISSION"]],
        'Distrito_NORTHERN': [df.loc[j, "Distrito_NORTHERN"]],
        'Distrito_PARK': [df.loc[j, "Distrito_PARK"]],
        'Distrito_RICHMOND': [df.loc[j, "Distrito_RICHMOND"]],
        'Distrito_SOUTHERN': [df.loc[j, "Distrito_SOUTHERN"]],
        'Distrito_TARAVAL': [df.loc[j, "Distrito_TARAVAL"]],
        'Distrito_TENDERLOIN': [df.loc[j, "Distrito_TENDERLOIN"]],
        'Distrito_LUANDA': [df.loc[j, "Distrito_LUANDA"]],
        'Ano': [df.loc[j, "Ano"]],
        'Mes': [df.loc[j, "Mes"]],
        'Dia': [df.loc[j, "Dia"]],
        'Hora': [df.loc[j, "Hora"]],
        'Minuto': [df.loc[j, "Minuto"]],

    })
    for i, estimator in enumerate(model.estimators_):
        probabilities[i] = estimator.predict_proba(data)

    # Calcular a média das probabilidades estimadas
    average_probability = np.mean(probabilities, axis=0)

    # Obter a probabilidade para a classe de interesse (crime)
    crime_probability = average_probability[model.classes_ == 1]
    previsao = crime_probability[0] * 100
    previsao = round(previsao, 2)

    if previsao > 49:
        zonas.append({'lat': df.iloc[i, 1], 'long': df.iloc[i, 0], 'ano': df.iloc[i, 14],
                      'mes': df.iloc[i, 15],'dia': df.iloc[i, 16],'hora': df.iloc[i, 17],
                      'probabilidade': previsao})


# Converta o vetor de dicionário em formato JSON
json_vector = json.dumps(zonas)

# Salve o vetor de dicionário em um arquivo
with open("zonas_de_perigo.json", "w") as f:
    f.write(json_vector)


