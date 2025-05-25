// app/home.tsx
import { View, Text } from "react-native";

export default function Home() {
  return (
    <View className="flex-1 bg-background justify-center items-center p-4">
      <Text className="text-2xl text-textPrimary">
        Welcome to Family Ledger!
      </Text>
    </View>
  );
}
