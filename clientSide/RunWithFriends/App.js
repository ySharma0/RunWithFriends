import { NavigationContainer } from '@react-navigation/native';
import React from 'react';
import MainStack, { TabStack } from './components/router';
import './components/global';

export default function App() {
  return (
    <NavigationContainer>
      { loggedIn ? (
        <MainStack />
      ) : (
        <TabStack />
      )
    }
    </NavigationContainer>
  );
}

