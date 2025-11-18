import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';
import { ThemeProvider } from '@/contexts/theme-context';
import { ListItem } from './ListItem';

const meta = {
    title: 'Interact/ListItem',
    component: ListItem,
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
    args: { onPress: fn(), onRemove: fn() },
} satisfies Meta<typeof ListItem>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Basic: Story = {
    args: {
        avatarUrl: 'https://randomuser.me/api/portraits/men/32.jpg',
        username: 'Jean Dupont',
        votes: 128,
    },
};

export const WithRemoveButton: Story = {
    args: {
        avatarUrl: 'https://randomuser.me/api/portraits/women/44.jpg',
        username: 'Marie Curie',
        votes: 230,
        isDeleteVisible: true,
    },
};