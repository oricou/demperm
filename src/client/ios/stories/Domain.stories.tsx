import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';
import { ThemeProvider } from '@/contexts/theme-context';
import { Domain } from './Domain';

const meta = {
    title: 'Interact/Domain',
    component: Domain,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ flex: 1, padding: 16 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
    args: { onPress: fn() },
} satisfies Meta<typeof Domain>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Basic: Story = {
    args: {
        icon: 'home',
        label: 'Immobilier',
    },
};

export const Large: Story = {
    args: {
        icon: 'megaphone',
        label: 'Emploi',
        thickness: 32,
    },
};


