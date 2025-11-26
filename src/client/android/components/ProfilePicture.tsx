import React from 'react';
import { View} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { FontAwesome } from '@expo/vector-icons';

type Props = {
  size?: number;
};

const ProfileAvatar: React.FC<Props> = ({size = 80 }) => {
  const borderThickness = 3;
  
  const innerSize = size - (borderThickness * 2);

  return (
    <LinearGradient
      colors={['#00008B', '#FFFFFF', '#FF0000']}
      start={{ x: 0, y: 0.5 }}
      end={{ x: 1, y: 0.5 }}
      style={{
        width: size,
        height: size,
        borderRadius: size,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <View
        style={{
          width: innerSize,
          height: innerSize,
          borderRadius: innerSize,
          backgroundColor: '#E0E0E0',
          justifyContent: 'center',
          alignItems: 'center',
          overflow: 'hidden',
          borderWidth: 3,
          borderColor: '#FFF',
        }}
      >
        <FontAwesome name="user" size={innerSize * 0.5} color="#4A4A4A" />
      </View>
    </LinearGradient>
  );
};

export default ProfileAvatar;