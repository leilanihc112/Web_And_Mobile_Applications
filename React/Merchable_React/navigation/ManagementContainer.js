import * as React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';

//Screens
import ManagementScreen from './screen/ManagementScreen';
import ViewSingleStandScreen from './screen/ViewSingleStandScreen';
import CreatePostScreen from './screen/CreatePostScreen';

const Stack = createStackNavigator();

const ManagementContainer = ({props, navigation}) => {
    return (
        <Stack.Navigator initialRouteName="Management">
            <Stack.Screen 
              name="Management" 
              component={ManagementScreen} 
              options={{
                  headerStyle: {
                    backgroundColor: '#59bfff',
                  },
                  headerTintColor: '#fff',
              }}
            />
            <Stack.Screen 
              name="View Single Stand" 
              component={ViewSingleStandScreen} 
              options={{
                  headerStyle: {
                    backgroundColor: '#59bfff',
                  },
                  headerTintColor: '#fff',
              }}
            />
            <Stack.Screen 
              name="Create Post" 
              component={CreatePostScreen} 
              options={{
                  headerStyle: {
                    backgroundColor: '#59bfff',
                  },
                  headerTintColor: '#fff',
              }}
            />
        </Stack.Navigator>
    )
}

const styles = StyleSheet.create({
    container:{
      flex:1, 
      justifyContent:'center',
      alignItems:'center',
      backgroundColor: '#212529'
    },
    text:{
      fontSize: 36,
      fontWeight: "bold",
      paddingBottom: 80,
      color: "#59bfff",
    }
  });

export default ManagementContainer;