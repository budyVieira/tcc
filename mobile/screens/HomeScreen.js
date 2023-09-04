import { StyleSheet, Text , View, TouchableOpacity, Alert, Button } from 'react-native';
import React, { useState, useEffect } from 'react';
import axios from "axios";
import * as Notifications from 'expo-notifications';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});



export default function HomeScreen({ navigation }) {
  /*
  setInterval(async () => {
    await schedulePushNotification();
  }, 2000);*/

  const [data, setData] = useState("");
  const [output, setOutput] = useState([]);
/*
  useEffect(() => {
  }, []);
*/
  const predict = async () => {
    
    // Obtém os dados de entrada
    const offenseCodeGroup = "Assalto";
    const occurredOnDate = "2023-08-31 19:00:00";
    const year = 2023;
    const month = 8;
    const day = 13;
    const dayOfWeek = 1;
    const hour = 19;
    const minute = 55;
    const street = "Talatona";
    const latitude = -8.992603673547702;
    const longitude = 13.267653282652281;
    const provincia = "LUANDA";


    // Converte os dados em um objeto JSON
    const dataToSend = {
      offenseCodeGroup,
      occurredOnDate,
      year,
      month,
      day,
      dayOfWeek,
      hour,
      minute,
      street,
      provincia,
      latitude,
      longitude,
    };

    try{
      // Envia os dados para a API
      const response = await axios.post("http://192.168.100.103:8080/api/predict", dataToSend);

      // Obtém a resposta da API
      const prediction = response.data;
      //console.log(prediction)

      Alert.alert('Atenção', 'Se encontra em uma zona com uma probabilidade de crime de: ' + prediction["probabilidade"] + " %", [
        {text: 'OK', onPress: () => console.log('OK Pressed')},
      ]);
      await schedulePushNotification(prediction["probabilidade"]);
      
    } catch(err) {
      console.error(err)
    }

    
  }

  const handleDenunciaPress = () => {
    navigation.navigate('Form');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Previsão de Crimes</Text>
      {/** 
      <TouchableOpacity
        title="Ir para o formulário"
        onPress={handleDenunciaPress}
        style={styles.button}>
          <Text style={styles.buttonText}>Denunciar</Text>
      </TouchableOpacity>
      */}

        <TouchableOpacity
        onPress={predict}
        style={styles.button}>
          <Text style={styles.buttonText}>Prever</Text>
      </TouchableOpacity>

      {/**
      <Button
        title="Press to schedule a notification"
        onPress={async () => {
          await schedulePushNotification(data);
        }}
      />
      */}
    </View>
  );
}

async function schedulePushNotification(proba) {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "Atenção! 📬",
      body: 'Cuidado, neste momento está a se aproximar de uma zona perigosa com uma probabilidade de ocorrência de crime de ' + proba + " %",
      data: { data: 'goes here' },
    },
    trigger: { seconds: 1 },
  });
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 50,
    paddingHorizontal: 20,
  },
  button: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: 'red',
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 100,
    color: "red"
  },
});
