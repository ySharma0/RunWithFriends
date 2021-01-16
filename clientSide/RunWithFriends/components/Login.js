import React from 'react';
import { View, Text, Button } from 'react-native';

function Login( { navigation }) {
    return (
        <View>
            <Text>Hello from Login!</Text>
            <Button title= 'Go To Sign Up' onPress={() => navigation.navigate("SignUp")}></Button>
        </View>
    );
}

export default Login;