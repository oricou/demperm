import { ThemeProvider } from '@/contexts/theme-context';
import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { fn } from 'storybook/test';
import { Comment } from './Comment';

const meta = {
    title: 'Social/Comment',
    component: Comment,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ flex: 1 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    tags: ['autodocs'],
    args: {
        onPressLike: fn(),
        onPressComment: fn(),
        onPressUser: fn(),
    },
} satisfies Meta<typeof Comment>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {
        username: 'Jean Dupont',
        avatarUri: 'https://i.pravatar.cc/150?img=12',
        createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // Il y a 2 heures
        text: 'Merci pour ce partage ! C\'est très intéressant et bien expliqué.',
        likeCount: 5,
        commentCount: 2,
        level: 0,
        liked: false,
    },
};

export const Liked: Story = {
    args: {
        username: 'Marie Martin',
        avatarUri: 'https://i.pravatar.cc/150?img=5',
        createdAt: new Date(Date.now() - 30 * 60 * 1000), // Il y a 30 minutes
        text: 'Totalement d\'accord avec vous !',
        likeCount: 12,
        commentCount: 0,
        level: 0,
        liked: true,
    },
};

export const LongComment: Story = {
    args: {
        username: 'Pierre Dubois',
        avatarUri: 'https://i.pravatar.cc/150?img=33',
        createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // Il y a 1 jour
        text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
        likeCount: 8,
        commentCount: 3,
        level: 0,
        liked: false,
    },
};

export const OneWeekAgo: Story = {
    args: {
        username: 'Sophie Laurent',
        avatarUri: 'https://i.pravatar.cc/150?img=9',
        createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // Il y a 1 semaine
        text: 'Super initiative ! J\'espère que ça va continuer.',
        likeCount: 15,
        commentCount: 5,
        level: 0,
        liked: false,
    },
};

export const OneMonthAgo: Story = {
    args: {
        username: 'Luc Bernard',
        avatarUri: 'https://i.pravatar.cc/150?img=11',
        createdAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // Il y a 1 mois
        text: 'Excellente analyse de la situation.',
        likeCount: 20,
        commentCount: 8,
        level: 0,
        liked: false,
    },
};

export const OneYearAgo: Story = {
    args: {
        username: 'Julie Petit',
        avatarUri: 'https://i.pravatar.cc/150?img=16',
        createdAt: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000), // Il y a 1 an
        text: 'Ce sujet est toujours d\'actualité !',
        likeCount: 50,
        commentCount: 15,
        level: 0,
        liked: false,
    },
};

export const Nested: Story = {
    args: {
        username: 'Antoine Moreau',
        avatarUri: 'https://i.pravatar.cc/150?img=68',
        createdAt: new Date(Date.now() - 3 * 60 * 60 * 1000), // Il y a 3 heures
        text: 'Réponse à un autre commentaire',
        likeCount: 3,
        commentCount: 1,
        level: 1,
        liked: false,
    },
};

export const DeepNested: Story = {
    args: {
        username: 'Camille Robert',
        avatarUri: 'https://i.pravatar.cc/150?img=20',
        createdAt: new Date(Date.now() - 1 * 60 * 60 * 1000), // Il y a 1 heure
        text: 'Encore plus profond dans la discussion',
        likeCount: 1,
        commentCount: 0,
        level: 2,
        liked: false,
    },
};

export const NoAvatar: Story = {
    args: {
        username: 'Utilisateur Anonyme',
        createdAt: new Date(Date.now() - 5 * 60 * 1000), // Il y a 5 minutes
        text: 'Commentaire sans avatar',
        likeCount: 0,
        commentCount: 0,
        level: 0,
        liked: false,
    },
};
