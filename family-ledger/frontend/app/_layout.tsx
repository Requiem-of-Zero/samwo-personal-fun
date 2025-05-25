// app/_layout.tsx

// 1) Expo-Router Slot for file-based routing
import { Slot } from "expo-router";

// 2) Redux setup
import { Provider } from "react-redux";
import { store } from "../store/store";

export default function RootLayout() {
  return (
    // 3) Wrap all screens in the Redux store provider
    <Provider store={store}>
      {/* 4) Render whatever route is active (app/index.tsx, app/login.tsx, etc.) */}
      <Slot />
    </Provider>
  );
}
