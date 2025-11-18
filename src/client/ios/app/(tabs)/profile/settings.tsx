import React, {useEffect, useState} from 'react';
import {StyleSheet, View} from 'react-native';
import {Colors} from "@/constants/theme";
import {SafeAreaView} from "react-native-safe-area-context";
import {ThemedText} from "@/components/themed-text";
import {ThemedView} from "@/components/themed-view";
import {Toggle} from "@/stories/Toggle";
import {Button} from "@/stories/Button";
import {router} from "expo-router";
import {useTheme} from "@/hooks/use-theme";
import {Settings} from "@/api/types/profile/settings";
import {getSettings} from "@/api/mock/functions";

export default function SettingsScreen() {
    const { themeMode, setThemeMode, colorScheme } = useTheme();
    const [settings, setSettings] = useState<Settings>()
    const backgroundColor = Colors[colorScheme].primary;
    const [isShowingVote, setIsShowingVote] = useState<boolean>(false);
    const [isProfilePublic, setIsProfilePublic] = useState<boolean>(false);
    const [isLimitedToUndredVotes, setIsLimitedToUndredVotes] = useState<boolean>(false);
    const [allowedNotifications, setAllowedNotifications] = useState<boolean>(false);
    const [isLightTheme, setIsLightTheme] = useState<boolean>(colorScheme === 'light');
    const [isAutoTheme, setIsAutoTheme] = useState<boolean>(themeMode === 'auto');

    useEffect(() => {
        const _settings = getSettings();
        setSettings(_settings);

        setIsLimitedToUndredVotes(_settings.democracy.limitVotes);
        setIsShowingVote(_settings.democracy.shuwMyVote);
        setIsProfilePublic(_settings.social.public);
    })

    const handleThemeChange = () => {
        setIsAutoTheme(false);

        setIsLightTheme(prev => {
            const nextIsLight = !prev;
            setThemeMode(nextIsLight ? 'light' : 'dark');
            return nextIsLight;
        });
    };

    const handleAutoThemeChange = () => {
        setIsAutoTheme(prevIsAuto => {
            const nextIsAuto = !prevIsAuto;
            if (nextIsAuto) {
                setThemeMode('auto');
                setIsLightTheme(colorScheme === 'light');
            } else {
                const nextIsLight = colorScheme === 'light';
                setThemeMode(nextIsLight ? 'light' : 'dark');
                setIsLightTheme(nextIsLight);
            }
            return nextIsAuto;
        });
    };

    return(
        <SafeAreaView style={{ backgroundColor: Colors[colorScheme].background, flex: 1 }}>
            <ThemedView style={styles.container}>
                <ThemedView style={{flexDirection:"row", marginVertical: 20}}>
                    <Button
                        backgroundColor="background"
                        icon="chevron-back"
                        label=""
                        onPress={() => {router.back()}}
                        size="large"
                        style={{position: "absolute"}}
                    />
                    <ThemedText type="screenTitle" style={{marginInline: "auto"}}>Paramètres</ThemedText>
                </ThemedView>
                <ThemedView style={{flexDirection:"column"}}>
                    <ThemedText type={"title"} style={{marginInline: 22}}>Démocratie</ThemedText>
                    <ThemedView style={[styles.settingContainer, {backgroundColor} ]}>
                        <ThemedText type={"title"}>Montrer mon vote</ThemedText>
                        <Toggle
                            isEnabled={isShowingVote}
                            onValueChange={() => {setIsShowingVote(!isShowingVote);}}
                        />
                    </ThemedView>
                    <ThemedView style={[styles.settingContainer, {backgroundColor} ]}>
                        <ThemedText type={"title"}>Profil public</ThemedText>
                        <Toggle
                            isEnabled={isProfilePublic}
                            onValueChange={() => {setIsProfilePublic(!isProfilePublic);}}
                        />
                    </ThemedView>
                    <ThemedView style={[styles.settingContainer, {backgroundColor} ]}>
                        <ThemedText type={"title"}>Limiter à 100 voix</ThemedText>
                        <Toggle
                            isEnabled={isLimitedToUndredVotes}
                            onValueChange={() => {setIsLimitedToUndredVotes(!isLimitedToUndredVotes);}}
                        />
                    </ThemedView>
                    <ThemedText type={"title"} style={{marginInline: 22, marginTop: 28}}>Autres</ThemedText>
                    <ThemedView style={[styles.settingContainer, {backgroundColor} ]}>
                        <ThemedText type={"title"}>Notifications</ThemedText>
                        <Toggle
                            isEnabled={allowedNotifications}
                            onValueChange={() => {setAllowedNotifications(!allowedNotifications);}}
                        />
                    </ThemedView>
                    <ThemedView style={[styles.settingContainer, {backgroundColor} ]}>
                        <ThemedText type={"title"}>Thème</ThemedText>
                        <View style={{gap: 10}}>
                            <View style={{alignItems: "center", gap: 5}}>
                                <ThemedText>Automatique</ThemedText>
                                <Toggle
                                    isEnabled={isAutoTheme}
                                    onValueChange={handleAutoThemeChange}
                                />
                            </View>
                            <View style={{flexDirection: "row", gap: 5}}>
                                <ThemedText>🌙</ThemedText>
                                <Toggle
                                    isEnabled={isLightTheme}
                                    onValueChange={handleThemeChange}
                                />
                                <ThemedText>☀️</ThemedText>
                            </View>
                        </View>
                    </ThemedView>
                </ThemedView>
            </ThemedView>
        </SafeAreaView>
    );

}

const styles = StyleSheet.create({
    settingContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderRadius: 16,
        padding: 24,
        marginLeft: 8,
        marginRight: 8,
        marginBottom: 8,
    },
    container: {
        height: "100%"
    }
});
