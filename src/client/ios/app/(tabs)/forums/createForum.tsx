import { CreateForumDto } from "@/api/dtos/forum.dto";
import { domainsService } from "@/api/services/domains.service";
import { Domain } from "@/api/types/forum/domain";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Colors, Spacing, Typography } from "@/constants/theme";
import { useTheme } from "@/hooks/use-theme";
import { Button } from "@/stories/Button";
import { Dropdown, DropdownOption } from "@/stories/Dropdown";
import { InputBar } from "@/stories/InputBar";
import { useLocalSearchParams, useRouter } from "expo-router";
import React, { useEffect, useState } from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function CreateForumScreen() {
  const router = useRouter();
  const { colorScheme } = useTheme();
  const insets = useSafeAreaInsets();
  const params = useLocalSearchParams();

  const [domains, setDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<string>("");
  const [forumName, setForumName] = useState("");
  const [forumDescription, setForumDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);


  useEffect(() => {
    // Charger les domaines au montage du composant
    const fetchDomains = async () => {
      const loadedDomains = await domainsService.getDomains();
      console.log("Domaines chargés:", loadedDomains);
      setDomains(loadedDomains);
    };

    if (params.domainId) {
      setSelectedDomain(params.domainId as string);
    } else {
      fetchDomains();
    }
  }, [params.domainId]);

  const handleCreateForum = () => {
    if (isLoading) return; 
    setIsLoading(true);
    if (params.domainId) {
      const dto: CreateForumDto = {
        name: forumName,
        description: forumDescription,
      };

      domainsService.createSubforum(selectedDomain, dto).then(() => {
        // Après la création, retourner à la page mes forums
        router.back();
      });
    }
    else {
      // TODO
    }
    setIsLoading(false);
    // const formdata :CreateForumDto = {
    //     name: forumName,
    //     description: forumDescription
    // };

    // forumsService.createForum(formdata).then(() => {
    //     // Après la création, retourner à la page mes forums
    //     router.back();
    // }
  };

  // Convertir les domaines en options pour le Dropdown
  const domainOptions: DropdownOption[] = domains.map((domain) => ({
    label: domain.name,
    value: domain.id.toString(),
  }));

  return (
    <ThemedView style={styles.container}>
      {/* Header avec bouton retour */}
      <View
        style={[
          styles.header,
          {
            backgroundColor:
              colorScheme === "light"
                ? Colors.light.background
                : Colors.dark.background,
            paddingTop: insets.top + Spacing.padding,
          },
        ]}
      >
        <Button
          backgroundColor="background"
          icon="chevron-back"
          label=""
          onPress={() => router.back()}
          size="large"
        />
        <ThemedText style={styles.headerTitle}>Créer un forum</ThemedText>
        <View style={styles.headerPlaceholder} />
      </View>

      {/* Contenu du formulaire */}
      <ScrollView
        style={[
          styles.scrollView,
          { backgroundColor: Colors[colorScheme].background },
        ]}
        contentContainerStyle={styles.contentContainer}
      >
        {/* Sélectionner un domaine */}
        {!params.domainId && (
          <View style={styles.fieldContainer}>
            <ThemedText style={styles.label}>
              Sélectionner un domaine
            </ThemedText>
            <Dropdown
              options={domainOptions}
              value={selectedDomain}
              onChange={setSelectedDomain}
              placeholder="Choisir un domaine"
            />
          </View>
        )}

        {/* Nom du forum */}
        <View style={styles.fieldContainer}>
          <ThemedText style={styles.label}>Nom du forum</ThemedText>
          <InputBar
            hideRightIcon
            onChangeText={setForumName}
            placeholder="Nom ..."
            value={forumName}
          />
        </View>

        {/* Description du forum */}
        <View style={styles.fieldContainer}>
          <ThemedText style={styles.label}>Description du forum</ThemedText>
          <InputBar
            bigInput
            hideRightIcon
            onChangeText={setForumDescription}
            placeholder="Description..."
            value={forumDescription}
          />
        </View>

        {/* Bouton Créer */}
        <View style={styles.buttonContainer}>
          <Button
            label="Créer le forum"
            onPress={handleCreateForum}
            size="large"
          />
        </View>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: Spacing.padding,
    paddingBottom: Spacing.padding,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.1)",
  },
  headerTitle: {
    fontSize: Typography.sizes.screenTitle,
    fontWeight: Typography.weights.semiBold,
    flex: 1,
    textAlign: "center",
  },
  headerPlaceholder: {
    width: 48,
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    padding: Spacing.padding,
  },
  fieldContainer: {
    marginBottom: Spacing.margin * 2,
  },
  label: {
    fontSize: Typography.sizes.general,
    fontWeight: Typography.weights.semiBold,
    marginBottom: Spacing.margin,
  },
  buttonContainer: {
    marginTop: Spacing.margin * 2,
  },
});
