import { domainsService } from "@/api/services/domains.service";
import { forumsService } from "@/api/services/forums.service";
import { subforumsService } from "@/api/services/subforums.service";
import { SimpleForum } from "@/api/types/forum/simple-forum";
import { ThemedView } from "@/components/themed-view";
import { Colors, Spacing, Typography } from "@/constants/theme";
import { useThemeContext } from "@/contexts/theme-context";
import { Button } from "@/stories/Button";
import { Forum } from "@/stories/Forum";
import { InputBar } from "@/stories/InputBar";
import { useFocusEffect, useLocalSearchParams, useRouter } from "expo-router";
import React, { useCallback, useState } from "react";
import {
  ScrollView,
  StyleSheet,
  Text,
  View
} from "react-native";


export default function ThemeForumsScreen() {
  const { colorScheme } = useThemeContext();
  const router = useRouter();
  const params = useLocalSearchParams();
  const [forums, setForums] = useState<SimpleForum[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [domainName, setDomainName] = useState("");

  useFocusEffect(
    useCallback(() => {
      // Récupérer l'ID du domaine depuis les paramètres
      const domainId = params.domainId as string;
      const forumId = params.forumId as string;

      async function loadData() {
        // Charger les forums du domaine
        if (domainId) {
          const loadedForums = await domainsService.getSubforums(domainId);
          setForums(loadedForums);
          const domain = await domainsService.getDomainById(domainId);
          if (domain) {
            setDomainName(domain.name);
          }
        } else if (forumId) {
          const loadedForum = await forumsService.getSubforums(forumId);
          setForums(loadedForum);
          const forum = await subforumsService.getSubforumById(forumId);
          if (forum) {
            setDomainName(forum.title);
          }
        }
      }
      loadData();
    }, [params.domainId, params.forumId])
  );

  const handleForumPress = (forumId: string) => {
    // Navigation vers la page du forum
    console.log("Naviguer vers le forum:", forumId);
    router.push({
      pathname: "/(tabs)/forums/forumHome",
      params: { forumId },
    });
  };

  const handleSearch = () => {
    // Logique de recherche
    console.log("Recherche:", searchQuery);
  };

  const handleCreateForum = () => {
    let _params = {};
    if (params.domainId) {
      _params = { domainId: params.domainId };
    } else if (params.forumId) {
      _params = { forumId: params.forumId };
    }
    router.push({
      pathname: "/(tabs)/forums/createForum",
      params: _params,
    });
  };

  // Filtrer les forums selon la recherche
  const filteredForums = forums.filter(
    (forum) =>
      forum.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      forum.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <ThemedView style={styles.container}>

      {/* Barre de navigation et recherche */}
      <View
        style={[
          styles.navigationBar,
          { backgroundColor: Colors[colorScheme].background },
        ]}
      >
        <Button
          backgroundColor="background"
          icon="chevron-back"
          label=""
          onPress={() => router.back()}
          size="medium"
        />

        <View style={styles.searchContainer}>
          <InputBar
            onActionPress={handleSearch}
            onChangeText={setSearchQuery}
            placeholder={`Rechercher dans ${domainName}`}
            rightIcon="search"
            value={searchQuery}
          />
        </View>
      </View>

      {/* Bouton Créer un forum */}
      <View style={styles.createButtonContainer}>
        <Button
          label="Créer un forum"
          onPress={handleCreateForum}
          size="large"
        />
      </View>

      <ScrollView
        style={[
          styles.scrollView,
          { backgroundColor: Colors[colorScheme].background },
        ]}
      >
        {/* Liste des forums */}
        <ThemedView>
          {filteredForums.length > 0 ? (
            filteredForums.map((forum) => (
              <Forum
                key={forum.id}
                title={forum.title}
                tags={forum.domains.map((domain) => domain.name)}
                onPress={() => handleForumPress(forum.id)}
              />
            ))
          ) : (
            <Text
              style={[styles.emptyText, { color: Colors[colorScheme].text }]}
            >
              Aucun forum trouvé dans ce domaine
            </Text>
          )}
        </ThemedView>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  headerContainer: {
    paddingBottom: Spacing.padding,
  },
  segmentedControlContainer: {
    paddingHorizontal: Spacing.padding,
  },
  segmentedControl: {
    flexDirection: "row",
    borderRadius: Spacing.borderRadius,
    padding: 4,
    gap: 4,
  },
  tab: {
    flex: 1,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  tabText: {
    fontSize: Typography.sizes.general,
    fontWeight: Typography.weights.semiBold,
  },
  tabTextActive: {
    color: "#FFFFFF",
  },
  navigationBar: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: Spacing.padding / 2,
  },
  searchContainer: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  emptyText: {
    textAlign: "center",
    fontSize: Typography.sizes.general,
    marginTop: Spacing.margin * 2,
  },
  createButtonContainer: {
    marginVertical: Spacing.margin,
    marginHorizontal: Spacing.margin,
  },
});
