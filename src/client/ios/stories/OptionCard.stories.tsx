import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { OptionCard } from './OptionCard';
import { fn } from 'storybook/test';

const meta = {
    title: 'Interact/OptionCard',
    component: OptionCard,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ flex: 1, alignItems: 'stretch', padding: 16, gap: 8 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
    args: { onValueChange: fn() },
} satisfies Meta<typeof OptionCard>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Basic: Story = {
    args: {
        label: 'Activer les notifications',
        isEnabled: true,
    },
};

export const WithDescription: Story = {
    args: {
        label: 'Mode sombre automatique',
        description: 'Active le thème sombre selon les préférences système.',
        isEnabled: false,
    },
};

export const Disabled: Story = {
    args: {
        label: 'Option désactivée',
        description: 'Cette option ne peut pas être modifiée.',
        isEnabled: false,
        disabled: true,
    },
};
