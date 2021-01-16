import React from 'react';
import { View, Text, Button } from 'react-native';
import AppButton from './AppButton';

function Login( { navigation }) {
    return (
        <View>
            <Text>Hello from Login!</Text>
            <AppButton title="SIGN UP!" onPress={() => navigation.navigate("SignUp")}  backgroundColor="#007bff" />        
            </View>
    );
}

export default Login;