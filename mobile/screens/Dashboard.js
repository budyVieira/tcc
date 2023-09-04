import Background from '../components/Background'
import Logo from '../components/Logo'
import Header from '../components/Header'
import Paragraph from '../components/Paragraph'
import Button from '../components/Button'
import React, { useState, useEffect } from 'react';
import axios from "axios";
//import * as BackgroundFetch from 'expo-background-fetch';
//import * as TaskManager from 'expo-task-manager'
import * as Notifications from 'expo-notifications';
import * as Location from 'expo-location';
//const BACKGROUND_FETCH_TASK = 'background-fetch';


Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});


export default function Dashboard({ navigation }) {
  //const [status, setStatus] = React.useState(null);
  //const [isRegistered, setIsRegistered] = useState(false);
  const [location, setLocation] = useState({ value: '', error: '' });

  useEffect(() => {
    setInterval(() => {
      predict();
    },  15 * 60 * 1000);
  }, []);

const getLocation = async () => {
  let { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') {
    Alert.alert('Permissão de localização negada');
    return;
  }

  let location = await Location.getCurrentPositionAsync({});
  setLocation({ value: location, error: '' });
  const lat = location.coords.latitude;
  const long = location.coords.longitude;
  return {latidude : lat, longitude: long}
};

function add300Meters(latitude, longitude) {
  // Converte a latitude e a longitude para radianos
  const latitudeRadians = latitude * Math.PI / 180;
  const longitudeRadians = longitude * Math.PI / 180;

  // Calcula a distância em metros para cada direção
  const northDistance = 300 * Math.cos(latitudeRadians);
  const southDistance = 300 * Math.cos(latitudeRadians);
  const eastDistance = 300 * Math.sin(latitudeRadians);
  const westDistance = 300 * Math.sin(latitudeRadians);

  // Calcula as novas coordenadas
  const northCoordinate = latitude + northDistance / 6371;
  const southCoordinate = latitude - southDistance / 6371;
  const eastCoordinate = longitude + eastDistance / 6371;
  const westCoordinate = longitude - westDistance / 6371;

  // Retorna um objeto com as novas coordenadas
  return {
    north: {
      latitude: northCoordinate,
      longitude: longitude,
    },
    south: {
      latitude: southCoordinate,
      longitude: longitude,
    },
    east: {
      latitude: latitude,
      longitude: eastCoordinate,
    },
    west: {
      latitude: latitude,
      longitude: westCoordinate,
    },
  };
}

const predict = async () => {
  const loc = await getLocation();

  const now = new Date();

  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();
  let diaSemana = now.getDay() - 1;
  if (diaSemana < 0) diaSemana = 6;
  const hour = now.getHours();
  const minute = now.getMinutes();

  // Obtém os dados de entrada
  const results = add300Meters(loc.latidude, loc.longitude);
  const provincia = "LUANDA";

  let lat = results.north.latitude;
  let long = results.north.latitude;
  // Converte os dados em um objeto JSON
  const dataToSendN = {
    year,
    month,
    day,
    diaSemana,
    hour,
    minute,
    provincia,
    lat,
    long,
  };
  lat = results.south.latitude;
  long = results.south.latitude;
  const dataToSendS = {
    year,
    month,
    day,
    diaSemana,
    hour,
    minute,
    provincia,
    lat,
    long,
  };
  lat = results.east.latitude;
  long = results.east.latitude;
  const dataToSendE = {
    year,
    month,
    day,
    diaSemana,
    hour,
    minute,
    provincia,
    lat,
    long,
  };
  lat = results.west.latitude;
  long = results.west.latitude;
  const dataToSendW = {
    year,
    month,
    day,
    diaSemana,
    hour,
    minute,
    provincia,
    lat,
    long,
  };


  try{
    // Envia os dados para a API
    const responseN = await axios.post("http://192.168.100.103:8080/api/predict", dataToSendN);
    const responseS = await axios.post("http://192.168.100.103:8080/api/predict", dataToSendS);
    const responseE = await axios.post("http://192.168.100.103:8080/api/predict", dataToSendE);
    const responseW = await axios.post("http://192.168.100.103:8080/api/predict", dataToSendW);

    // Obtém a resposta da API
    const predictionN = responseN.data;
    const predictionS = responseS.data;
    const predictionE = responseE.data;
    const predictionW = responseW.data;

    if (predictionN["probabilidade"] >= 50)
      await schedulePushNotification("Norte", predictionN["probabilidade"]);
    else if (predictionS["probabilidade"] >= 50)
      await schedulePushNotification("Sul", predictionS["probabilidade"]);
    else if (predictionE["probabilidade"] >= 50)
      await schedulePushNotification("Este", predictionE["probabilidade"]);
    else if (predictionW["probabilidade"] >= 50)
      await schedulePushNotification("Oeste", predictionW["probabilidade"]);
    
  } catch(err) {
    console.error(err)
  }

}
  return (
    <Background>
      <Logo />
      <Header>Bem vindo 💫</Header>
      <Paragraph>
        Parabéns, você está logado.
      </Paragraph>
      <Button
        mode="outlined"
        onPress={() => navigation.navigate('FormScreen')}
      >
        Fazer Denúncia
      </Button>
      <Button
        mode="outlined"
        onPress={() => navigation.navigate('HomeScreen')}
      >
        Denúncias Realizadas
      </Button>
      <Button
        mode="outlined"
        onPress={() => navigation.navigate('GraficoScreen')}
      >
        Áreas para Evitar
      </Button>
      <Button
        mode="outlined"
        onPress={() =>
          navigation.reset({
            index: 0,
            routes: [{ name: 'StartScreen' }],
          })
        }
      >
        Sair
      </Button>
    </Background>
  )
}

async function schedulePushNotification(direcao, proba) {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "Atenção! 📬",
      body: 'Cuidado, neste momento está a se aproximar de uma zona perigosa. Daqui a 300 metros na direção ' + direcao + ' existe uma probabilidade de ocorrência de crime de ' + proba + " %",
      data: { data: 'goes here' },
    },
    trigger: { seconds: 1 },
  });
}


/*

TaskManager.defineTask(BACKGROUND_FETCH_TASK, async () => {
  
  return BackgroundFetch.BackgroundFetchResult.NewData;
});

async function registerBackgroundFetchAsync() {
  return BackgroundFetch.registerTaskAsync(BACKGROUND_FETCH_TASK, {
    minimumInterval: 5, // 15 minutes
    stopOnTerminate: false, // android only,
    startOnBoot: true, // android only
  });
}

  const checkStatusAsync = async () => {
    const status = await BackgroundFetch.getStatusAsync();
    const isRegistered = await TaskManager.isTaskRegisteredAsync(BACKGROUND_FETCH_TASK);
    setStatus(status);
    setIsRegistered(isRegistered);
  };

  const toggleFetchTask = async () => {
    if (isRegistered) {
      await unregisterBackgroundFetchAsync();
    } else {
      await registerBackgroundFetchAsync();
    }

    checkStatusAsync();
  };
*/