import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import precision_score, accuracy_score
from sklearn.naive_bayes import GaussianNB
import joblib

from joblib import dump

# Carregar o dataset
dataset = pd.read_csv('Dataset/crime.csv', encoding='latin-1')

# Configurar para exibir todas as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


dataset = dataset.drop(['INCIDENT_NUMBER', 'OFFENSE_CODE', 'OFFENSE_DESCRIPTION', 'DISTRICT', 'REPORTING_AREA', 'SHOOTING', 'UCR_PART', 'Location'], axis=1)  # Exemplo de remoção de colunas
dataset = dataset.dropna()  # Exemplo de remoção de linhas com dados ausentes

#Tradução de tipo de crime
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Aggravated Assault', 'Agressao')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Homicide', 'Homicidio')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Firearm Violations', 'Armas de Fogo')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Robbery', 'Assalto')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Simple Assault', 'Roubo')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Violations', 'Violacao')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Manslaughter', 'Homicidio')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Auto Theft', 'Roubo')
dataset['OFFENSE_CODE_GROUP'] = dataset['OFFENSE_CODE_GROUP'].replace('Fire Related Reports', 'Armas de Fogo')

#Tradução de dias de semana
dataset['DAY_OF_WEEK'] = dataset['DAY_OF_WEEK'].replace('Monday', 'Segunda-feira')
dataset['DAY_OF_WEEK'] = dataset['DAY_OF_WEEK'].replace('Tuesday', 'Terca-feira')
dataset['DAY_OF_WEEK'] = dataset['DAY_OF_WEEK'].replace('Wednesday', 'Quarta-feira')
dataset['DAY_OF_WEEK'] = dataset['DAY_OF_WEEK'].replace('Thursday', 'Quinta-feira')
dataset['DAY_OF_WEEK'] = dataset['DAY_OF_WEEK'].replace('Friday', 'Sexta-feira')
dataset['DAY_OF_WEEK'] = dataset['DAY_OF_WEEK'].replace('Saturday', 'Sabado')
dataset['DAY_OF_WEEK'] = dataset['DAY_OF_WEEK'].replace('Sunday', 'Domingo')

dados = ['Agressao', 'Homicidio', 'Armas de Fogo', 'Assalto', 'Roubo', 'Violacao']
dataset = dataset[dataset['OFFENSE_CODE_GROUP'].isin(dados)]

#dataset['crime_ocorreu'] = [1 if ano > 2016 else 0 for ano in dataset['YEAR']]


def define_crime_ocorreu(row):
    ano = row['YEAR']
    mes = row['MONTH']

    if ano >= 2016 and mes >= 6:
        return 1
    elif ano >= 2016 and mes < 6:
        return 0
    elif ano < 2016 and mes >= 6:
        return 0
    else:
        return 1


# Aplicar a função para criar a coluna 'crime_ocorreu'
dataset['crime_ocorreu'] = dataset.apply(define_crime_ocorreu, axis=1)
df = dataset

#print(df['crime_ocorreu'].value_counts())
"""
# Explorar os dados
print(dataset.head())

# Verificar as informações do dataset
#print(dataset.info())
# Verificar a distribuição das classes
#print(dataset['crime_ocorreu'].value_counts())
"""
#Salvar dataset limpo
#Adicionar para o arquivo csv

"""
try:
    # Caminho para o arquivo CSV
    arquivo_csv = 'Dataset/crimes_limpo_v2.csv'
    df.to_csv(arquivo_csv, mode='a', header=True, index=False)
except:
  print("Erro ao criar dataset Limpo!")
"""


# Dividir os dados em features e target
X = df.drop(['crime_ocorreu', 'OCCURRED_ON_DATE', 'DAY_OF_WEEK', 'OFFENSE_CODE_GROUP', 'STREET'], axis=1)  # Substitua 'crime' pelo nome da coluna alvo
y = df['crime_ocorreu']

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


# Salvar o modelo treinado
#dump(ensemble, 'crime_radar_model_v2.joblib')
# Salvar o modelo em formato pkl para solucao mobile
#joblib.dump(ensemble, 'ensemble_model.pkl')
