import pandas as pd
import numpy as np

from joblib import dump

# Configurar para exibir todas as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Carregar o dataset
df = pd.read_csv('Dataset/train.csv', encoding='latin-1')


df = df.dropna()  # Remoção de linhas com dados ausentes

# Definir os valores válidos para a coluna 'Resolution'
valores_validos = ['ARREST, BOOKED', 'ARREST, CITED', 'NONE']

# Filtrar as linhas com valores válidos na coluna 'Resolution'
df = df[df['Resolution'].isin(valores_validos)]

# Mudar a coluna target para balores bool
df['Resolution'] = df['Resolution'].replace('ARREST, BOOKED', 1)
df['Resolution'] = df['Resolution'].replace('ARREST, CITED', 1)
df['Resolution'] = df['Resolution'].replace('NONE', 0)

# Converter a coluna 'Resolution' para tipo 'bool'
df['Resolution'] = df['Resolution'].astype(bool)

#Tradução de dias de semana
df['DayOfWeek'] = df['DayOfWeek'].replace('Monday', 'Segunda')
df['DayOfWeek'] = df['DayOfWeek'].replace('Tuesday', 'Terca')
df['DayOfWeek'] = df['DayOfWeek'].replace('Wednesday', 'Quarta')
df['DayOfWeek'] = df['DayOfWeek'].replace('Thursday', 'Quinta')
df['DayOfWeek'] = df['DayOfWeek'].replace('Friday', 'Sexta')
df['DayOfWeek'] = df['DayOfWeek'].replace('Saturday', 'Sabado')
df['DayOfWeek'] = df['DayOfWeek'].replace('Sunday', 'Domingo')


# Definir os valores válidos para a coluna 'Category'
valores_validos = ['LARCENY/THEFT', 'ASSAULT', 'VEHICLE THEFT', 'BURGLARY', 'ROBBERY', 'MISSING PERSON', 'STOLEN PROPERTY', 'SEX OFFENSES FORCIBLE', 'KIDNAPPING', 'SEX OFFENSES NON FORCIBLE']

# Filtrar as linhas com valores válidos na coluna 'Category'
df = df[df['Category'].isin(valores_validos)]

#Tradução de Category
df['Category'] = df['Category'].replace('LARCENY/THEFT', 'ROUBO')
df['Category'] = df['Category'].replace('ASSAULT', 'ASSALTO')
df['Category'] = df['Category'].replace('VEHICLE THEFT', 'ROUBO DE VEICULOS')
df['Category'] = df['Category'].replace('BURGLARY', 'ROUBO')
df['Category'] = df['Category'].replace('ROBBERY', 'ROUBO')
df['Category'] = df['Category'].replace('MISSING PERSON', 'PESSOA DESAPARECIDA')
df['Category'] = df['Category'].replace('STOLEN PROPERTY', 'PROPRIEDADE ROUBADA')
df['Category'] = df['Category'].replace('SEX OFFENSES FORCIBLE', 'ESTUPRO')
df['Category'] = df['Category'].replace('KIDNAPPING', 'SEQUESTRO')
df['Category'] = df['Category'].replace('SEX OFFENSES NON FORCIBLE', 'ESTUPRO')

# Renomear a coluna
df.rename(columns={'Dates': 'Data'}, inplace=True)
df.rename(columns={'Category': 'Categoria'}, inplace=True)
df.rename(columns={'Descript': 'Descricao'}, inplace=True)
df.rename(columns={'DayOfWeek': 'DiaSemana'}, inplace=True)
df.rename(columns={'PdDistrict': 'Distrito'}, inplace=True)
df.rename(columns={'Resolution': 'CrimeOcorreu'}, inplace=True)
df.rename(columns={'Address': 'Endereco'}, inplace=True)
df.rename(columns={'X': 'Longitude'}, inplace=True)
df.rename(columns={'Y': 'Latitude'}, inplace=True)


# Converter a coluna para tipo de dados correto
df['Data'] = df['Data'].astype(str)
df['Categoria'] = df['Categoria'].astype(str)
df['Descricao'] = df['Descricao'].astype(str)
df['DiaSemana'] = df['DiaSemana'].astype(str)
df['Endereco'] = df['Endereco'].astype(str)
df['Longitude'] = df['Longitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

# Label encoding para a coluna DiaSemana
# Dicionário de mapeamento de dias da semana para valores numéricos
dias_semana_mapping = {
    'Segunda': 0,
    'Terca': 1,
    'Quarta': 2,
    'Quinta': 3,
    'Sexta': 4,
    'Sabado': 5,
    'Domingo': 6
}

# Aplicar o mapeamento à coluna 'DiaSemana'
df['DiaSemana_encoded'] = df['DiaSemana'].map(dias_semana_mapping)


# One-hot encoding para a coluna Distrito
df = pd.get_dummies(df, columns=['Distrito'])
df['Distrito_LUANDA'] = False

# Converter a coluna 'Data' para formato datetime
df['Data'] = pd.to_datetime(df['Data'])

# Extrair informações da coluna 'Data' e criar novas colunas
df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month
df['Dia'] = df['Data'].dt.day
df['Hora'] = df['Data'].dt.hour
df['Minuto'] = df['Data'].dt.minute

"""
try:
    # Caminho para o arquivo CSV
    arquivo_csv = 'Dataset/crime_dataset_clean.csv'
    df.to_csv(arquivo_csv, mode='a', header=True, index=False)
except:
  print("Erro ao criar dataset Limpo!")

"""
# print(df.head(5))

# print(df.dtypes)
# ---------------------------------------------------------------------------- #

# Carregar o dataset
#df1 = pd.read_csv('Dataset/test.csv', encoding='latin-1')
#print(df1.head(20))

#print(df.head(10))



from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, precision_score

# Suponha que você tenha 'dados_treino' e 'dados_teste' como seus DataFrames


X = df.drop(['Descricao', 'CrimeOcorreu', 'Categoria', 'Endereco', 'Data', 'DiaSemana'], axis=1)
y = df['CrimeOcorreu']

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)

