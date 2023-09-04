import schedule
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import os
from joblib import dump


# Defina a função de treinamento.
def train_model():
  # Carregue os dados de treinamento.
  df = pd.read_csv('Dataset/crime_dataset_clean.csv', encoding='latin-1')
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
  ensemble = VotingClassifier(
    estimators=[('KNN', knn), ('Decision Tree', decision_tree), ('Random Forest', random_forest),
                ('Naive Bayes', naive_bayes)], voting='hard')

  # Treinar o ensemble
  ensemble.fit(X_train, y_train)

  # Excluir o modelo anterior, se existir
  if os.path.exists('../PTC_Back/modelo/modelo_init.joblib'):
    os.remove('../PTC_Back/modelo/modelo_init.joblib')

  # Salvar o novo modelo reentendido
  dump(ensemble, '../PTC_Back/modelo/modelo_init.joblib')


# Defina a programação para treinar o modelo a cada 7 horas.
schedule.every(7).hours.do(train_model)

# Execute a programação.
while True:
  schedule.run_pending()
  time.sleep(1)
