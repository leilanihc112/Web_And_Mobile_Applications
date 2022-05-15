import React, {useRef, useEffect, useState} from 'react';
import { View, Text, Image, ScrollView, TextInput, Button, ActivityIndicator, FlatList, SafeAreaView, LogBox, SectionList, Animated, PanResponder, StyleSheet, useWindowDimensions, ImageBackground } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

const FadeInView = (props) => {
  const fadeAnim = useRef(new Animated.Value(0)).current  // Initial value for opacity: 0

  useEffect(() => {
    Animated.timing(
      fadeAnim,
      {
        toValue: 1,
        duration: 1000,
		useNativeDriver: true
      }
    ).start();
  }, [fadeAnim])
  
  return (
    <Animated.View                 // Special animatable View
      style={{
        ...props.style,
        opacity: fadeAnim,         // Bind opacity to animated value
      }}
    >
      {props.children}
    </Animated.View>
  );
}

const CatApp = (props) => {
const [isHungry, setIsHungry] = useState(true);
  return (
    <View>
      <Image
        source={{uri: "https://reactnative.dev/docs/assets/p_cat1.png"}}
        style={{width: 200, height: 200}}
      />
      <Text>
        I am {props.name ? props.name : "your cat"}, and I am {isHungry ? "hungry" : "full"}!
      </Text>
      <Button
        onPress={() => {
          setIsHungry(false);
		  alert('Thank you!');
        }}
        disabled={!isHungry}
        title={isHungry ? "Pour me some milk, please!" : "Thank you!"}
      />
    </View>
  );
}

const HomeScreen = ({navigation}) => {
	const [text, setText] = useState('');
	const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  const getMovies = async () => {
     try {
      const response = await fetch('https://reactnative.dev/movies.json');
      const json = await response.json();
      setData(json.movies);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }
  
  const pan = useRef(new Animated.ValueXY()).current;
  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: () => true,
      onPanResponderMove: Animated.event([
        null,
        { dx: pan.x, dy: pan.y }
      ], {useNativeDriver: false}),
      onPanResponderRelease: () => {
        Animated.spring(pan, { toValue: { x: 0, y: 0 }, useNativeDriver: false }).start();
      }
    })
  ).current;


  useEffect(() => {
    getMovies();
  }, []);
  
  useEffect(() => {
    LogBox.ignoreLogs(['VirtualizedLists should never be nested']);
}, [])

	return (
		<ScrollView>
	  <Text>Cat Name:</Text>
      <TextInput
        style={{
          height: 40,
          borderColor: 'gray',
          borderWidth: 1
        }}
        placeholder="Name"
		onChangeText={newText => setText(newText)}
        defaultValue={text}
      />
      <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
		<FadeInView>
			<CatApp name={text}></CatApp>
		</FadeInView>
      </View>
	  <View style={{ flex: 1, padding: 24 }}>
      {isLoading ? <ActivityIndicator/> : (
        <FlatList
          data={data}
          keyExtractor={({ id }, index) => id}
          renderItem={({ item }) => (
            <Text>{item.title}, {item.releaseYear}</Text>
          )}
        />
      )}
      </View>
	  <Button
      title="View some images"
      onPress={() =>
        navigation.navigate('Images')
      }
      />
	  <Button
      title="Drag a square"
      onPress={() =>
        navigation.navigate('Square')
      }
      />
	  <Button
      title="View a List"
      onPress={() =>
        navigation.navigate('SectionList')
      }
      />
	  </ScrollView>
	);
};

const SectionListScreen  = ({ navigation, route }) => {
	const styles = StyleSheet.create({
	  container: {
	   flex: 1,
	   paddingTop: 22
	  },
	  sectionHeader: {
		paddingTop: 2,
		paddingLeft: 10,
		paddingRight: 10,
		paddingBottom: 2,
		fontSize: 14,
		fontWeight: 'bold',
		backgroundColor: 'rgba(247,247,247,1.0)',
	  },
	  item: {
		padding: 10,
		fontSize: 18,
		height: 44,
	  },
	});
	return (
		  <View style={styles.container}>
			<SectionList
			  sections={[
				{title: 'D', data: ['Devin', 'Dan', 'Dominic']},
				{title: 'J', data: ['Jackson', 'James', 'Jillian', 'Jimmy', 'Joel', 'John', 'Julie']},
				{title: 'L', data: ['Luke', 'Layla', 'Lynn', 'Lydia', 'Lionel', 'Levi']},
			  ]}
			  renderItem={({item}) => <Text style={styles.item}>{item}</Text>}
			  renderSectionHeader={({section}) => <Text style={styles.sectionHeader}>{section.title}</Text>}
			  keyExtractor={(item, index) => index}
			/>
		  </View>
		);
};

