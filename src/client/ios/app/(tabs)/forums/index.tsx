import {useThemeContext} from "@/contexts/theme-context";
import {useState} from "react";
import {StyleSheet, View} from "react-native";
import {Colors} from "@/constants/theme";
import {ForumHeader} from "@/components/forum-header";
import ForumsDiscoverScreen from "@/app/(tabs)/forums/forumsDiscover";
import MyForumsScreen from "@/app/(tabs)/forums/myForums";

type TabKey = 'decouvrir' | 'mesForums';

export default function Index() {
    const { colorScheme } = useThemeContext();
    const [tab, setTab] = useState<TabKey>('decouvrir');

    return (
        <View style={[styles.container, { backgroundColor: Colors[colorScheme].background }]}>
            <ForumHeader
                activeTab={tab}
                onTabChange={setTab}
            />
            {tab === "decouvrir" &&
                <ForumsDiscoverScreen/>
            }
            {tab === "mesForums" &&
                <MyForumsScreen/>
            }
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
});