import AsyncStorage from "@react-native-async-storage/async-storage";
import {Platform} from "react-native";
import * as SecureStore from 'expo-secure-store';

export async function getInStoreUsageOfRealData() : Promise<string> {
    if(Platform.OS === "ios" || Platform.OS === "android") {
        return await SecureStore.getItemAsync("usingRealData") ?? "false";
    }
    return await AsyncStorage.getItem("usingRealData") ?? "false";
}