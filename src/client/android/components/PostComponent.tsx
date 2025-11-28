import React, { useEffect, useState } from "react";
import { View, Text, Image, FlatList, Modal, TouchableOpacity } from "react-native";
import ProfileScreen from "../app/profile";
import ThemePage from "../app/messagerie_debat/theme";
import TopBar from "./TopBar";
import BottomBar from "./BottomBar";
import Post from "../types/post";
import styles from "../styles/post_style";
import ProfileAvatar from "./ProfilePicture";
import Theme from '@/types/theme';

type Props = {
  post: Post;
};

//TO DO afficher une image help
// Cette page affiche un post avec ses informations
const PostComponent: React.FC<Props> = ({ post }) => {
  const [showProfile, setShowProfile] = useState(false);
  const [showTheme, setShowTheme] = useState(false);
  const [showPost, setShowPost] = useState(false);

  const [themes, setThemes] = useState<Theme[]>([]);

  useEffect(() => {
    let mounted = true;
    // Fetch forums/themes from backend
    const API = 'http://localhost:8000/api/v1';
    fetch(`${API}/forums/`)
      .then((res) => res.json())
      .then((data) => {
        if (!mounted) return;
        // Backend may return { results: [...] } or an array directly
        const list = Array.isArray(data) ? data : data?.results ?? data?.items ?? [];
        setThemes(list);
      })
      .catch((err) => {
        console.warn('Failed to load themes:', err);
      });

    return () => {
      mounted = false;
    };
  }, []);
  

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
            <Text style={styles.alias}>{post.author_username}</Text>
          </TouchableOpacity>
          <Text style={styles.timestamp}>
            {" "}
            {post.updated_at.toLocaleString()}
          </Text>
        </View>
        <TouchableOpacity onPress={() => setShowTheme(true)}>
          {<Text style={styles.theme}>{post.subforum_id}</Text>}
        </TouchableOpacity>
      </View>

      <Text style={styles.title}>{post.title}</Text>
      <TouchableOpacity onPress={() => setShowPost(true)}>
            <Text style={styles.paragraph}>{post.content}</Text>
          </TouchableOpacity>

      <View style={styles.actionsRow}>
        <View style={styles.actionItem}>
          <Image
            source={require("../public/images/like.png")}
            style={styles.actionIcon}
          />
          <Text style={styles.actionText}>{post.like_count}</Text>
        </View>
        <View style={styles.actionItem}>
          <Image
            source={require("../public/images/commentaire.png")}
            style={styles.actionIcon}
          />
          <Text style={styles.actionText}>{post.comment_count}</Text>
        </View>
      </View>
      {
        // TO DO jsp comment récupérer les commentaires avec le backend
        /*
      <FlatList
        data={post.comments}
        keyExtractor={(item) => item.uuid}
        renderItem={({ item }) => (
          <CommentComponent comment={item} onReply={handleReply} />
        )}
      />
      */}
      <View style={styles.lineSeparator} />
      </View>



      <Modal visible={showProfile} animationType="slide" onRequestClose={() => setShowProfile(false)}>
        <View style={{ flex: 1 }}>
          <TopBar />
          <View style={{ flex: 1 }}>
            <View style={{ padding: 8 }}>
              <TouchableOpacity onPress={() => setShowProfile(false)}>
                <Text style={{ color: "#007aff", marginBottom: 8 }}>← Retour</Text>
              </TouchableOpacity>
            </View>
            <ProfileScreen />
          </View>
          <BottomBar />
        </View>
      </Modal>



      <Modal visible={showTheme} animationType="slide" onRequestClose={() => setShowTheme(false)}>
        <View style={{ flex: 1 }}>
          <TopBar />
          <View style={{ flex: 1 }}>
            {/*<ThemePage theme={getThemeForPost()} />*/}
          </View>
          <BottomBar />
        </View>
      </Modal>

    <Modal visible={showPost} animationType="slide" onRequestClose={() => setShowPost(false)}>
        <View style={{ flex: 1 }}>
          <TopBar />
          <View style={{ flex: 1 }}>
            <PostComponent post={post} />
          </View>
          <BottomBar />
        </View>
      </Modal>
    </>
  );
};

export default PostComponent;
