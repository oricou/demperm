import type { Meta, StoryObj } from '@storybook/react-native-web-vite';

import { View } from 'react-native';
import { fn } from 'storybook/test';
import { ThemeProvider } from '@/contexts/theme-context';
import { Button } from './Button';

const meta = {
  title: 'Interact/Button',
  component: Button,
  decorators: [
    (Story) => (
        <ThemeProvider>
            <View style={{ flex: 1, alignItems: 'flex-start' }}>
                <Story />
            </View>
        </ThemeProvider>
    ),
  ],
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/writing-docs/autodocs
  tags: ['autodocs'],
  // Use `fn` to spy on the onPress arg, which will appear in the actions panel once invoked: https://storybook.js.org/docs/essentials/actions#action-args
  args: { onPress: fn() },
} satisfies Meta<typeof Button>;

export default meta;

type Story = StoryObj<typeof meta>;

export const OnlyLabel: Story = {
  args: {
    label: 'Rejoindre',
  },
};

export const LabelWithIcon: Story = {
  args: {
    label: 'Home',
    icon: 'home'
  },
};

export const OnlyIcon: Story = {
    args: {
        icon: 'chatbubbles'
    },
};

export const Large: Story = {
  args: {
    size: 'large',
    label: 'Rejoindre',
  },
};

export const Small: Story = {
  args: {
    size: 'small',
    label: 'Rejoindre',
  },
};
