import { StyleSheet, Text, type TextProps } from 'react-native';

import { useThemeColor } from '@/hooks/use-theme-color';
import { Typography } from '@/constants/theme';

export type ThemedTextProps = TextProps & {
  lightColor?: string;
  darkColor?: string;
  type?: 'default' | 'title' | 'screenTitle' | 'profile' | 'seeMore' | 'link';
};

export function ThemedText({
  style,
  lightColor,
  darkColor,
  type = 'default',
  ...rest
}: ThemedTextProps) {
  const color = useThemeColor({ light: lightColor, dark: darkColor }, 'text');

  return (
    <Text
      style={[
        { color },
        type === 'default' ? styles.default : undefined,
        type === 'title' ? styles.title : undefined,
        type === 'screenTitle' ? styles.screenTitle : undefined,
        type === 'profile' ? styles.profile : undefined,
        type === 'seeMore' ? styles.seeMore : undefined,
        type === 'link' ? styles.link : undefined,
        style,
      ]}
      {...rest}
    />
  );
}

const styles = StyleSheet.create({
  default: {
    fontSize: Typography.sizes.general,
    fontWeight: Typography.weights.regular,
    fontFamily: Typography.fonts?.regular,
  },
  title: {
    fontSize: Typography.sizes.title,
    fontWeight: Typography.weights.regular,
    fontFamily: Typography.fonts?.regular,
  },
  screenTitle: {
    fontSize: Typography.sizes.screenTitle,
    fontWeight: Typography.weights.regular,
    fontFamily: Typography.fonts?.regular,
  },
  profile: {
    fontSize: Typography.sizes.profile,
    fontWeight: Typography.weights.semiBold,
    fontFamily: Typography.fonts?.semiBold,
  },
  seeMore: {
    fontSize: Typography.sizes.seeMore,
    fontWeight: Typography.weights.semiBold,
    fontFamily: Typography.fonts?.semiBold,
  },
  link: {
    fontSize: Typography.sizes.general,
    fontWeight: Typography.weights.semiBold,
    fontFamily: Typography.fonts?.semiBold,
  },
});
