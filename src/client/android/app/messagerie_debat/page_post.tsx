import React, { useState } from "react";
import { View, FlatList, TouchableOpacity, Text } from "react-native";
import Post from "@/types/post";
import PostComponent from "../../components/PostComponent";


type Props = {
  posts?: Post[];
};


const PostPage: React.FC<Props> = ({ posts }) => {

  const [selectedPost, setselectedPost] = useState<Post | null>(null);
  const data = posts ?? [];

  if (selectedPost) {
    return (
      <View style={{ flex: 1 }}>
        <PostComponent post={selectedPost} />
      </View>
    );
  }


  return (
    <View style={{ flex: 1 }}>

      <FlatList
        data={data}
        keyExtractor={(item) => item.uuid}
        renderItem={({ item }) => (
           <TouchableOpacity onPress={() => setselectedPost(item)}>
          <PostComponent post={item}/>
          </TouchableOpacity>
        )}
        showsVerticalScrollIndicator={false}

      />
    </View>
  );
};

export default PostPage;
