// store/authSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface User {
  id: number;
  email: string;
  full_name?: string;
}

interface AuthState {
  user: User | null;
}

const initialState: AuthState = { user: null };

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login(state, action: PayloadAction<User>) {
      state.user = action.payload;
    },
    logout(state) {
      state.user = null;
    },
    register(state, action: PayloadAction<User>){
      state.user = action.payload;
    }
  },
});

export const { login, logout, register } = authSlice.actions;
export default authSlice.reducer;
