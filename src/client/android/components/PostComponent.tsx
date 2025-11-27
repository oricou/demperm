import React, { useState } from "react";
import { View, Text, Image, FlatList, Modal, TouchableOpacity } from "react-native";
import ProfileScreen from "../app/profile";
import ThemePage from "../app/messagerie_debat/theme";
import TopBar from "./TopBar";
import BottomBar from "./BottomBar";
import { theme1, theme2, theme3, theme4, theme5, theme6 } from "@/public/exemples/exemples_theme";
import Post from "../types/post";
import styles from "../styles/post_style";
import CommentComponent from "./CommentComponent";
import ProfileAvatar from "./ProfilePicture";

type Props = {
  post: Post;
};

//TO DO afficher une image help
// Cette page affiche un post avec ses informations
const PostComponent: React.FC<Props> = ({ post }) => {
  const [showProfile, setShowProfile] = useState(false);
  const [showTheme, setShowTheme] = useState(false);

  const availableThemes = [theme1, theme2, theme3, theme4, theme5, theme6];
  const getThemeForPost = () => {
    // try to find a theme with matching name or uuid
    const byName = availableThemes.find((t) => t.name === post.theme);
    if (byName) return byName;
    const byUuid = availableThemes.find((t) => t.uuid === post.theme);
    if (byUuid) return byUuid;
    // fallback: build a minimal theme using the post's theme string as name
    return {
      uuid: `theme-fallback-${post.theme}`,
      name: post.theme,
      description: "",
      likes: 0,
      posts: [post],
    } as any;
  };

  const handleReply = (commentId: string) => {
    console.log("Reponse au commentaire :", commentId);
  };

  return (
    <>
      <View style={styles.container}>
      <View style={styles.headerRow}>
        <View style={styles.leftColumn}>
          <ProfileAvatar size={40} />
          <TouchableOpacity onPress={() => setShowProfile(true)}>
            <Text style={styles.alias}>{post.alias}</Text>
          </TouchableOpacity>
          <Text style={styles.timestamp}>
            {" "}
            {post.timestamp.toLocaleString()}
          </Text>
        </View>
        <TouchableOpacity onPress={() => setShowTheme(true)}>
          <Text style={styles.theme}>{post.theme}</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.title}>{post.title}</Text>
      <Text style={styles.paragraph}>{post.content}</Text>

      <View style={styles.actionsRow}>
        <View style={styles.actionItem}>
          <Image
            source={require("../public/images/like.png")}
            style={styles.actionIcon}
          />
          <Text style={styles.actionText}>{post.likes}</Text>
        </View>
        <View style={styles.actionItem}>
          <Image
            source={require("../public/images/commentaire.png")}
            style={styles.actionIcon}
          />
          <Text style={styles.actionText}>{post.comments.length}</Text>
        </View>
      </View>
      <FlatList
        data={post.comments}
        keyExtractor={(item) => item.uuid}
        renderItem={({ item }) => (
          <CommentComponent comment={item} onReply={handleReply} />
        )}
      />
      <View style={styles.lineSeparator} />
      </View>
      <Modal visible={showProfile} animationType="slide" onRequestClose={() => setShowProfile(false)}>
        <View style={{ flex: 1 }}>
          {/* show app header */}
          <TopBar />

          {/* content area for the profile screen */}
          <View style={{ flex: 1 }}>
            <View style={{ padding: 8 }}>
              <TouchableOpacity onPress={() => setShowProfile(false)}>
                <Text style={{ color: "#007aff", marginBottom: 8 }}>← Retour</Text>
              </TouchableOpacity>
            </View>
            <ProfileScreen />
          </View>

          {/* show app bottom navigation */}
          <BottomBar />
        </View>
      </Modal>

      <Modal visible={showTheme} animationType="slide" onRequestClose={() => setShowTheme(false)}>
        <View style={{ flex: 1 }}>
          {/* show app header */}
          <TopBar />

          {/* content area for the theme page */}
          <View style={{ flex: 1 }}>
            {/* No explicit retour per request — modal shows ThemePage */}
            <ThemePage theme={getThemeForPost()} />
          </View>

          {/* show app bottom navigation */}
          <BottomBar />
        </View>
      </Modal>
    </>
  );
};

export default PostComponent;
