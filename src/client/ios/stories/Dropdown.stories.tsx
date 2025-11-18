import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { Dropdown } from './Dropdown';

const meta = {
    title: 'Interact/Dropdown',
    component: Dropdown,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ padding: 16 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
} satisfies Meta<typeof Dropdown>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {
        options: [
            { label: 'Agriculture', value: 'agriculture' },
            { label: 'Ecologie', value: 'ecologie' },
            { label: 'Finance', value: 'finance' },
        ],
        defaultValue: '',
        placeholder: 'Choisir un domaine',
    },
};

export const ErrorState: Story = {
    args: {
        options: [
            { label: 'Option A', value: 'a' },
            { label: 'Option B', value: 'b' },
        ],
        error: true,
        placeholder: 'Sélectionnez une option',
    },
};
