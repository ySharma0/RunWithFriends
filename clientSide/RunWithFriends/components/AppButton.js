import React from 'react';
import {
    Button, 
    StyleSheet, 
    TouchableOpacity,  
    Text, 
    View
} from 'react-native';


const AppButton = ({ onPress, title }) => {
  return (
    <TouchableOpacity onPress={onPress} style={styles.appButtonContainer}>
      <Text style={styles.appButtonText}>{title}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  // ...
  appButtonContainer: {
    elevation: 8,
    backgroundColor: "#009688",
    borderRadius: 100,
    paddingVertical: 10,
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  appButtonText: {
    fontSize:15,
    color: "#fff",
    fontWeight: "bold",
    alignSelf: "center",
    textTransform: "uppercase",
  },
});

  export default AppButton;