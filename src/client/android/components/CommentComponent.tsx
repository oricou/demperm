//Probablement inutile, je peux re utiliser le component PostComponent pour les comments


/*import React, { useState } from "react";
import { View, Text, Image, FlatList, TouchableOpacity } from "react-native";
import Comment from "@/types/post";
import styles from "@/styles/post_style";
import ProfileAvatar from "./ProfilePicture";

type Props = {
  post: Comment;
  isReply?: boolean;
  onReply: (commentId: string) => void;
};

const CommentComponent: React.FC<Props> = ({
  comment,
  isReply = false,
  onReply,
}) => {
  const [showReplies, setShowReplies] = useState(false);

  const hasAnswers = comment.answers && comment.answers.length > 0;

  return (
    <View style={[styles.container, isReply && styles.replyContainer]}>
      <View style={styles.headerRow}>
        <View style={styles.leftColumn}>
          <ProfileAvatar size={30} />
          <Text style={styles.alias}>{comment.alias}</Text>
          <Text style={styles.timestamp}>
            {" "}
            {comment.timestamp.toLocaleString()}
          </Text>
        </View>
      </View>

      <Text style={styles.paragraph}>{comment.content}</Text>

      <View style={styles.actionsRow}>
        <View style={styles.actionItem}>
          <Image
            source={require("@/public/images/like.png")}
            style={styles.actionIcon}
          />
          <Text style={styles.actionText}>{comment.likes}</Text>
        </View>

        <TouchableOpacity
          style={styles.actionItem}
          onPress={() => onReply(comment.uuid)}
        >
          <Image
            source={require("@/public/images/commentaire.png")}
            style={styles.actionIcon}
          />
          <Text style={styles.actionText}>{comment.answers.length}</Text>
        </TouchableOpacity>
      </View>
      {hasAnswers && (
        <TouchableOpacity
          onPress={() => setShowReplies(!showReplies)}
          style={styles.showRepliesButton}
        >
          <View style={styles.separatorLine} />
          <Text style={styles.showRepliesText}>
            {showReplies
              ? "Masquer les réponses"
              : `Afficher les ${comment.answers.length} réponses`}
          </Text>
        </TouchableOpacity>
      )}

      {showReplies && (
        <FlatList
          data={comment.answers}
          keyExtractor={(item) => item.uuid}
          style={{ marginTop: 8 }}
          renderItem={({ item }) => (
            <CommentComponent comment={item} isReply={true} onReply={onReply} />
          )}
        />
      )}
    </View>
  );
};

export default CommentComponent;
*/