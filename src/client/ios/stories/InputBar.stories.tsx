import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';
import { ThemeProvider } from '@/contexts/theme-context';
import { InputBar } from './InputBar';

const meta = {
    title: 'Interact/InputBar',
    component: InputBar,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ flex: 1, alignItems: 'stretch', padding: 16 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
    args: {
        onChangeText: fn(),
        onActionPress: fn(),
    },
} satisfies Meta<typeof InputBar>;

export default meta;

type Story = StoryObj<typeof meta>;

// Search mode
export const Search: Story = {
    args: {
        placeholder: 'Rechercher...',
        rightIcon: 'search',
        backgroundColor: 'background',
    },
};

// Chat input
export const Chat: Story = {
    args: {
        placeholder: 'Écrire un message...',
        rightIcon: 'paper-plane'
    },
};

// Blog post input
export const BigPostInput: Story = {
    args: {
        placeholder: 'Description...',
        bigInput: true,
        backgroundColor: 'background',
        hideRightIcon: true
    },
};

// Regular post input
export const NoIcon: Story = {
    args: {
        placeholder: 'Titre',
        hideRightIcon: true,
    },
};
