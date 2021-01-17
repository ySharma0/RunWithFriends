import React, { useEffect } from 'react';
import {  StyleSheet, View, Text, Button } from 'react-native';
import { Table, TableWrapper, Row, Rows, Col, Cols, Cell } from 'react-native-table-component';
import TabStack from './router';
import AppButton from './AppButton';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StackRouter } from 'react-navigation';
import Leaderboards from './Leaderboards';

const tableData = ["cHeads", "3 People"]
const Stack = createStackNavigator();

export default function Dashboard({ navigation }) {
    useEffect(() => {
        loggedIn = true;
    }, [])

    return (
        <View style={styles.mainView}>
            <AppButton
                title="Leaderboard!"
                onPress={() => navigation.navigate("Leaderboards")}
                backgroundColor="#007bff"
            />
            <Text> Current Challenges: </Text>
            <Table>
                <Row data={tableData} onPress={() => {navigation.navigate("ViewChallenge")}}/>
            </Table>
        </View>
    )
}


const styles = StyleSheet.create({
    mainView:{
        paddingTop: 35,
    }
})