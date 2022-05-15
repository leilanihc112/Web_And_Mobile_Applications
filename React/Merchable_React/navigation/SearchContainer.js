import * as React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';

//Screens
import SearchScreen from './screen/SearchScreen';
import ViewSingleStandScreen from './screen/ViewSingleStandScreen';

const Stack = createStackNavigator();

const SearchContainer = ({props, navigation}) => {
    return (
        <Stack.Navigator initialRouteName="Search">
            <Stack.Screen 
              name="Search" 
              component={SearchScreen} 
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

export default SearchContainer;