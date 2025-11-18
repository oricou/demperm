import {Colors} from "@/constants/theme";
import {useThemeContext} from "@/contexts/theme-context";
import ToggleSwitch from 'toggle-switch-react-native'

export interface ToggleProps {
    /** Is toggle enabled */
    isEnabled: boolean;
    /** Toggle handler */
    onValueChange: () => void;
}

export const Toggle = ({
                           isEnabled,
                           onValueChange
                       }: ToggleProps) => {
    const { colorScheme } = useThemeContext();
    return (
    <ToggleSwitch
        isOn={isEnabled}
        onColor={Colors[colorScheme].highlight1}
        offColor={Colors[colorScheme].text}
        onToggle={() => onValueChange()}
    />
    );
};