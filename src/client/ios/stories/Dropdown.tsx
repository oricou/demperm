import React, { useMemo, useState } from 'react';
import {
    Modal,
    Pressable,
    StyleProp,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
    ViewStyle,
    FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useThemeContext } from '@/contexts/theme-context';
import { Colors, Spacing, Typography } from '@/constants/theme';
import { fontFamily } from '@/stories/utils';

export type DropdownOption<T extends string | number = string> = {
    label: string;
    value: T;
};

export interface DropdownProps<T extends string | number = string> {
    options: Array<DropdownOption<T>>;
    /** Controlled value */
    value?: T;
    /** Uncontrolled initial value */
    defaultValue?: T;
    /** Placeholder when no value */
    placeholder?: string;
    /** Callback when selection changes */
    onChange?: (value: T) => void;
    /** Disable interactions */
    disabled?: boolean;
    /** Error state (border turns highlight2/red) */
    error?: boolean;
    /** Optional container style */
    style?: StyleProp<ViewStyle>;
}

export function Dropdown<T extends string | number = string>({
                                                                 options,
                                                                 value,
                                                                 defaultValue,
                                                                 placeholder = 'Sélectionner…',
                                                                 onChange,
                                                                 disabled = false,
                                                                 error = false,
                                                                 style,
                                                             }: DropdownProps<T>) {
    const { colorScheme } = useThemeContext();
    const palette = Colors[colorScheme];

    const [open, setOpen] = useState(false);
    const [internalValue, setInternalValue] = useState<T | undefined>(defaultValue);

    const currentValue = value !== undefined ? value : internalValue;

    const currentLabel = useMemo(() => {
        const found = options.find(o => o.value === currentValue);
        return found?.label ?? '';
    }, [options, currentValue]);

    const handleSelect = (val: T) => {
        if (value === undefined) setInternalValue(val);
        onChange?.(val);
        setOpen(false);
    };

    const borderColor = error
        ? palette.highlight2
        : palette.highlight1;

    return (
        <>
            <TouchableOpacity
                activeOpacity={0.7}
                disabled={disabled}
                onPress={() => setOpen(true)}
                accessibilityRole="button"
                style={[
                    styles.trigger,
                    {
                        backgroundColor: palette.primary,
                        borderColor,
                        opacity: disabled ? 0.6 : 1,
                    },
                    style,
                ]}
            >
                <Text
                    style={[
                        styles.label,
                        {
                            color: currentLabel ? palette.text : palette.text + '99',
                            fontFamily,
                        },
                    ]}
                    numberOfLines={1}
                >
                    {currentLabel || placeholder}
                </Text>
                <Ionicons
                    name="chevron-down"
                    size={18}
                    color={palette.text}
                    style={[styles.chevron, open && styles.chevronOpen]}
                />
            </TouchableOpacity>

            <Modal
                visible={open}
                transparent
                animationType="fade"
                onRequestClose={() => setOpen(false)}
            >
                <Pressable style={styles.backdrop} onPress={() => setOpen(false)} />

                <View
                    style={[
                        styles.sheet,
                        { backgroundColor: palette.primary, borderColor: borderColor },
                    ]}
                    accessibilityRole="menu"
                >
                    <View style={styles.sheetHeader}>
                        <TouchableOpacity onPress={() => setOpen(false)} accessibilityRole="button">
                            <Ionicons name="close" size={20} color={palette.text} />
                        </TouchableOpacity>
                    </View>

                    <FlatList
                        data={options}
                        keyExtractor={(item) => String(item.value)}
                        ItemSeparatorComponent={() => (
                            <View
                                style={{
                                    height: StyleSheet.hairlineWidth,
                                    backgroundColor: colorScheme === 'light' ? '#00000010' : '#FFFFFF10',
                                }}
                            />
                        )}
                        renderItem={({ item }) => {
                            const selected = item.value === currentValue;
                            return (
                                <TouchableOpacity
                                    accessibilityRole="menuitem"
                                    onPress={() => handleSelect(item.value)}
                                    style={styles.optionRow}
                                    activeOpacity={0.7}
                                >
                                    <Text
                                        style={[
                                            styles.optionLabel,
                                            {
                                                color: selected ? palette.highlight1 : palette.text,
                                                fontFamily,
                                                fontWeight: selected ? '600' : '400',
                                            },
                                        ]}
                                    >
                                        {item.label}
                                    </Text>
                                    {selected && (
                                        <Ionicons name="checkmark" size={18} color={palette.highlight1} />
                                    )}
                                </TouchableOpacity>
                            );
                        }}
                    />
                </View>
            </Modal>
        </>
    );
}

const styles = StyleSheet.create({
    trigger: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        paddingHorizontal: Spacing.padding,
        paddingVertical: 12,
        borderRadius: Spacing.borderRadius,
        borderWidth: 2,
    },
    chevron: {
        transform: [{ rotate: '0deg' }],
    },
    chevronOpen: {
        transform: [{ rotate: '180deg' }],
    },
    label: {
        flex: 1,
        fontSize: Typography.sizes.general,
    },
    backdrop: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.35)',
    },
    sheet: {
        position: 'absolute',
        left: 8,
        right: 8,
        bottom: 8,
        borderRadius: Spacing.borderRadius,
        borderWidth: 1,
        maxHeight: '55%',
        overflow: 'hidden',
    },
    sheetHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: Spacing.padding,
        paddingVertical: 12,
    },
    sheetTitle: {
        fontSize: Typography.sizes.title,
    },
    optionRow: {
        paddingHorizontal: Spacing.padding,
        paddingVertical: 14,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
    },
    optionLabel: {
        fontSize: Typography.sizes.general,
    },
});
