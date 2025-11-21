import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';
import { ThemeProvider } from '@/contexts/theme-context';
import {Forum} from "@/stories/Forum";

const meta = {
    title: 'Interact/Forum',
    component: Forum,
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
} satisfies Meta<typeof Forum>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Simple: Story = {
    args: {
        title: 'Mode sombre',
    },
};

export const WithTags: Story = {
    args: {
        title: 'Filtres actifs',
        tags: ['Maison', 'Appartement', 'Studio'],
    },
};