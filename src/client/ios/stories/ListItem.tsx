import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet, StyleProp, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors } from '@/constants/theme';
import {fontFamily, Ministere, ministereDomainColors} from '@/stories/utils';
import {Chip} from "@/stories/Chip";

export interface ListItemProps {
    /** URL de l'image de profil */
    avatarUrl: string;
    /** Nom d'utilisateur */
    username: string;
    /** Nombre de votes */
    votes: number;
    /** Visibilité du la croix*/
    isDeleteVisible?: boolean;
    /** Ministère pour lequel l'utilisateur est membre*/
    ministry?: Ministere;
    /** Est ce qu'il est underlined ? */
    isUnderlined?: boolean;
    /** Fonction au clic sur la carte (optionnelle) */
    onPress?: () => void;
    /** Fonction au clic sur la croix (optionnelle) */
    onRemove?: () => void;
    /** Style personnalisé */
    style?: StyleProp<ViewStyle>;
}

/** Élément de liste — avatar, nom, votes et option de suppression */
export const ListItem = ({
                             avatarUrl,
                             username,
                             votes,
                             ministry,
                             isUnderlined = false,
                             isDeleteVisible,
                             onPress,
                             onRemove,
                             style,
                         }: ListItemProps) => {
    const { colorScheme } = useThemeContext();
    const backgroundColor = isUnderlined ? Colors[colorScheme].background : Colors[colorScheme].primary;
    const textColor = Colors[colorScheme].text;
    const highlightColor = Colors[colorScheme].highlight1;
    const borderColor = isUnderlined ? Colors[colorScheme].highlight1 : Colors[colorScheme].primary;

    return (
        <TouchableOpacity
            activeOpacity={onPress ? 0.7 : 1}
            onPress={onPress}
            accessibilityRole="button"
            style={[
                styles.container,
                { backgroundColor, borderColor },
                style,
            ]}
        >
            {/* Partie gauche : Avatar + Nom */}
            <View style={styles.leftSection}>
                <Image source={{ uri: avatarUrl }} style={styles.avatar} />
                <Text style={[styles.username, { color: textColor, fontFamily }]}>{username}</Text>
            </View>

            {/* Partie droite : Votes + icône de suppression */}
            <View style={styles.rightSection}>
                <View style={{flexDirection:"column", alignItems: 'center'}}>
                    <Text style={[styles.votes, { color: highlightColor, fontFamily }]}>
                        {votes} votes
                    </Text>
                    {ministry &&
                        <Chip size={"small"} label={ministry} backgroundColor={ministereDomainColors[ministry]}/>
                    }
                </View>

                {isDeleteVisible && (
                    <TouchableOpacity
                        onPress={(e) => {
                            e.stopPropagation();
                            onRemove && onRemove();
                        }}
                        accessibilityRole="button"
                        style={styles.removeButton}
                    >
                        <Ionicons name="close" size={20} color={highlightColor} />
                    </TouchableOpacity>
                )}
            </View>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderWidth: 1.5,
        borderRadius: 16,
        padding: 16,
        margin: 8,
    },
    leftSection: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 10,
    },
    avatar: {
        width: 40,
        height: 40,
        borderRadius: 20,
    },
    username: {
        fontSize: 16,
    },
    rightSection: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    votes: {
        fontSize: 15,
        fontWeight: 'bold',
    },
    removeButton: {
        padding: 2,
    },
});