const SquareScreen = ({ navigation, route }) => {
	const pan = useRef(new Animated.ValueXY()).current;
  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: () => true,
      onPanResponderMove: Animated.event([
        null,
        { dx: pan.x, dy: pan.y }
      ], {useNativeDriver: false}),
      onPanResponderRelease: () => {
        Animated.spring(pan, { toValue: { x: 0, y: 0 }, useNativeDriver: false}).start();
      }
    })
  ).current;
  
  const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center"
  },
  titleText: {
    fontSize: 14,
    lineHeight: 24,
    fontWeight: "bold"
  },
  box: {
    height: 150,
    width: 150,
    backgroundColor: "blue",
    borderRadius: 5
  }
});

  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Drag & Release this box!</Text>
      <Animated.View
        style={{
          transform: [{ translateX: pan.x }, { translateY: pan.y }]
        }}
        {...panResponder.panHandlers}
      >
        <View style={styles.box} />
      </Animated.View>
    </View>
  );
};

const ImagesScreen = ({ navigation, route }) => {
  const images = new Array(6).fill('https://images.unsplash.com/photo-1556740749-887f6717d7e4');
	
  const scrollX = useRef(new Animated.Value(0)).current;

  const { width: windowWidth } = useWindowDimensions();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.scrollContainer}>
        <ScrollView
          horizontal={true}
          pagingEnabled
          showsHorizontalScrollIndicator={false}
          onScroll={Animated.event([
            {
              nativeEvent: {
                contentOffset: {
                  x: scrollX
                }
              }
            }
          ], {useNativeDriver: false})}
          scrollEventThrottle={1}
        >
          {images.map((image, imageIndex) => {
            return (
              <View
                style={{ width: windowWidth, height: 250 }}
                key={imageIndex}
              >
                <ImageBackground source={{ uri: image }} style={styles.card}>
                  <View style={styles.textContainer}>
                    <Text style={styles.infoText}>
                      {"Image - " + imageIndex}
                    </Text>
                  </View>
                </ImageBackground>
              </View>
            );
          })}
        </ScrollView>
        <View style={styles.indicatorContainer}>
          {images.map((image, imageIndex) => {
            const width = scrollX.interpolate({
              inputRange: [
                windowWidth * (imageIndex - 1),
                windowWidth * imageIndex,
                windowWidth * (imageIndex + 1)
              ],
              outputRange: [8, 16, 8],
              extrapolate: "clamp"
            });
            return (
              <Animated.View
                key={imageIndex}
                style={[styles.normalDot, { width }]}
              />
            );
          })}
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center"
  },
  scrollContainer: {
    height: 300,
    alignItems: "center",
    justifyContent: "center"
  },
  card: {
    flex: 1,
    marginVertical: 4,
    marginHorizontal: 16,
    borderRadius: 5,
    overflow: "hidden",
    alignItems: "center",
    justifyContent: "center"
  },
  textContainer: {
    backgroundColor: "rgba(0,0,0, 0.7)",
    paddingHorizontal: 24,
    paddingVertical: 8,
    borderRadius: 5
  },
  infoText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold"
  },
  normalDot: {
    height: 8,
    width: 8,
    borderRadius: 4,
    backgroundColor: "silver",
    marginHorizontal: 4
  },
  indicatorContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center"
  }
});

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Welcome' }}
        />
        <Stack.Screen name="Images" component={ImagesScreen} />
		<Stack.Screen name="Square" component={SquareScreen} />
		<Stack.Screen name="SectionList" component={SectionListScreen}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;