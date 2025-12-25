import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    borderColor: "#c2cce0",
    borderWidth: 1,
    borderRadius: 40,
    paddingHorizontal: 20,
    paddingVertical: 6,
    backgroundColor: "white",
    marginVertical: 5,
    marginHorizontal: 10,
  },
  input: {
    flex: 1,
    fontSize: 18,
    color: "#1b2c74",
  },
  icon: {
    width: 14,
    height: 14,
    tintColor: "#1b2c74",
    marginLeft: 10,
  },
});

export default styles;
