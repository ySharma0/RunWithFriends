import React from 'react';
import { View, Text, Button } from 'react-native';

function Login( { navigation }) {
    return (
        <View>
            <Text>Hello from Login!</Text>
            <Button onPress={() => navigation.navigate("SignUp")}>Go To SignUp</Button>
        </View>
    );
}

export default Login;