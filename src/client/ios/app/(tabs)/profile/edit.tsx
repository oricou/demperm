import React, { useState, useEffect } from 'react';
import {
    StyleSheet,
    View,
    ActivityIndicator,
    ScrollView,
    Alert,
} from 'react-native';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Button } from '@/stories/Button';
import { InputBar } from '@/stories/InputBar';
import { Toggle } from '@/stories/Toggle';
import { Colors, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { userService, UpdateUserDto } from '@/api/services/user.service';

export default function EditProfileScreen() {
    const { colorScheme } = useTheme();
    const backgroundColor = Colors[colorScheme].primary;

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Champs du formulaire
    const [username, setUsername] = useState('');
    const [bio, setBio] = useState('');
    const [location, setLocation] = useState('');
    const [profilePictureUrl, setProfilePictureUrl] = useState('');
    const [isPrivate, setIsPrivate] = useState(false);

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            setLoading(true);
            setError(null);
            const profile = await userService.getMe();
            if (profile) {
                setUsername(profile.username || '');
                setBio(profile.biography || '');
                setLocation(profile.location || '');
                setProfilePictureUrl((profile as any).profile_picture_url || '');
                setIsPrivate(profile.isPrivate || false);
            }
        } catch (err: any) {
            console.error('Erreur lors de la récupération du profil:', err);
            if (err.response) {
                setError(err.response?.data?.message || err.message || 'Erreur lors de la récupération du profil');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        try {
            setSaving(true);
            setError(null);

            const updateData: UpdateUserDto = {
                username: username || undefined,
                display_name: username || undefined,
                bio: bio || undefined,
                location: location || undefined,
                profile_picture_url: profilePictureUrl || undefined,
                privacy: isPrivate ? 'private' : 'public',
            };

            await userService.updateMe(updateData);
            
        } catch (err: any) {
            console.error('Erreur lors de la mise à jour du profil:', err);
            const errorMessage = err.response?.data?.message || err.message || 'Erreur lors de la mise à jour du profil';
            Alert.alert('Erreur', errorMessage);
            setError(errorMessage);
        } finally {
            setSaving(false);
            router.navigate('/profile');
        }
    };

    if (loading) {
        return (
            <SafeAreaView style={{ backgroundColor: Colors[colorScheme].background, flex: 1 }}>
                <ThemedView style={[styles.container, styles.centerContent]}>
                    <ActivityIndicator size="large" />
                    <ThemedText>Chargement du profil...</ThemedText>
                </ThemedView>
            </SafeAreaView>
        );
    }

    return (
        <SafeAreaView style={{ backgroundColor: Colors[colorScheme].background, flex: 1 }}>
            <ThemedView style={styles.container}>
                {/* Header */}
                <ThemedView style={styles.header}>
                    <Button
                        backgroundColor="background"
                        icon="chevron-back"
                        label=""
                        onPress={() => router.back()}
                        size="large"
                        style={styles.backButton}
                    />
                    <ThemedText type="screenTitle" style={styles.headerTitle}>
                        Modifier le profil
                    </ThemedText>
                    <View style={styles.headerSpacer} />
                </ThemedView>

                <ScrollView 
                    style={styles.scrollView} 
                    showsVerticalScrollIndicator={false}
                    keyboardShouldPersistTaps="handled"
                >
                        {/* Nom d'utilisateur */}
                        <ThemedView style={styles.fieldContainer}>
                            <ThemedText type="title" style={styles.fieldLabel}>
                                Nom d'utilisateur
                            </ThemedText>
                            <InputBar
                                placeholder="Votre nom d'utilisateur"
                                value={username}
                                onChangeText={setUsername}
                                backgroundColor="primary"
                                hideRightIcon
                                style={styles.input}
                            />
                        </ThemedView>

                        {/* Biographie */}
                        <ThemedView style={styles.fieldContainer}>
                            <ThemedText type="title" style={styles.fieldLabel}>
                                Biographie
                            </ThemedText>
                            <InputBar
                                placeholder="Décrivez-vous en quelques mots..."
                                value={bio}
                                onChangeText={setBio}
                                backgroundColor="primary"
                                bigInput
                                hideRightIcon
                                style={styles.input}
                            />
                        </ThemedView>

                        {/* Localisation */}
                        <ThemedView style={styles.fieldContainer}>
                            <ThemedText type="title" style={styles.fieldLabel}>
                                Localisation
                            </ThemedText>
                            <InputBar
                                placeholder="Votre localisation"
                                value={location}
                                onChangeText={setLocation}
                                backgroundColor="primary"
                                hideRightIcon
                                style={styles.input}
                            />
                        </ThemedView>

                        {/* URL Photo de profil */}
                        <ThemedView style={styles.fieldContainer}>
                            <ThemedText type="title" style={styles.fieldLabel}>
                                URL de la photo de profil
                            </ThemedText>
                            <InputBar
                                placeholder="https://exemple.com/photo.jpg"
                                value={profilePictureUrl}
                                onChangeText={setProfilePictureUrl}
                                backgroundColor="primary"
                                hideRightIcon
                                style={styles.input}
                            />
                        </ThemedView>

                        {/* Profil privé */}
                        <ThemedView style={[styles.settingContainer, { backgroundColor }]}>
                            <ThemedText type="title">Profil privé</ThemedText>
                            <Toggle
                                isEnabled={isPrivate}
                                onValueChange={() => setIsPrivate(!isPrivate)}
                            />
                        </ThemedView>

                        {/* Erreur */}
                        {error && (
                            <ThemedView style={styles.errorContainer}>
                                <ThemedText style={styles.errorText}>{error}</ThemedText>
                            </ThemedView>
                        )}

                        {/* Bouton de sauvegarde */}
                        <View style={styles.buttonContainer}>
                            <Button
                                label={saving ? "Enregistrement..." : "Enregistrer les modifications"}
                                onPress={handleSave}
                                backgroundColor="highlight1"
                                size="large"
                                style={styles.saveButton}
                            />
                            <Button
                                label="Annuler"
                                onPress={() => router.back()}
                                backgroundColor="background"
                                size="large"
                                style={styles.cancelButton}
                            />
                        </View>
                    </ScrollView>
                </ThemedView>
            </SafeAreaView>
        );
    }

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    centerContent: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        marginVertical: 20,
        paddingHorizontal: Spacing.margin,
    },
    backButton: {
        position: 'absolute',
        left: Spacing.margin,
        zIndex: 1,
    },
    headerTitle: {
        flex: 1,
        textAlign: 'center',
    },
    headerSpacer: {
        width: 40,
    },
    scrollView: {
        flex: 1,
        paddingHorizontal: Spacing.margin,
    },
    fieldContainer: {
        marginBottom: 16,
    },
    fieldLabel: {
        marginBottom: 8,
        marginLeft: 8,
    },
    input: {
        borderRadius: Spacing.borderRadius,
    },
    settingContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderRadius: Spacing.borderRadius,
        padding: 24,
        marginBottom: 16,
    },
    errorContainer: {
        padding: Spacing.padding,
        marginBottom: 16,
    },
    errorText: {
        color: Colors.light.highlight2,
        textAlign: 'center',
    },
    buttonContainer: {
        marginTop: 8,
        marginBottom: 32,
        gap: 12,
    },
    saveButton: {
        width: '100%',
    },
    cancelButton: {
        width: '100%',
    },
});
