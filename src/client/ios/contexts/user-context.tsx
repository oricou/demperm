import React, {createContext, useState, useContext, useEffect} from "react";
import {onAuthStateChanged, signOut, User} from "firebase/auth";
import {auth} from "@/auth/firebase-config";
import {signInWithEmailAndPassword, createUserWithEmailAndPassword} from "firebase/auth";
import { router } from "expo-router";

interface UserContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<any>;
  register: (email: string, password: string) => Promise<any>;
  logout: () => Promise<any>;
  loading: boolean;
}

export const UserContext = createContext<UserContextType>({ user: null, login: async (): Promise<undefined> => {}, register: async (): Promise<undefined> => {}, logout: async (): Promise<undefined> => {}, loading: true});

export const UserProvider = ({children}: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      setLoading(false);
      console.log("User state changed:", firebaseUser);
      if (firebaseUser) {
        router.replace("/feed")
      }
      else {
        router.replace("/auth/login")
      }
    });

    return () => unsub();
  }, []);



  async function login(email: string, password: string) {
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      setUser(result.user);
    } catch (e) {
      console.log("Erreur login :", e);
      return e;
    }
  }

  async function register(email: string, password: string) {
    try {
      const result = await createUserWithEmailAndPassword(auth, email, password);
      setUser(result.user);
    } catch (e) {
      console.log("Erreur register :", e);
      return e;
    }
  }

  async function logout() {
    try {
      await signOut(auth);
      setUser(null);
    } catch (e) {
      console.log("Erreur logout :", e);
      console.log(typeof e);
      return e;
    }
  }


  return (
    <UserContext.Provider value={{ user, login, register, logout, loading }}>

    {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
