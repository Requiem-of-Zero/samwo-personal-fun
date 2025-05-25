// app/index.tsx
import { Redirect } from "expo-router";
import { useSelector } from "react-redux";
import type { RootState } from "../store/store";

export default function Index() {
  const user = useSelector((state: RootState) => state.auth.user);

  // if you already know where to go, simply return a Redirect:
  return user
    ? <Redirect href="/home" />
    : <Redirect href="/signin"/>;
}
