import React, {useCallback, useEffect, useState} from 'react';
import {RefreshControl, ScrollView, StyleSheet} from 'react-native';
import {router, useLocalSearchParams, useRouter} from 'expo-router';

import { ThemedView } from '@/components/themed-view';
import {ProfileHeader} from "@/stories/ProfileHeader";
import {Profile} from "@/api/types/profile/profile";
import {getMyProfile} from "@/api/mock/functions";
import {Post} from "@/stories/Post";
import {Button} from "@/stories/Button";

export default function ProfileScreen() {
    const { id } = useLocalSearchParams<{ id: string }>();
    console.log(id); //FIXME with getting the profile corresponding to the userId

    const [profile, setProfile] = React.useState<Profile>();
    const [refreshing, setRefreshing] = useState(false);

    const handleGetData = () => {
        const profile : Profile|undefined = getMyProfile();
        if (profile)
            setProfile(profile);
    };

    const onRefresh = useCallback(() => {
        setRefreshing(true);
        handleGetData();
        setRefreshing(false);
    }, []);

    const handleMyVotesPress = () => {
        router.navigate("/profile/votes");
    }

    const handleModifyPress = () => {

    }

    const handleSettingsPress = () => {
        router.navigate("/profile/settings");
    }

    const handleNewPostPress = () => {
        router.navigate("/forums/create-post");
    }

    useEffect(() => {
        handleGetData();
    }, [])

    if (!profile) {
        // TODO: Create error screen
        return <></>
    }

    return (
        <>
            <ThemedView>
                <ProfileHeader username={profile.user.displayName}
                               description={profile.bio}
                               votes={profile.voteCount}

                               bannerUri={profile.user.bannerUrl}
                               avatarUri={profile.user.profilePictureUrl}

                               onPressModify={handleModifyPress}
                               onPressMyVotes={handleMyVotesPress}
                               onPressSettings={handleSettingsPress}
                />
            </ThemedView>

            <ThemedView style={styles.container}>
                <ScrollView refreshControl={<RefreshControl
                    refreshing={refreshing} onRefresh={onRefresh} />}>

                    <Button
                        icon="add"
                        label="Nouveau post"
                        onPress={handleNewPostPress}
                        style={styles.createPostButton}
                    />
                    {
                        profile.posts.map(post => {
                            return (
                                <Post username={post.author.displayName}
                                      date={post.createdAt}
                                      text={post.content}
                                      key={post.id}
                                />
                            )
                        })
                    }
                </ScrollView>
            </ThemedView>
        </>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    createPostButton: {
        margin: 8
    }
});