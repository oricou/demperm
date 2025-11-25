import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { Chip } from './Chip';

const meta = {
    title: 'Display/Chip',
    component: Chip,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ flex: 1, alignItems: 'flex-start', padding: 16 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
} satisfies Meta<typeof Chip>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Basic: Story = {
    args: {
        label: 'Basic',
    },
};

export const CustomColor: Story = {
    args: {
        label: 'Lavande',
        backgroundColor: '#CBA6F7',
    },
};

export const WithIcon: Story = {
    args: {
        label: 'Home',
        icon: 'home',
        backgroundColor: '#FFDD87',
    },
};

export const Large: Story = {
    args: {
        label: 'Big Chip',
        size: 'large',
        backgroundColor: '#76E4F7',
    },
};

export const Darker: Story = {
    args: {
        label: 'Deep Blue',
        backgroundColor: '#3478F6',
    },
};
