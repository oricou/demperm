import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { BottomBar, BottomBarKey } from './BottomBar';
import { fn } from 'storybook/test';

const meta = {
    title: 'Navigation/BottomBar',
    component: BottomBar,
    decorators: [
        (Story) => (
            <ThemeProvider>
                <View style={{ width: 400 }}>
                    <Story />
                </View>
            </ThemeProvider>
        ),
    ],
    args: {
        onTabPress: fn<(key: BottomBarKey) => void>(),
    },
    tags: ['autodocs'],
} satisfies Meta<typeof BottomBar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const ControlledForums: Story = {
    args: { activeTab: 'chatbubbles' },
};
