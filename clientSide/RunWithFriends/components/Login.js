import React from 'react';
import { StyleSheet, View, Text, TextInput, Button } from 'react-native';
import {useState} from 'react';
import AppButton from './AppButton';

function Login({ navigation }) {
  const [email, checkEmail] = useState("");
  const [password, checkPassword] = useState("");
  return (
    <View style={styles.container}>
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Email"
          placeholderTextColor="gray"
        />
      </View>
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Password"
          placeholderTextColor="gray"
          secureTextEntry={true}
        />
      </View>
      <AppButton
        title="Log In!"
        // Need to change the path to this one//
        ///
        onPress={() => navigation.navigate("Dashboard")}
        ///
        //

        backgroundColor="#007bff"
      />
      <AppButton
        title="Create Account"
        onPress={() => navigation.navigate("SignUp")}
        backgroundColor="#007bff"
      />
    </View>
  );
}

const styles = StyleSheet.create({
    container:{
        flex: 1, 
        backgroundColor: '#2B60DE',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputView: {
        backgroundColor: "white",
        borderRadius: 30,
        width: "70%",
        height: 45,
        marginBottom: 20,
        alignItems: "center",
      },
      TextInput: {
        height: 50,
        flex: 1,
        padding: 10,
        marginLeft: 20,
      },
     

});

export default Login;