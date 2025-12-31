import {Redirect, router} from 'expo-router';
import {DemocracyHeader} from "@/components/democracy-header";
import {Colors, Spacing} from "@/constants/theme";
import {StyleSheet, View} from "react-native";
import {useThemeContext} from "@/contexts/theme-context";
import {useState} from "react";
import DemocracyRankingScreen from "@/app/(tabs)/democracy/democracyRanking";
import DemocracyNewsScreen from "@/app/(tabs)/democracy/democracyNews";
import DemocracyRetainedScreen from "@/app/(tabs)/democracy/democracyRetained";

type TabKey = 'actualites' | 'classement' | 'retenus';

export default function Index() {
  const { colorScheme } = useThemeContext();
  const [tab, setTab] = useState<TabKey>('actualites');

  return (
      <View style={[styles.container, { backgroundColor: Colors[colorScheme].background }]}>
        <DemocracyHeader
            activeTab={tab}
            onTabChange={setTab}
        />
        {tab === "classement" &&
            <DemocracyRankingScreen/>
        }
        {tab === "actualites" &&
        <DemocracyNewsScreen/>
        }
        {tab === "retenus" &&
        <DemocracyRetainedScreen/>}
      </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});