import React, { useState } from "react";
import { View, FlatList } from "react-native";
import Post from "@/types/post";
import PostComponent from "../../components/PostComponent";


type Props = {
  posts?: Post[];
};


const PostPage: React.FC<Props> = ({ posts }) => {

  // etat pour la recherche
  const [search, setSearch] = useState("");

  // fonction simple de filtre — si pas de posts fournis, on affiche rien
  const filteredPosts = (posts ?? []).filter(
    (post) =>
      post.title.toLowerCase().includes(search.toLowerCase()) ||
      post.content.toLowerCase().includes(search.toLowerCase()) ||
      post.alias.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <View style={{ flex: 1 }}>

      <FlatList
        data={filteredPosts}
        keyExtractor={(item) => item.uuid}
        renderItem={({ item }) => <PostComponent post={item} />}
      />
    </View>
  );
};

export default PostPage;
