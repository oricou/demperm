import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Colors, Spacing, Typography } from "@/constants/theme";
import { useThemeContext } from "@/contexts/theme-context";
import { useUser } from "@/contexts/user-context";
import { Button } from "@/stories/Button";
import { InputBar } from "@/stories/InputBar";
import { router } from "expo-router";
import React, { useState } from "react";
import {StyleSheet, TouchableOpacity, View} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import {Toggle} from "@/stories/Toggle";

export default function Register() {
    const { registerAndCheckProfile, completeProfile } = useUser()!;
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");
    const [biography, setBiography] = useState("");
    const [location, setLocation] = useState("");
    const [isPrivate, setIsPrivate] = useState(false);
    const [step, setStep] = useState(1);

    const handleRegister = async () => {
      const registered = await registerAndCheckProfile(email, password);

      if (registered === true)
        router.replace("//(tabs)/feed");

      // registered but not created in backend
      else if (registered === false) setStep(2);

      else alert("Erreur lors de l'inscription: " + registered.message);
    }

    const handleCompleteProfile = async () => {
      await completeProfile(username, biography, location, isPrivate);
      router.replace("/feed");
    }

    const { colorScheme } = useThemeContext();
    const primaryColor = Colors[colorScheme].primary;
    const backgroundColor = Colors[colorScheme].background;

    return (
        <SafeAreaView style={[styles.container, {backgroundColor: backgroundColor}]}>
            <ThemedView style={[styles.loginContainer, {backgroundColor: primaryColor}]}>
                <ThemedText style={styles.title}>
                    S'inscrire
                </ThemedText>
                {step === 1 &&
                    <Step1
                        email={email}
                        password={password}
                        setEmail={setEmail}
                        setPassword={setPassword}
                        handleRegister={handleRegister}
                        setStep={setStep}/>
                }
                {step === 2 &&
                    <Step2
                        username={username}
                        biography={biography}
                        setUsername={setUsername}
                        setBiography={setBiography}
                        setStep={setStep}
                    />
                }
                {step === 3 &&
                    <Step3
                        location={location}
                        setLocation={setLocation}
                        setIsPrivate={setIsPrivate}
                        isPrivate={isPrivate}
                        handleCompleteProfile={handleCompleteProfile}
                        setStep={setStep}
                    />
                }
                <TouchableOpacity onPress={() => router.replace("/auth/login")}>
                    <ThemedText style={styles.bottomLinkText}>
                        Vouos avez déjà un compte ? <ThemedText>Connectez-vous</ThemedText>
                    </ThemedText>
                </TouchableOpacity>
            </ThemedView>
        </SafeAreaView>
    );
}

interface Step1Props {
    email: string,
    password: string,
    setEmail: (text: string) => void,
    setPassword: (text: string) => void;
    setStep: (step: number) => void;
    handleRegister: () => void;
}

function Step1({setEmail, setPassword, handleRegister, email, password}: Step1Props) {
    return (
        <>
            <InputBar
                backgroundColor="background"
                hideRightIcon
                onChangeText={setEmail}
                placeholder="Email"
                value={email}
            />

            <InputBar
                backgroundColor="background"
                hideRightIcon
                onChangeText={setPassword}
                placeholder="Mot de passe"
                isPassword={true}
                value={password}
            />

            <Button
                label="Continuer"
                onPress={() => handleRegister()}
                style={styles.loginButton}
                size={"large"}
            />
        </>
    )
}

interface Step2Props {
    username: string,
    biography: string,
    setUsername: (text: string) => void,
    setBiography: (text: string) => void;
    setStep: (step: number) => void;
}
function Step2({setUsername, setBiography,  setStep, username, biography}: Step2Props) {
    return (
        <>
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
            <View style={styles.formButtons}>
                <Button
                    label="Retour"
                    onPress={() => setStep(1)}
                    style={styles.loginButton}
                    size={"large"}
                />
                <Button
                    label="Continuer"
                    onPress={() => setStep(3)}
                    style={styles.loginButton}
                    size={"large"}
                />
            </View>
        </>
    )
}

interface Step3Props {
    setIsPrivate: (status: boolean) => void,
    setLocation: (text: string) => void,
    isPrivate: boolean;
    location: string;
    handleCompleteProfile: () => void;
    setStep: (step: number) => void;
}

function Step3({setLocation, setIsPrivate, isPrivate, handleCompleteProfile, setStep, location} : Step3Props) {
    return (
        <>
            <InputBar
                backgroundColor="background"
                hideRightIcon
                onChangeText={setLocation}
                value={location}
                placeholder="Ville"
            />
            <View style={styles.isPrivateToggle}>
                <ThemedText>Privé</ThemedText>
                <Toggle isEnabled={isPrivate} onValueChange={() => setIsPrivate(!isPrivate)}/>
                <ThemedText>Public</ThemedText>
            </View>
            <View style={styles.formButtons}>
                <Button
                    label="Retour"
                    onPress={() => setStep(2)}
                    style={styles.loginButton}
                    size={"large"}
                />
                <Button
                    label="Valider l'inscription"
                    onPress={handleCompleteProfile}
                    style={styles.loginButton}
                    size={"large"}
                />
            </View>
        </>
    )
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
        gap: Spacing.margin
    },
    formButtons:{
        flexDirection: "row",
        alignSelf: "center",
    }
})