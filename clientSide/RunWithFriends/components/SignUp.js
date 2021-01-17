import React from 'react';
import { StyleSheet, View, Text, TextInput, Button } from 'react-native';
// import { TextInput } from 'react-native-gesture-handler';
import AppButton from './AppButton';

function SignUp({ navigation }) {
  return (
    <View style={styles.container}>
        <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Enter Email"
          placeholderTextColor="gray"
          secureTextEntry={true}
        />
      </View>
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Enter Password"
          placeholderTextColor="gray"
          secureTextEntry={true}
        />
      </View>
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder=" Re-Enter Password"
          placeholderTextColor="gray"
          secureTextEntry={true}
        />
      </View>
      <AppButton
        title="SiGN UP!"
        onPress={() => navigation.navigate("MoreInfo")}
        backgroundColor="#007bff"
      />



    </View>
  );
};


const styles = StyleSheet.create({
    container:{
        flex: 1, 
        backgroundColor: '#2B60DE',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputView: {
        backgroundColor: 'white',
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


export default SignUp;