# Inicializar os classificadores
knn = KNeighborsClassifier(n_neighbors=10)
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
naive_bayes = GaussianNB()

# Treinar os classificadores
knn.fit(X_train, y_train)
decision_tree.fit(X_train, y_train)
random_forest.fit(X_train, y_train)
naive_bayes.fit(X_train, y_train)

# Criar o ensemble
ensemble = VotingClassifier(estimators=[('KNN', knn), ('Decision Tree', decision_tree), ('Random Forest', random_forest), ('Naive Bayes', naive_bayes)], voting='hard')

# Treinar o ensemble
ensemble.fit(X_train, y_train)

from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Inicializar listas para as métricas
matrizes_confusao = []
auc_rocs = []


# Função para calcular métricas e plotar a Curva ROC
def calcular_metricas_e_plotar_roc(modelo, nome):
    # Fazer previsões
    y_pred = modelo.predict(X_test)

    # Calcular a Matriz de Confusão
    matriz_confusao = confusion_matrix(y_test, y_pred)
    matrizes_confusao.append((nome, matriz_confusao))

    # Calcular AUC-ROC
    probabilidade_classes = modelo.predict_proba(X_test)[:, 1]
    auc_roc = roc_auc_score(y_test, probabilidade_classes)
    auc_rocs.append((nome, auc_roc))

    # Plotar a Curva ROC
    fpr, tpr, _ = roc_curve(y_test, probabilidade_classes)
    plt.figure()
    plt.plot(fpr, tpr, label=f"{nome} (AUC = {auc_roc:.2f})")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Taxa de Falso Positivo')
    plt.ylabel('Taxa de Verdadeiro Positivo')
    plt.title(f'Curva ROC para {nome}')
    plt.legend(loc="lower right")


# Calcular métricas para cada modelo
calcular_metricas_e_plotar_roc(knn, "KNN")
calcular_metricas_e_plotar_roc(naive_bayes, "GaussianNB")
calcular_metricas_e_plotar_roc(decision_tree, "Decision Tree")
calcular_metricas_e_plotar_roc(random_forest, "Random Forest")

# Mostrar as Matrizes de Confusão para cada modelo
for nome, matriz_confusao in matrizes_confusao:
    print(f"Matriz de Confusão para {nome}:\n{matriz_confusao}\n")

# Mostrar AUC-ROC para cada modelo
for nome, auc_roc in auc_rocs:
    print(f"AUC-ROC para {nome}: {auc_roc:.2f}")

plt.show()

"""
# Obter as previsões para o conjunto de teste
knn_predictions = knn.predict(X_test)
decision_tree_predictions = decision_tree.predict(X_test)
random_forest_predictions = random_forest.predict(X_test)
naive_bayes_predictions = naive_bayes.predict(X_test)
ensemble_predictions = ensemble.predict(X_test)


# Calcular a precisão para cada algoritmo
knn_precision = precision_score(y_test, knn_predictions)
decision_tree_precision = precision_score(y_test, decision_tree_predictions)
random_forest_precision = precision_score(y_test, random_forest_predictions)
naive_bayes_precision = precision_score(y_test, naive_bayes_predictions)
ensemble_precision = precision_score(y_test, ensemble_predictions)


# Avaliar o desempenho dos algoritmos individuais
print("KNN Accuracy:", knn.score(X_test, y_test))
print("KNN Precision:", knn_precision)

print("-----------------------------------------------------------")
print("Decision Tree Accuracy:", decision_tree.score(X_test, y_test))
print("Decision Tree Precision:", decision_tree_precision)
print("-----------------------------------------------------------")
print("Random Forest Accuracy:", random_forest.score(X_test, y_test))
print("Random Forest Precision:", random_forest_precision)
print("-----------------------------------------------------------")
print("Naive Bayes Accuracy:", naive_bayes.score(X_test, y_test))
print("Naive Bayes Precision:", naive_bayes_precision)
print("-----------------------------------------------------------")
# Avaliar o desempenho do ensemble
print("Ensemble Accuracy:", ensemble.score(X_test, y_test))
print("Ensemble Precision:", ensemble_precision)
"""

# Salvar o modelo treinado
#dump(ensemble, 'modelo_init.joblib')
