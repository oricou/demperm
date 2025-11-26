import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  containerWrapper: {
    position: "relative",
    width: "100%",
  },

  globalUnderline: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    height: 2,
    backgroundColor: "#000091",
    zIndex: 1,
  },

  activeTabUnderline: {
    marginTop: 4,
    width: "100%",
    height: 4,
    backgroundColor: "#000091",
    zIndex: 2,
  },

  container: {
    flexDirection: "row",
    justifyContent: "space-between",
    width: "100%",
    marginTop: 10,
  },

  tabContainer: {
    alignItems: "center",
    minWidth: "45%",
  },

  tabText: {
    fontSize: 22,
    fontWeight: "600",
    color: "#000091",
  },
});

export default styles;
