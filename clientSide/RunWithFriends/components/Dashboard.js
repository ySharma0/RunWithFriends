import React, { useEffect } from 'react';
import { View, Text, Button } from 'react-native';
import TabStack from './router';
import AppButton from './AppButton';

export default function Dashboard({ navigation }) {
    useEffect(() => {
        loggedIn = true;
    }, [])

    return (
        <View>
            <Text>dashboard!</Text>
            <AppButton
                title="Leaderboard!"
                onPress={() => navigation.navigate("Leaderboards")}
                backgroundColor="#007bff"
            />
        </View>
    )
}
