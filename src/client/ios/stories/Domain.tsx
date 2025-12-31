import React from 'react';
import {
    View,
    Text,
    TouchableOpacity,
    StyleSheet,
    StyleProp,
    ViewStyle,
    ImageBackground,
} from 'react-native';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors } from '@/constants/theme';
import { fontFamily } from '@/stories/utils';

export type DomainBackground =
    | 'Culture'
    | 'Education'
    | 'Emploi'
    | 'Environnement'
    | 'Numerique'
    | 'Sante'
    | 'Securite'
    | 'Sport'
    | 'Transport';

const DOMAIN_IMAGES = {
    Culture: require('../assets/Domains/Culture.png'),
    Education: require('../assets/Domains/Education.png'),
    Emploi: require('../assets/Domains/Emploi.png'),
    Environnement: require('../assets/Domains/Environnement.png'),
    Numerique: require('../assets/Domains/Numerique.png'),
    Sante: require('../assets/Domains/Sante.png'),
    Securite: require('../assets/Domains/Securite.png'),
    Sport: require('../assets/Domains/Sport.png'),
    Transport: require('../assets/Domains/Transport.png'),
} as const;

const DOMAIN_ASPECT_RATIO = 1576 / 495;

export interface DomainProps {
    label: string;
    background: DomainBackground;
    onPress?: () => void;
    textColor?: string;
    style?: StyleProp<ViewStyle>;
}

export const Domain = ({ label, background, onPress, textColor, style }: DomainProps) => {
    const { colorScheme } = useThemeContext();
    const defaultTextColor = Colors[colorScheme].text;

    return (
        <TouchableOpacity
            activeOpacity={onPress ? 0.7 : 1}
            onPress={onPress}
            accessibilityRole="button"
            style={[styles.container, style, { aspectRatio: DOMAIN_ASPECT_RATIO }]}
        >
            <ImageBackground
                source={DOMAIN_IMAGES[background]}
                resizeMode="cover"
                style={styles.bg}          // ✅ force fill
                imageStyle={styles.bgImg}  // ✅ force fill
            >
                <View style={styles.center}>
                    <Text
                        numberOfLines={2}
                        style={[styles.label, { color: textColor ?? defaultTextColor, fontFamily }]}
                    >
                        {label}
                    </Text>
                </View>
            </ImageBackground>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        width: '100%',          // ✅ responsive width by default
        borderRadius: 16,
        overflow: 'hidden',
    },
    bg: {
        width: '100%',
        height: '100%',
        justifyContent: 'center',
    },
    bgImg: {
        width: '100%',
        height: '100%',
        borderRadius: 16,
    },
    center: {
        paddingHorizontal: 16,
        alignItems: 'center',
        justifyContent: 'center',
    },
    label: {
        fontSize: 18,
        fontWeight: '700',
        textAlign: 'center',
    },
});
