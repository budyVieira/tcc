import React, { useState, useEffect } from 'react';
import { View, Text, Alert, Platform, StyleSheet, ScrollView, KeyboardAvoidingView  } from 'react-native';
import * as Location from 'expo-location';
import TextInput from '../components/TextInput';
import axios from "axios";
import DatePicker from '@react-native-community/datetimepicker';
import TimePicker from '@react-native-community/datetimepicker';
import Button from '../components/Button';
import BackButton from '../components/BackButton'
import {Picker} from '@react-native-picker/picker';

export default function FormScreen({ navigation }) {

  const [modelLoaded, setModelLoaded] = useState(false);
  const [selectedValue, setSelectedValue] = useState('');

  const items = [
    { label: 'Distrito/Provincia', value: '' },
    { label: 'Luanda', value: 'LUANDA' },
    { label: 'Bayview', value: 'BAYVIEW' },
    { label: 'Central', value: 'CENTRAL' },
    { label: 'Ingleside', value: 'INGLESIDE' },
    { label: 'Mission', value: 'MISSION' },
    { label: 'Northern', value: 'NORTHERN' },
    { label: 'Park', value: 'PARK' },
    { label: 'Richmond', value: 'RICHMOND' },
    { label: 'Southern', value: 'SOUTHERN' },
    { label: 'Taraval', value: 'TARAVAL' },
    { label: 'Tenderloin', value: 'TENDERLOIN' },
  ];


  const [location, setLocation] = useState({ value: '', error: '' });
  const [latitude, setLatitude] = useState({ value: '', error: '' });
  const [longitude, setLongitude] = useState({ value: '', error: '' });
  const [tipoCrime, setTipoCrime] = useState({ value: '', error: '' });
  const [data, setData] = useState('');
  const [descricao, setDescricao] = useState({ value: '', error: '' });
  const [local, setLocal] = useState({ value: '', error: '' });

  // Funções de manipulação dos campos
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedTime, setSelectedTime] = useState(new Date());

  const handleDateChange = (event, date) => {
    if (date) {
      setSelectedDate(date);
    }
  };

  const handleTimeChange = (event, time) => {
    if (time) {
      setSelectedTime(time);
    }
  };


  const getLocation = async () => {
    let { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permissão de localização negada');
      return;
    }

    let location = await Location.getCurrentPositionAsync({});
    setLocation({ value: location, error: '' });
    setLatitude({ value: location.coords.latitude.toString(), error: '' });
    setLongitude({ value: location.coords.longitude.toString(), error: '' });
  };



  const handleEnviar = async () => {
    // Aqui você pode enviar os dados do formulário para o backend
    // e tratar a lógica de atualização do dataset e treinamento do modelo

    // Exemplo de exibição dos dados no console
    const year = selectedDate.getFullYear();
    const month = selectedDate.getMonth() + 1;
    const day = selectedDate.getDate();
    const hour = selectedTime.getHours();
    const minute = selectedTime.getMinutes();
    const categoria = tipoCrime.value;
    const desc = descricao.value;
    const lat = latitude.value;
    const long = longitude.value;
    const endereco = local.value;
    const distrito = selectedValue;
    let data = `${year}-${(month < 10 ? '0' : '') + month}-${(day < 10 ? '0' : '') + day} ${(hour < 10 ? '0' : '') + hour}:${(minute < 10 ? '0' : '') + minute}`;

    let diaSemana = selectedDate.getDay() - 1;
    if (diaSemana < 0) diaSemana = 6;

    try {
      const formData = {
        data,
        lat,
        long,
        categoria,
        diaSemana,
        year,
        month,
        day,
        hour,
        minute,
        desc,
        distrito,
        endereco
      };
      //console.log(formData)
      
        // Envia os dados para a API
        const response = await axios.post("http://192.168.100.103:8080/api/denuncia", formData);
        const msg = response.data;
      
        Alert.alert(msg['resposta']);
      
    } catch (err) {
      Alert.alert('Erro ao enviar a denúncia. Por favor, tente novamente mais tarde.');
      console.error(err)
    }
    
  };


  const handleVoltar = () => {
    navigation.goBack();
  };

  return (
    <>
    <View style={{paddingTop: '20%', marginBottom: "3%", paddingLeft: '5%'}}>
      <BackButton goBack={navigation.goBack} />
    </View>
    <ScrollView style={styles.container}>
    <KeyboardAvoidingView keyboardVerticalOffset={700}>
      <Button
        mode="outlined"
        onPress={getLocation}
      >
        Usar GPS
      </Button>
      
      <TextInput
        label="Latitude"
        returnKeyType="next"
        value={latitude.value}
        onChangeText={(text) => setLatitude({ value: text, error: '' })}
        error={!!latitude.error}
        errorText={latitude.error}
      />

      <TextInput
        label="Longitude"
        returnKeyType="next"
        value={longitude.value}
        onChangeText={(text) => setLongitude({ value: text, error: '' })}
        error={!!longitude.error}
        errorText={longitude.error}
      />

      <TextInput
        label="Tipo de Crime"
        returnKeyType="next"
        value={tipoCrime.value}
        onChangeText={(text) => setTipoCrime({ value: text, error: '' })}
        error={!!tipoCrime.error}
        errorText={tipoCrime.error}
      />

      {Platform.OS === 'ios' ? (
        <View>
          <Text>Data:</Text>
          <DatePicker
            value={selectedDate}
            mode="date"
            display="default"
            onChange={handleDateChange}
          />
        </View>
      ) : (
        <View>
          <Text>Data:</Text>
          <Button title="Seleccionar data" onPress={() => {}} />
        </View>
      )}

      {/* Time Picker */}
      {Platform.OS === 'ios' ? (
        <View>
          <Text>Hora:</Text>
          <TimePicker
            value={selectedTime}
            mode="time"
            display="default"
            onChange={handleTimeChange}
          />
        </View>
      ) : (
        <View>
          <Text>Hora:</Text>
          <Button title="Seleciona o Horario" onPress={() => {}} />
        </View>
      )}

      <TextInput
        label="Descrição"
        returnKeyType="next"
        value={descricao.value}
        onChangeText={(text) => setDescricao({ value: text, error: '' })}
        error={!!descricao.error}
        errorText={descricao.error}
      />

    <Picker
      selectedValue={selectedValue}
      onValueChange={setSelectedValue}
    >
      {items.map((item, index) => (
        <Picker.Item key={index} label={item.label} value={item.value} />
      ))}
    </Picker>
      
      <TextInput
        label="Endereço"
        returnKeyType="next"
        value={local.value}
        onChangeText={(text) => setLocal({ value: text, error: '' })}
        error={!!local.error}
        errorText={local.error}
      />
      </KeyboardAvoidingView>
      <Button
        mode="outlined"
        onPress={handleEnviar}
      >
        Enviar
      </Button>
    </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 5,
    marginBottom: '5%'
  },
  label: {
    fontSize: 10,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 16,
    paddingHorizontal: 8,
  },
});