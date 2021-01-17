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
        <TextInput style={styles.TextInput} 
        placeholder='Email'
        placeholderTextColor='gray'
        />
      </View>
      <View style={styles.inputView}>
        <TextInput style={styles.TextInput} 
        placeholder='Password'
        placeholderTextColor='gray'
        secureTextEntry={true}
        />
      </View>
      <AppButton
        title="Log In!"
        onPress={() => navigation.navigate("Log In")}
        backgroundColor="#007bff"
      />
        <AppButton
        title="SIGN UP!"
        onPress={() => navigation.navigate("SignUp")}
        backgroundColor="#007bff"
      />
    </View>
  );
}

const styles = StyleSheet.create({
    container:{
        flex: 1, 
        backgroundColor: 'white',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputView: {
        backgroundColor: "gold",
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

