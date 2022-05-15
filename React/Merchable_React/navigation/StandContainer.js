import * as React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';

//Screens
import ViewStandsScreen from './screen/ViewStandsScreen';
import ViewSingleStandScreen from './screen/ViewSingleStandScreen';
import CreatePostScreen from './screen/CreatePostScreen';

const Stack = createStackNavigator();

const StandContainer = ({props, navigation}) => {
    return (
        <Stack.Navigator initialRouteName="View Stands">
            <Stack.Screen 
              name="View Stands" 
              component={ViewStandsScreen} 
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

export default StandContainer;