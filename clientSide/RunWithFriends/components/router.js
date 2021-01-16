import React from 'react';
import { View, Text } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';
import Login from './Login';
import SignUp from './SignUp';

const Stack = createStackNavigator();

export default function SignedOutStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen name="Login" component={Login} />
            <Stack.Screen name="SignUp" component={SignUp} /> 
        </Stack.Navigator>
    );
}