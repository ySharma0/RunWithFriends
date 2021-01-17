import React from 'react';
import { View, Text } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Login from './Login';
import SignUp from './SignUp';
import Dashboard from './Dashboard';
import Profile from './Profile';
import { NavigationContainer } from '@react-navigation/native';
import FindFriends from './FindFriends';
import Leaderboards from './Leaderboards';

const Stack = createStackNavigator();

export default function MainStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen name="Login" component={Login} />
            <Stack.Screen name="SignUp" component={SignUp} /> 
            <Stack.Screen name="Dashboard" component={Dashboard} />
            <Stack.Screen name="Leaderboards" component={Leaderboards} />

        </Stack.Navigator>
    );
}

const Tab = createBottomTabNavigator();

export function TabStack() {
    return (
        <Tab.Navigator>
            <Tab.Screen name="Profile" component={Profile} />
            <Tab.Screen name="Dashboard" component={Dashboard} />
            <Tab.Screen name="FindFriends" component={FindFriends} />
        </Tab.Navigator>
    );
}