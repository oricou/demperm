import type { StyleProp, ViewStyle } from 'react-native';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import {useThemeContext} from "@/contexts/theme-context";
import {Colors, VariantKey} from '@/constants/theme';
import {iconVariants, fontFamily} from "@/stories/utils";
import {Ionicons} from "@expo/vector-icons";

export interface ButtonProps {
  /** What background color to use */
  backgroundColor?: VariantKey;
  /** What icon to show */
  icon?: iconVariants;
  /** How large should the button be? */
  size?: 'small' | 'medium' | 'large';
  /** Button contents */
  label?: string;
  /** Click handler */
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
}

/** Primary UI component for user interaction */
export const Button = ({
  size = 'medium',
    backgroundColor = "highlight1",
  label,
  icon,
  style,
  onPress,
}: ButtonProps) => {
  const { colorScheme } = useThemeContext();

  const sizeStyle = styles[size];
  const textSizeStyle = textSizeStyles[size];
  const textColor = backgroundColor === "primary" || backgroundColor === "background" ?
      Colors[colorScheme].text : Colors[colorScheme].background;

  let iconSize: number = 15;
  if(size === "small"){
      iconSize = 12;
  }
  if(size === "large"){
      iconSize = 18;
  }

  return (
    <TouchableOpacity accessibilityRole="button" activeOpacity={0.6} onPress={onPress}>
      <View
        style={[
          styles.button,
          sizeStyle,
          style,
          { borderColor: 'black', backgroundColor: Colors[colorScheme][backgroundColor] },
        ]}
      >
          {icon &&(
              <Ionicons name={icon} color={textColor} size={iconSize}/>
          )}
          {label && (
              <Text style={[textSizeStyle, {color: textColor, fontFamily}]}>{label}</Text>
          )}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    borderRadius: 16,
    flexDirection: 'row',
    gap: 6,
    justifyContent: 'center',   // horizontally center text + icon
    alignItems: 'center',
  },

  buttonText: {
    textAlign: 'center',
    alignItems: "center",
  },
  small: {
    paddingVertical: 1,
    paddingHorizontal: 14,
  },
  smallText: {
    fontSize: 12,
  },
  medium: {
    paddingVertical: 4,
    paddingHorizontal: 17,
  },
  mediumText: {
    fontSize: 14,
  },
  large: {
    paddingVertical: 7,
    paddingHorizontal: 20,
  },
  largeText: {
    fontSize: 16,
  },
});

const textSizeStyles = {
  small: styles.smallText,
  medium: styles.mediumText,
  large: styles.largeText,
};
