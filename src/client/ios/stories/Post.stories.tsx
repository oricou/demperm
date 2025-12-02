import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { Post } from './Post';
import { fn } from 'storybook/test';

const meta = {
    title: 'Feed/Post',
    component: Post,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ padding: 8, backgroundColor: '#EEE' }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    args: {
        username: 'John Doe',
        date: '25 octobre 2025',
        text:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud...',
        likeCount: 412,
        commentCount: 35,
        onPressLike: fn(),
        onPressComment: fn(),
        onPressRepost: fn(),
        onPressShare: fn(),
    },
    tags: ['autodocs'],
} satisfies Meta<typeof Post>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithoutImage: Story = {
    args: {
        images: [],
        level: 0,        // shows bar + bigger gap before card
        liked: false,
    },
};

export const SingleImageLiked: Story = {
    args: {
        images: [
            'https://images.unsplash.com/photo-1502877338535-766e1452684a?w=800',
        ],
        level: 0,
        liked: true,     // heart filled + red
    },
};

export const MultipleImagesUnliked: Story = {
    args: {
        images: [
            'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800',
            'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=400',
            'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400',
            'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=400',
        ],
        level: 3,
        liked: false,
    },
};
