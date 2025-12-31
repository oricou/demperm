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
import {Toggle} from "@/stories/Toggle";

export default function Login() {
    const { loginAndCheckProfile, completeProfile } = useUser()!;

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showProfileForm, setShowProfileForm] = useState(false);
    
    // Champs du profil
    const [username, setUsername] = useState("");
    const [biography, setBiography] = useState("");
    const [location, setLocation] = useState("");
    const [isPrivate, setIsPrivate] = useState(false);

  const handleLogin = async () => {
    try {
      const result = await loginAndCheckProfile(email, password);
      
      if (result.needsProfile) {
        // Le profil n'existe pas, afficher le formulaire
        setShowProfileForm(true);
      }
      else
        router.replace("/feed")
    } catch (e: any) {
      alert("Erreur lors de la connexion: " + (e.message || e))
    }
  }

  const handleCompleteProfile = async () => {
    try {
      await completeProfile(username, biography, location, isPrivate);
      router.replace("/feed") // il y avait pas de redirectoin après la complétion du profil.
      // La navigation sera gérée automatiquement par le context
    } catch (e: any) {
      alert("Erreur lors de la création du profil: " + (e.message || e))
    }
  }
    const { colorScheme } = useThemeContext();
    const primaryColor = Colors[colorScheme].primary;
    const backgroundColor = Colors[colorScheme].background;

    if (showProfileForm) {
        return (
            <SafeAreaView style={[styles.container, {backgroundColor: backgroundColor}]}>
                <ThemedView style={[styles.loginContainer, {backgroundColor: primaryColor}]}>
                    <ThemedText style={styles.title}>
                        Complétez votre profil
                    </ThemedText>
                    
                    <InputBar
                        backgroundColor="background"
                        hideRightIcon
                        onChangeText={setUsername}
                        placeholder="Nom d'utilisateur"
                        value={username}
                    />

                    <InputBar
                        backgroundColor="background"
                        hideRightIcon
                        onChangeText={setBiography}
                        placeholder="Biographie"
                        bigInput
                        value={biography}
                    />

                    <InputBar
                        backgroundColor="background"
                        hideRightIcon
                        onChangeText={setLocation}
                        placeholder="Ville"
                        value={location}
                    />

                    <View style={styles.isPrivateToggle}>
                        <ThemedText>Privé</ThemedText>
                        <Toggle isEnabled={isPrivate} onValueChange={() => setIsPrivate(!isPrivate)}/>
                        <ThemedText>Public</ThemedText>
                    </View>

                    <Button
                        label="Valider"
                        onPress={handleCompleteProfile}
                        style={styles.loginButton}
                        size={"large"}
                    />
                </ThemedView>
            </SafeAreaView>
        );
    }

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
    },
    isPrivateToggle: {
        alignSelf: "center",
        alignItems: "center",
        flexDirection: "row",
        gap: Spacing.margin,
        marginTop: Spacing.margin
    }
})