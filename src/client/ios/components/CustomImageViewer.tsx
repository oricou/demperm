import React from 'react';
import ImageViewing from 'react-native-image-viewing';

export interface ImageSource {
  uri: string;
}

export interface CustomImageViewerProps {
  images: ImageSource[];
  visible: boolean;
  onClose: () => void;
  initialIndex?: number;
}

const CustomImageViewer: React.FC<CustomImageViewerProps> = ({
  images,
  visible,
  onClose,
  initialIndex = 0,
}) => {
  return (
    <ImageViewing
      images={images}
      imageIndex={initialIndex}
      visible={visible}
      onRequestClose={onClose}
    />
  );
};

export default CustomImageViewer;
