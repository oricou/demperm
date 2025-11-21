import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { ChatBubble } from './ChatBubble';

const meta = {
    title: 'Messaging/ChatBubble',
    component: ChatBubble,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ paddingVertical: 16, gap: 8 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
} satisfies Meta<typeof ChatBubble>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Other: Story = {
    args: { text: 'Salut ! toi aussi tu est fan de démocratie ?', time: '14:02' },
};

export const Own: Story = {
    args: { text: "Oui oui, j'adore la démocratie", isOwn: true, time: '14:03' },
};
