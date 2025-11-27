import React, { useState } from "react";
import { View, Text, Image, FlatList, Modal, TouchableOpacity } from "react-native";
import ProfileScreen from "../app/profile";
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
        <Text style={styles.theme}>{post.theme}</Text>
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
          <View style={{ padding: 8 }}>
            <TouchableOpacity onPress={() => setShowProfile(false)}>
              <Text style={{ color: "#007aff", marginBottom: 8 }}>← Retour</Text>
            </TouchableOpacity>
          </View>
          <ProfileScreen />
        </View>
      </Modal>
    </>
  );
};

export default PostComponent;
