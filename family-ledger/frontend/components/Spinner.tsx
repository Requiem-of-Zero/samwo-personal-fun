// components/Spinner.jsx
import React, { useEffect, useRef } from "react";
import { Animated, Easing, View, StyleSheet } from "react-native";

export default function Spinner({
  size = 100, // diameter of the spinner
  duration = 1000, // one full rotation in ms
}) {
  const spin = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.timing(spin, {
        toValue: 1,
        duration,
        easing: Easing.linear,
        useNativeDriver: true,
      })
    ).start();
  }, [spin, duration]);

  const rotation = spin.interpolate({
    inputRange: [0, 1],
    outputRange: ["0deg", "360deg"],
  });

  return (
    <View
      style={[
        styles.clip,
        { width: size, height: size, borderRadius: size / 2 },
      ]}
    >
      <Animated.Image
        source={require("../assets/images/coin.png")} // now a circle asset
        style={{
          width: size,
          height: size,
          transform: [{ rotate: rotation }],
          backgroundColor: "transparent",
        }}
        resizeMode="contain"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  clip: {
    overflow: "hidden", // ← this actually masks off the square pixels
    backgroundColor: "transparent",
  },
});
