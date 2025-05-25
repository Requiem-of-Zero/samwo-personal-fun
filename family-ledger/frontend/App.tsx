import "./global.css";  
import "expo-router/entry";         // ← make sure this comes first
import { Slot } from "expo-router";
import { Provider } from "react-redux";
import { store } from "./store/store";

export default function App() {
  return (
      <Provider store={store}>
        <Slot />
      </Provider>
  );
}
