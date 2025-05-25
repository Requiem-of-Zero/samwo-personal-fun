// app/+not-found.tsx
import { View, Text, TouchableOpacity } from "react-native";
// useRouter gives you push(), replace(), back(), etc.
import { useRouter } from "expo-router";

export default function NotFound() {
  // grab the router instance
  const router = useRouter();

  return (
    <View className="flex-1 bg-background justify-center items-center p-4">
      {/* Title */}
      <Text className="text-xl text-textPrimary mb-4">
        ❓ Page not found
      </Text>

      {/* Go back button */}
      <TouchableOpacity
        onPress={() => router.back()}        // <-- use router.back() instead of Stack.pop()
        className="px-4 py-2 bg-primary rounded"
      >
        <Text className="text-textPrimary">
          Go Back
        </Text>
      </TouchableOpacity>
    </View>
  );
}
