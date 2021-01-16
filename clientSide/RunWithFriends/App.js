import { NavigationContainer } from '@react-navigation/native';
import React from 'react';
import SignedOutStack from './components/router';
// import { NavigationContainer } from '@react-navigation/native';

export default function App() {
  return (
    <NavigationContainer>
      <SignedOutStack />
    </NavigationContainer>
  );
}