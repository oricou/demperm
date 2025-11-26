import React from "react";
import { View, Text, Image, FlatList } from "react-native";
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
  const handleReply = (commentId: string) => {
    console.log("Reponse au commentaire :", commentId);
  };

  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <View style={styles.leftColumn}>
          <ProfileAvatar size={40} />
          <Text style={styles.alias}>{post.alias}</Text>
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
  );
};

export default PostComponent;
