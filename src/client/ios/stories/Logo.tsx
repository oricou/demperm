import { useThemeContext } from '@/contexts/theme-context';
import React from 'react';
import { Image, StyleSheet, View } from 'react-native';

export interface LogoProps {
    width?: number;
    height?: number;
}

export const Logo: React.FC<LogoProps> = ({ width = 40, height = 40 }) => {
    const { colorScheme } = useThemeContext();

    const logoSource = colorScheme === 'dark'
        ? require('@/assets/images/logo_sombre.png')
        : require('@/assets/images/logo_claire.png');

    return (
        <View style={[styles.container, { width, height }]}>
            <Image
                source={logoSource}
                style={[styles.logo, { width, height }]}
                resizeMode="contain"
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    logo: {
        width: '100%',
        height: '100%',
    },
});
