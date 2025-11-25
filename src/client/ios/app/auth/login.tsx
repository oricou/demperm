import { useUser } from "@/contexts/user-context";
import {TextInput, View, Text, TouchableOpacity, StyleSheet} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import React, { useState } from "react";
import {router} from "expo-router";
import {ThemedView} from "@/components/themed-view";
import {InputBar} from "@/stories/InputBar";
import {Button} from "@/stories/Button";
import {Colors, Spacing, Typography} from "@/constants/theme";
import {useThemeContext} from "@/contexts/theme-context";
import {ThemedText} from "@/components/themed-text";

export default function Login() {
    const { login } = useUser()!;

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const e = await login(email, password);
    console.log(e);
    if (e) {
      alert("Erreur lors de la connexion: " + e)
    }
  }
    const { colorScheme } = useThemeContext();
    const primaryColor = Colors[colorScheme].primary;
    const backgroundColor = Colors[colorScheme].background;

    return (
        <SafeAreaView style={[styles.container, {backgroundColor: backgroundColor}]}>
            <ThemedView style={[styles.loginContainer, {backgroundColor: primaryColor}]}>
                <ThemedText style={styles.title}>
                    Se connecter
                </ThemedText>
                <InputBar
                    backgroundColor="background"
                    hideRightIcon
                    onChangeText={setEmail}
                    placeholder="Email"
                    rightIcon="search"
                />

                <InputBar
                    backgroundColor="background"
                    hideRightIcon
                    onChangeText={setPassword}
                    placeholder="Mot de passe"
                    rightIcon="search"
                    isPassword={true}
                />

                <Button
                    label="Se connecter"
                    onPress={handleLogin}
                    style={styles.loginButton}
                    size={"large"}
                />

                <TouchableOpacity onPress={() => router.replace("/auth/register")}>
                    <ThemedText style={styles.bottomLinkText}>
                        Pas de compte ? <ThemedText>Inscrivez-vous</ThemedText>
                    </ThemedText>
                </TouchableOpacity>
            </ThemedView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        height: "100%",
        backgroundColor: "red",
        justifyContent: "center"
    },
    loginContainer: {
        backgroundColor: "blue",
        borderRadius: 12,
        margin: Spacing.margin
    },
    loginButton: {
        marginHorizontal: Spacing.margin,
        marginTop: Spacing.margin
    },
    bottomLinkText: {
        margin: Spacing.margin,
        marginTop: Spacing.margin * 2,
        alignSelf: "center",
    },
    title: {
        alignSelf: "center",
        fontSize: Typography.sizes.title,
        fontWeight: Typography.weights.semiBold,
        margin: Spacing.margin,
    }
})