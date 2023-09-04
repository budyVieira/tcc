import json

from flask import Flask, render_template, request, jsonify
from joblib import load
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
from joblib import dump
import os

# Configurar para exibir todas as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    distritos_unicos = ["BAYVIEW", "CENTRAL", "INGLESIDE", "MISSION", "NORTHERN", "PARK", "RICHMOND", "SOUTHERN", "TARAVAL", "TENDERLOIN", "LUANDA"]
    # Inicialize um dicionário para criar as colunas binárias
    colunas_distritos = {}
    if request.method == 'POST':
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        data = request.form['data']
        horario = request.form['hora']
        ano = int(data.split('-')[0])
        mes = int(data.split('-')[1])
        dia = int(data.split('-')[2])
        hora = int(horario.split(':')[0])
        minuto = int(horario.split(':')[1])
        distrito = request.form['provincia']
        data_obj = datetime.strptime(data, "%Y-%m-%d").date()
        dia_semana = int(data_obj.weekday())

        dados = pd.DataFrame({
            'Longitude': [longitude],
            'Latitude': [latitude],
            'DiaSemana_encoded': [dia_semana],
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
            'Distrito_LUANDA': [0],
            'Ano': [ano],
            'Mes': [mes],
            'Dia': [dia],
            'Hora': [hora],
            'Minuto': [minuto],
        })
        dados[f"Distrito_{distrito}"] = 1
        # print(dados)
        # Carrega o modelo .joblib
        model = load('modelo/modelo_init.joblib')
        # Realize a previsão com o modelo
        probabilities = np.zeros((len(model.estimators_), len(model.classes_)))  # Array para armazenar as probabilidades
        for i, estimator in enumerate(model.estimators_):
            probabilities[i] = estimator.predict_proba(dados)

        # Calcular a média das probabilidades estimadas
        average_probability = np.mean(probabilities, axis=0)

        # Obter a probabilidade para a classe de interesse (crime)
        crime_probability = average_probability[model.classes_ == 1]
        previsao = crime_probability[0] * 100
        previsao = round(previsao, 2)
        return render_template('index.html', previsao=previsao)

    return render_template('index.html', previsao=None)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        #Receber os dados do formulario
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        data = request.form['data']
        horario = request.form['hora']
        tipo_crime = str(request.form['tipo_crime'])
        desc_crime = str(request.form['desc_crime'])
        rua = str(request.form['street'])
        ano = int(data.split('-')[0])
        mes = int(data.split('-')[1])
        dia = int(data.split('-')[2])
        hora = int(horario.split(':')[0])
        minuto = int(horario.split(':')[1])
        data_obj = datetime.strptime(data, "%Y-%m-%d").date()
        print(data_obj.weekday())
        dia_semana = ["Segunda-Feira" if int(data_obj.weekday()) == 0 else
                      "Terca-Feira" if int(data_obj.weekday()) == 1 else
                      "Quarta-Feira" if int(data_obj.weekday()) == 2 else
                      "Quinta-Feira" if int(data_obj.weekday()) == 3 else
                      "Sexta-Feira" if int(data_obj.weekday()) == 4 else
                      "Sabado" if int(data_obj.weekday()) == 5 else
                      "Domingo"]
        data = data + " " + horario
        distrito = request.form['provincia']

        #Elaboração para o formado do dataset
        dados = pd.DataFrame({
            "Data": [data],
            "Categoria": [tipo_crime],
            "Descricao": [desc_crime],
            "DiaSemana": [dia_semana[0]],
            "CrimeOcorreu": [1],
            "Endereco": [rua],
            "Longitude": [longitude],
            "Latitude": [latitude],
            'DiaSemana_encoded': [int(data_obj.weekday())],
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
            'Distrito_LUANDA': [0],
            'Ano': [ano],
            'Mes': [mes],
            'Dia': [dia],
            'Hora': [hora],
            'Minuto': [minuto],
        })
        dados[f"Distrito_{distrito}"] = 1

        #Adicionar para o arquivo csv
        try:
            # Caminho para o arquivo CSV
            arquivo_csv = 'ocorrencia/crimes_ocorridos_denuncias.csv'
            arquivo_csv1 = 'dataset/crime_dataset_clean.csv'
            dados.to_csv(arquivo_csv, mode='a', header=False, index=False)
            dados.to_csv(arquivo_csv1, mode='a', header=False, index=False)

        except Exception as e:
            return jsonify({'error': str(e)})

        return render_template('form.html', resposta='Ocorrência armazenada com sucesso!!')

    # show the form, it wasn't submitted
    return render_template('form.html')

