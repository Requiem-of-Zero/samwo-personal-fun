// app/register.tsx
import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  Dimensions,
  Image,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { LinearGradient } from "expo-linear-gradient";
import Animated, { FadeInDown, FadeInUp } from "react-native-reanimated";
import Spinner from "../components/Spinner"; // your custom spinner
import { useDispatch } from "react-redux";
import { register } from "../store/slices/authSlice";

const { width, height } = Dimensions.get("window");
const FULL_TITLE = "Create Account";

export default function Register() {
  const router = useRouter();
  const dispatch = useDispatch();

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  // initial splash spinner
  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(t);
  }, []);

  // form submit
  const handleRegister = async () => {
    if (!fullName || !email || !password) {
      return Alert.alert("Missing fields", "All fields are required.");
    }
    if (password !== confirm) {
      return Alert.alert("Password mismatch", "Passwords must match.");
    }
    const API = "http://127.0.0.1:8000";
    setSubmitting(true);
    try {
      const res = await fetch(`${API}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ full_name: fullName, email, password }),
      });
      const data = await res.json();

      if (!res.ok) {
        return Alert.alert(
          "Registration Failed",
          data.detail || "Unknown error"
        );
      }

      dispatch(register(data)); // if you want to auto-login
      Alert.alert("Welcome!", "Your account has been created.", [
        { text: "OK", onPress: () => router.replace("/signin") },
      ]);
    } catch (err: any) {
      Alert.alert("Network Error", err.message || "Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

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

  return (
    <SafeAreaView className="flex-1 bg-background">
      <LinearGradient colors={["#2E2E33", "#1F1F23"]} style={{ flex: 1 }}>
        {/* giant, faded logo in the background */}
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
          {/* Title */}
          <Animated.View entering={FadeInDown.duration(600)}>
            <Text className="text-4xl font-bold text-textPrimary mb-6">
              {FULL_TITLE}
            </Text>
          </Animated.View>

          {/* Form */}
          <Animated.View
            entering={FadeInUp.delay(300).duration(600)}
            className="w-full bg-background/80 rounded-2xl p-6 shadow-lg"
          >
            <TextInput
              value={fullName}
              onChangeText={setFullName}
              placeholder="Full Name"
              placeholderTextColor="#666"
              editable={!submitting}
              className="w-full bg-muted rounded-lg px-4 py-3 mb-4 text-textPrimary"
            />

            <TextInput
              value={email}
              onChangeText={setEmail}
              placeholder="Email"
              keyboardType="email-address"
              autoCapitalize="none"
              placeholderTextColor="#666"
              editable={!submitting}
              className="w-full bg-muted rounded-lg px-4 py-3 mb-4 text-textPrimary"
            />

            <TextInput
              value={password}
              onChangeText={setPassword}
              placeholder="Password"
              secureTextEntry
              placeholderTextColor="#666"
              editable={!submitting}
              className="w-full bg-muted rounded-lg px-4 py-3 mb-4 text-textPrimary"
            />

            <TextInput
              value={confirm}
              onChangeText={setConfirm}
              placeholder="Confirm Password"
              secureTextEntry
              placeholderTextColor="#666"
              editable={!submitting}
              className="w-full bg-muted rounded-lg px-4 py-3 mb-6 text-textPrimary"
            />

            <TouchableOpacity
              onPress={handleRegister}
              disabled={submitting}
              activeOpacity={0.8}
              className="w-full bg-primary rounded-lg py-4 items-center flex-row justify-center"
            >
              {submitting ? (
                <ActivityIndicator size="small" color="#FFF" />
              ) : (
                <Text className="text-textPrimary font-semibold text-lg">
                  Register
                </Text>
              )}
            </TouchableOpacity>

            <View className="flex-row mt-4 justify-center">
              <Text className="text-textSecondary">
                Already have an account?{" "}
              </Text>
              <TouchableOpacity onPress={() => router.replace("/signin")}>
                <Text className="text-accent font-semibold">Sign In</Text>
              </TouchableOpacity>
            </View>
          </Animated.View>
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
}
