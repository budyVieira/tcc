import React from 'react'
import Background from '../components/Background'
import Logo from '../components/Logo'
import Header from '../components/Header'
import Paragraph from '../components/Paragraph'
import Button from '../components/Button'

export default function Dashboard({ navigation }) {
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