import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';
import { ThemeProvider } from '@/contexts/theme-context';
import { DomainPrev } from './DomainPrev';

const meta = {
    title: 'Interact/DomainPrev',
    component: DomainPrev,
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
} satisfies Meta<typeof     DomainPrev>;

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

