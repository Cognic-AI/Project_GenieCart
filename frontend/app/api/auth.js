// auth.js
import { auth } from "../database/firebase_config.js";
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from "firebase/auth";

// Sign in function
export const signIn = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    console.log(userCredential.user.uid)
    return userCredential.user.uid;
  } catch (error) {
    console.error("Error signing in:", error);
    throw error;
  }
};

// Sign up function
export const signUp = async (email, password) => {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return userCredential.user;
  } catch (error) {
    console.error("Error signing up:", error);
    throw error;
  }
};