@app.route('/graficos', methods=['GET', 'POST'])
def graficos():

    # Carregue o arquivo CSV usando o pandas
    df = pd.read_csv('dataset/crime_dataset_clean.csv')

    # Filtrar os dados onde a coluna de interesse tem valor igual a 1
    filtered_df = df[df['CrimeOcorreu'] == 1]


    # Converta os dados do DataFrame pandas para uma estrutura que possa ser usada no gráfico
    count_by_crime = filtered_df['Categoria'].value_counts()
    labels = count_by_crime.index.tolist()
    data = count_by_crime.values.tolist()

    count_by_week_day = filtered_df['DiaSemana'].value_counts()
    labels1 = count_by_week_day.index.tolist()
    data1 = count_by_week_day.values.tolist()

    # Somar cada coluna de distrito para contar as ocorrências por distrito
    distrito_counts = {}
    for col in filtered_df.columns:
        if col.startswith('Distrito_'):
            distrito = col.replace('Distrito_', '')
            distrito_counts[distrito] = int(filtered_df[col].sum())

    return render_template('graficos.html', labels=labels, data=data, labels1=labels1, data1=data1, distrito_counts=distrito_counts)


@app.route('/api/predict', methods=['GET', 'POST'])
def api():

    if request.method == 'POST':
        dados = json.loads(request.data)
        latitude = float(dados['lat'])
        longitude = float(dados['long'])
        ano = int(dados['year'])
        mes = int(dados['month'])
        hora = int(dados['hour'])
        dia_semana = int(dados['diaSemana'])
        dia = int(dados['day'])
        minuto = int(dados['minute'])
        distrito = dados['provincia']

        data = pd.DataFrame({
            'Longitude': [longitude],
            'Latitude': [latitude],
            'DiaSemana_encoded': [dia_semana],
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
            'Distrito_LUANDA': [0],
            'Ano': [ano],
            'Mes': [mes],
            'Dia': [dia],
            'Hora': [hora],
            'Minuto': [minuto],
        })
        dados[f"Distrito_{distrito}"] = 1

        # Carrega o modelo .joblib
        model = load('modelo/modelo_init.joblib')
        # Realize a previsão com o modelo
        probabilities = np.zeros(
            (len(model.estimators_), len(model.classes_)))  # Array para armazenar as probabilidades
        for i, estimator in enumerate(model.estimators_):
            probabilities[i] = estimator.predict_proba(data)

        # Calcular a média das probabilidades estimadas
        average_probability = np.mean(probabilities, axis=0)

        # Obter a probabilidade para a classe de interesse (crime)
        crime_probability = average_probability[model.classes_ == 1]
        previsao = crime_probability[0] * 100
        previsao = round(previsao, 2)

    return jsonify({"probabilidade": previsao})


@app.route('/api/graph', methods=['GET', 'POST'])
def api_graph():
    # Carregue o arquivo CSV usando o pandas
    df = pd.read_csv('dataset/crime_dataset_clean.csv')

    # Filtrar os dados onde a coluna de interesse tem valor igual a 1
    filtered_df = df[df['CrimeOcorreu'] == 1]

    # Converta os dados do DataFrame pandas para uma estrutura que possa ser usada no gráfico
    count_by_crime = filtered_df['Categoria'].value_counts()
    labels = count_by_crime.index.tolist()
    data = count_by_crime.values.tolist()

    dados = {
        "labels" : labels,
        "data": data
    }

    return jsonify({"dados": dados})


@app.route('/api/denuncia', methods=['GET', 'POST'])
def api_denuncia():

    dados = json.loads(request.data)
    latitude = float(dados['lat'])
    longitude = float(dados['long'])
    ano = int(dados['year'])
    mes = int(dados['month'])
    hora = int(dados['hour'])
    dia_semana = int(dados['diaSemana'])
    dia = int(dados['day'])
    minuto = int(dados['minute'])
    distrito = dados['distrito']
    tipo_crime = dados['categoria']
    data = dados['data']
    desc_crime = dados['desc']
    rua = dados['endereco']

    dia_semana_str = ["Segunda-Feira" if dia_semana == 0 else
                      "Terca-Feira" if dia_semana == 1 else
                      "Quarta-Feira" if dia_semana == 2 else
                      "Quinta-Feira" if dia_semana == 3 else
                      "Sexta-Feira" if dia_semana == 4 else
                      "Sabado" if dia_semana == 5 else
                      "Domingo"]


    #Elaboração para o formado do dataset
    dt = pd.DataFrame({
        "Data": [data],
        "Categoria": [tipo_crime],
        "Descricao": [desc_crime],
        "DiaSemana": [dia_semana_str[0]],
        "CrimeOcorreu": [1],
        "Endereco": [rua],
        "Longitude": [longitude],
        "Latitude": [latitude],
        'DiaSemana_encoded': [dia_semana],
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
        'Distrito_LUANDA': [0],
        'Ano': [ano],
        'Mes': [mes],
        'Dia': [dia],
        'Hora': [hora],
        'Minuto': [minuto],
    })

    dt[f"Distrito_{distrito}"] = 1

    #Adicionar para o arquivo csv
    try:
        # Caminho para o arquivo CSV
        arquivo_csv = 'ocorrencia/crimes_ocorridos_denuncias.csv'
        arquivo_csv1 = 'dataset/crime_dataset_clean.csv'
        dados.to_csv(arquivo_csv, mode='a', header=False, index=False)
        dados.to_csv(arquivo_csv1, mode='a', header=False, index=False)

    except Exception as e:
        return jsonify({'error': str(e)})


    return jsonify({"resposta": "Denúncia realizada com sucesso!"})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    #app.run(debug="on")

