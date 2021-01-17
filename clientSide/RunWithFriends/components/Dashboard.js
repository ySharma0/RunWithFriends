import React, { useEffect } from 'react';
import { View, Text, Button } from 'react-native';
import TabStack from './router';

export default function Dashboard({ navigation }) {
    useEffect(() => {
        loggedIn = true;
    }, [])

    return (
        <View>
            <Text>dashboard!</Text>
        </View>
    )
}
