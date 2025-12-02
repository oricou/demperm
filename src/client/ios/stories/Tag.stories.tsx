import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { Tag } from './Tag';
import { fn } from 'storybook/test';

const meta = {
    title: 'Interact/Tag',
    component: Tag,
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
    args: { onToggle: fn() },
} satisfies Meta<typeof Tag>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {
        label: 'Filtre',
    },
};

export const WithIcon: Story = {
    args: {
        label: 'Maison',
        icon: 'home',
    },
};

export const Active: Story = {
    args: {
        label: 'Actif',
        defaultToggled: true,
    },
};

export const Large: Story = {
    args: {
        label: 'Grand tag',
        size: 'large',
    },
};

export const Small: Story = {
    args: {
        label: 'Petit tag',
        size: 'small',
    },
};
