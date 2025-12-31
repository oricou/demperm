import React, { useEffect, useState } from "react";
import { View, TouchableOpacity, Text } from "react-native";
import styles from "@/styles/submenu_style";

// Module-level flag to avoid rendering more than one SubMenu at a time
let isSubMenuMounted = false;

type Props = {
  tabs: string[];
  onChange?: (index: number) => void;
  /**
   * If true (default), only the first mounted instance will render.
   * Set to false to allow multiple instances (for debugging or special layouts).
   */
  singleInstance?: boolean;
};

const SubMenuComponent: React.FC<Props> = ({ tabs, onChange, singleInstance = true }) => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [shouldRender, setShouldRender] = useState(true);

  useEffect(() => {
    if (singleInstance) {
      if (isSubMenuMounted) {
        // Another instance is already mounted -> don't render this one
        setShouldRender(false);
        return;
      }

      // Mark as mounted
      isSubMenuMounted = true;
      setShouldRender(true);

      return () => {
        // Reset on unmount
        isSubMenuMounted = false;
      };
    }

    // If singleInstance is false, always render
    setShouldRender(true);
    return () => {};
  }, [singleInstance]);

  const handlePress = (index: number) => {
    setActiveIndex(index);
    onChange && onChange(index);
  };

  if (!shouldRender) return null;

  return (
    <View style={styles.container}>
      {tabs.map((tab, index) => (
        <TouchableOpacity
          key={index}
          style={styles.tabContainer}
          onPress={() => handlePress(index)}
        >
          <Text
            style={[
              styles.tabText,
              index === activeIndex ? styles.activeText : styles.inactiveText,
            ]}
          >
            {tab}
          </Text>

          <View
            style={[
              styles.underline,
              index === activeIndex
                ? styles.underlineActive
                : styles.underlineInactive,
            ]}
          />
        </TouchableOpacity>
      ))}
    </View>
  );
};

export default SubMenuComponent;
