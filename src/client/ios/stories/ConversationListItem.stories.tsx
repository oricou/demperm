// ConversationListItem.stories.tsx
import React from 'react';
import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';

import { ThemeProvider } from '@/contexts/theme-context';
import { ConversationListItem } from './ConversationListItem';
import { SimpleChat } from '@/api/types/chat/simple-chat';
import { SimpleUser } from '@/api/types/common/simple-user';

const baseUser: SimpleUser = {
    displayName: 'John Doe',
} as SimpleUser;

const createChat = (overrides?: Partial<SimpleChat>): SimpleChat => {
    const chat = new SimpleChat();
    chat.id = overrides?.id ?? 1;
    chat.user = (overrides?.user as SimpleUser) ?? baseUser;
    return chat;
};

const defaultChat = createChat();

const meta = {
    title: 'Messages/ConversationListItem',
    component: ConversationListItem,
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
        chat: defaultChat,
    },
} satisfies Meta<typeof ConversationListItem>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const LongUserName: Story = {
    args: {
        chat: createChat({
            id: 2,
            user: {
                ...baseUser,
                displayName: 'Very very long username that will probably wrap',
            } as SimpleUser,
        }),
    },
};

