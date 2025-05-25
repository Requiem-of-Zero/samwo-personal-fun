// app/signin.tsx

import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  Dimensions,
  Image,
} from "react-native";
import { useRouter } from "expo-router";
import { useDispatch } from "react-redux";
import { login } from "../store/slices/authSlice";
import { SafeAreaView } from "react-native-safe-area-context";
import { LinearGradient } from "expo-linear-gradient";
import Animated, { FadeInDown, FadeInUp } from "react-native-reanimated";
import Spinner from "../components/Spinner";

const { width, height } = Dimensions.get("window");
const FULL_TITLE = "Family Ledger";

export default function SignIn() {
  const router = useRouter();
  const dispatch = useDispatch();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [displayedTitle, setDisplayedTitle] = useState("");

  // 1) Simulate initial splash
  useEffect(() => {
    const id = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(id);
  }, []);

  // 2) After splash AND after FadeInDown (600ms), start typewriter:
  useEffect(() => {
    if (!loading) {
      // wait for the fade-down animation to finish
      const fadeOut = setTimeout(() => {
        let i = 0;
        const typer = setInterval(() => {
          setDisplayedTitle(FULL_TITLE.slice(0, i + 1));
          i++;
          if (i >= FULL_TITLE.length) clearInterval(typer);
        }, 125);
        return () => clearInterval(typer);
      }, 600);

      return () => clearTimeout(fadeOut);
    }
  }, [loading]);

  if (loading) {
    return (
      <SafeAreaView className="flex-1 bg-background">
        <View className="flex-1 justify-center items-center">
          <Spinner />
          <Text className="text-textSecondary mt-4">Loading…</Text>
        </View>
      </SafeAreaView>
    );
  }

  const handleSignIn = async () => {
    setSubmitting(true);
    console.log({ email, password });
    const API = "http://127.0.0.1:8000";
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });
      console.log("Response status:", res.status);
      const text = await res.text();
      console.log("Response body:", text);

      let data;
      try {
        data = JSON.parse(text);
      } catch (error) {
        throw new Error("Invalid JSON from server");
      }
      if (!res.ok) {
        Alert.alert("Login failed", data.detail || "Unknown error");
        setSubmitting(false);
        return;
      }

      console.log("Logged in user:", data);
      dispatch(login(data));
      router.replace("/home");
    } catch (error) {
      const msg =
        error instanceof Error
          ? error.message // if it really is an erroror
          : typeof error === "string"
          ? error // maybe it’s a string
          : "Something went wrong";

      Alert.alert("Network error", msg);
      setSubmitting(false);
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-background">
      <LinearGradient colors={["#2E2E33", "#1F1F23"]} style={{ flex: 1 }}>
        {/* oversized, subtle logo behind */}
        <Image
          source={require("../assets/family-ledger-logo.png")}
          style={{
            position: "absolute",
            width: width * 1.4,
            height: width * 1.4,
            top: -height * 0.1,
            left: -width * 0.1,
          }}
          className="opacity-10"
          resizeMode="contain"
        />

        <View className="flex-1 justify-center items-center px-6">
          {/* Typewriter heading after fade */}
          <Animated.View entering={FadeInDown.duration(600)}>
            <Text className="text-4xl font-bold text-textPrimary mb-6">
              {displayedTitle}
            </Text>
          </Animated.View>

          {/* Sign-in form */}
          <Animated.View
            entering={FadeInUp.delay(300).duration(600)}
            className="w-full bg-background/80 rounded-2xl p-6 shadow-lg"
          >
            <TextInput
              value={email}
              onChangeText={setEmail}
              placeholder="Email"
              keyboardType="email-address"
              autoCapitalize="none"
              className="w-full bg-muted rounded-lg px-4 py-3 mb-4 text-textPrimary"
              placeholderTextColor="#666"
              editable={!submitting}
            />
            <TextInput
              value={password}
              onChangeText={setPassword}
              placeholder="Password"
              secureTextEntry
              className="w-full bg-muted rounded-lg px-4 py-3 mb-6 text-textPrimary"
              placeholderTextColor="#666"
              editable={!submitting}
            />
            <TouchableOpacity
              onPress={handleSignIn}
              disabled={submitting}
              className="w-full bg-primary rounded-lg py-4 items-center"
              activeOpacity={0.8}
            >
              <Text className="text-textPrimary font-semibold text-lg">
                {submitting ? "Signing In…" : "Sign In"}
              </Text>
            </TouchableOpacity>
            <View className="flex-row mt-4 justify-center">
              <Text className="text-textSecondary">
                Don’t have an account?{" "}
              </Text>
              <TouchableOpacity onPress={() => router.replace("/register")}>
                <Text className="text-accent font-semibold">Sign Up</Text>
              </TouchableOpacity>
            </View>
          </Animated.View>
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
}
