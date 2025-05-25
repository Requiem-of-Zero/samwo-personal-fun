// store/store.ts
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/authSlice"; // This must be a function

export const store = configureStore({
  reducer: {
    auth: authReducer, // authReducer is the slice.reducer from above
  },
});

// For TS usage in components
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
