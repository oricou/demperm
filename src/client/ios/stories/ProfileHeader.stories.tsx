import type { Meta, StoryObj } from '@storybook/react-native-web-vite';
import { View } from 'react-native';
import { ThemeProvider } from '@/contexts/theme-context';
import { ProfileCard } from './Profilecard';
import { fn } from 'storybook/test';
import { ProfileHeader } from './ProfileHeader';

const meta = {
    title: 'Profile/ProfileHeader',
    component: ProfileHeader,
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
        description:
            'Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas iaculis massa nisl malesuada lacinia integer nunc posuere ut hendrerit semper vel class aptent taciti sociosqu ad litora torquent per conubia nostra inceptos himenaeos orci varius natoque penatibus et magnis dis parturient montes nascetur ridiculus mus donec rhoncus eros lobortis nulla molestie mattis scelerisque maximus eget fermentum odio phasellus non purus est efficitur laoreet mauris pharetra vestibulum fusce dictum risus blandit quis suspendisse aliquet nisi sodales consequat magna ante condimentum neque at luctus nibh finibus facilisis dapibus etiam interdum tortor ligula congue sollicitudin erat viverra ac tincidunt nam porta elementum a enim euismod quam justo lectus commodo augue arcu dignissim velit aliquam imperdiet mollis nullam volutpat porttitor ullamcorper rutrum gravida.',
        votes: 92,
        bannerUri:
            'https://images.unsplash.com/photo-1496024840928-4c417adf211d?q=80&w=1200&auto=format&fit=crop',
        avatarUri:
            'https://images.unsplash.com/photo-1543466835-00a7907e9de1?q=80&w=400&auto=format&fit=crop',
        onPressFollow: fn(),
    },
    tags: ['autodocs'],
} satisfies Meta<typeof ProfileCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
