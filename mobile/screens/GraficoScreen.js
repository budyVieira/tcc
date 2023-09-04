import React, { useState, useEffect } from 'react';
import axios from "axios";
// import all the components we are going to use
import {
  SafeAreaView,
  Text,
  View,
  StyleSheet,
  Dimensions,
  ScrollView,
} from 'react-native';

//import React Native chart Kit for different kind of Chart
import {
  BarChart,
} from 'react-native-chart-kit';
import BackButton from '../components/BackButton'
import Background from '../components/Background'

export default function GraficoScreen ({ navigation }) {

  const [status, setStatus] = useState('loading');
  const [data, setData] = useState([]);
  const [label, setLabel] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData  = async () => {
    try{
      // Envia os dados para a API
      const response = await axios.post("http://192.168.100.103:8080/api/graph");

      // Obtém a resposta da API
      const graphData = await response.data;

      setStatus('success');
      setData(graphData["dados"]["data"]);
      setLabel(graphData["dados"]["labels"]);
      
      console.log(graphData["dados"]["data"]);
      console.log(graphData["dados"]["labels"]);
      
    } catch(err) {
      console.error(err)
    }

  }
  return (
      <ScrollView>
        <Background>
        {status === 'loading' ? (
        <Text>Carregando...</Text>
        ) : (
          <View>
          <BackButton goBack={navigation.goBack} />
          <Text style={styles.header}>Bar Chart</Text>
          <BarChart
            data={{
              labels: label,
              datasets: [
                {
                  data: data,
                },
              ],
            }}
            width={Dimensions.get('window').width - 25}
            height={300}
            yAxisLabel={''}
            chartConfig={{
              backgroundColor: '#1cc910',
              backgroundGradientFrom: '#eff3ff',
              backgroundGradientTo: '#efefef',
              decimalPlaces: 1,
              color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
              style: {
                borderRadius: 16,
              },
            }}
            style={{
              marginVertical: 8,
              borderRadius: 0,
            }}
          />
          </View>
          )}
          </Background>
      </ScrollView>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
    padding: 10,
  },
  header: {
    textAlign: 'center',
    fontSize: 18,
    padding: 16,
    marginTop: 16,
  },
});
