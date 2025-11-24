import { ThemeProvider } from '@/contexts/theme-context';
import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { Logo } from './Logo';

const meta = {
    title: 'Components/Logo',
    component: Logo,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
    argTypes: {
        width: {
            control: { type: 'number', min: 20, max: 200, step: 10 },
        },
        height: {
            control: { type: 'number', min: 20, max: 200, step: 10 },
        },
    },
    args: {
        width: 40,
        height: 40,
    },
} satisfies Meta<typeof Logo>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {
        width: 40,
        height: 40,
    },
};

export const Large: Story = {
    args: {
        width: 80,
        height: 80,
    },
};

export const Small: Story = {
    args: {
        width: 24,
        height: 24,
    },
};

export const ExtraLarge: Story = {
    args: {
        width: 120,
        height: 120,
    },
};
