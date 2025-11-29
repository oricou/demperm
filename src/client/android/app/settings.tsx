import React, { ReactNode, useState } from 'react';
import { View, Text } from 'react-native';
import styles from '@/styles/ProfileStyles';
import { theme_style } from '@/styles/theme_style';
import { Image } from 'react-native';


interface ToggleSwitchProps {
  initial?: boolean;
  onChange?: (value: boolean) => void;
}

const ToggleSwitch: React.FC<ToggleSwitchProps> = ({ initial = false, onChange }) => {
  const [isOn, setIsOn] = useState(initial);

  const toggle = () => {
    const newValue = !isOn;
    setIsOn(newValue);
    onChange?.(newValue);
  };

  const color = isOn ? "#000091" : "#950B02";

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
      <span
        style={{
          fontWeight: "bold",
          color: color,
          minWidth: 40
        }}
      >
        {isOn ? "Public" : "Private"}
      </span>

      <button
        onClick={toggle}
        style={{
          width: 60,
          height: 28,
          borderRadius: 20,
          border: "none",
          background: color,
          position: "relative",
          cursor: "pointer",
          padding: 0
        }}
      >
        <div
          style={{
            width: 23,
            height: 23,
            borderRadius: "50%",
            background: "white",
            position: "absolute",
            top: 3,
            left: isOn ? 35 : 3,
            transition: "left 0.2s ease"
          }}
        ></div>
      </button>
    </div>
  );
};

interface Setting {
  title: string;
  description: string;
  rightComponent?: ReactNode;
  onClick?: () => void;
}

const Setting: React.FC<Setting> = ({
  title,
  description,
  rightComponent,
  onClick
}) => {


  return (
    <div style={{
      width: "100%",
      padding: "12px 16px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      background: "transparent",
      border: "none",
      textAlign: "left",
    }}>
      <Image source={require('@/public/images/theme_icon.png')} style={theme_style.themeIcon} />
      <button
        onClick={onClick}
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          background: "transparent",
          border: "none",
          cursor: "pointer",
          marginLeft: "15vw"
        }}
      >
        <div style={{ flex: 1, textAlign: "justify" }}>
          <div
            style={{
              fontSize: "31px",
              fontWeight: "bold",
              color: "#000091",
              marginBottom: 4
            }}
          >
            {title}
          </div>

          <div style={{ color: "#999", fontSize: "17px" }}>
            {description}
          </div>
        </div>
      </button>
      <div
        style={{
          marginLeft: 13,
          marginRight: 13,
          display: "flex",
          alignItems: "center",
          flexShrink: 0
        }}
      >
        {rightComponent}
      </div>
    </div>
  );
};

export default function SettingsScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Setting
        title='ParameterName'
        description='Description'
      />
      <Setting
        title='Limite de voix'
        description=''
        rightComponent=<Text style={{ fontSize: 23 }}>100</Text>
      />
      <Setting
        title='Anonymat'
        description='Définit votre visibilité'
        rightComponent=<ToggleSwitch initial={false}></ToggleSwitch>
      />
      <Setting
        title='Déconnexion'
        description='Met fin à votre session'
      />

      <View style={styles.lineSeparator} />

      <Text style={{ fontSize: 19, color: "#999" }}>Assistance clientèle</Text>
      <Text style={{ fontSize: 19, color: "#999" }}>Politique de la communauté</Text>
      <Text style={{ fontSize: 19, color: "#999" }}>Politique de confidentialité</Text>
      <Text style={{ fontSize: 19, color: "#999" }}>Conditions générales d'utilisations de DemPerm</Text>
      <Text style={{ fontSize: 19, color: "#999" }}>Version 0.0</Text>
    </View>
  );
}