import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';
import { ThemeProvider } from '@/contexts/theme-context';
import { Toggle } from './Toggle';

const meta = {
    title: 'Interact/Toggle',
    component: Toggle,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ flex: 1, alignItems: 'flex-start' }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/writing-docs/autodocs
    tags: ['autodocs'],
    args: { onValueChange: fn() },
} satisfies Meta<typeof Toggle>;

export default meta;

type Story = StoryObj<typeof meta>;

export const BasicEnabled: Story = {
    args: {
        isEnabled: true,
    },
};

export const BasicDisabled: Story = {
    args: {
        isEnabled: false
    },
};
