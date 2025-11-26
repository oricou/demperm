import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    searchBar: {
        height: 40,
        borderColor: '#ccc',
        borderWidth: 1,
        borderRadius: 8,
        paddingHorizontal: 10,
        backgroundColor: '#fff',
        color: '#000091',
    },
    avatar: {
        width: 50,
        height: 50,
        borderRadius: 25,
        marginRight: 12,
    },
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: "#f2f2f2",
    },
    item: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "white",
        padding: 15,
        marginBottom: 12,
        borderRadius: 8,
        elevation: 2,
    },
    title: {
        fontSize: 22,
        fontWeight: "bold",
        marginBottom: 20,
        color: '#000091',
    },
    text: {
        fontSize: 18,
        color: '#000091',
    },
    text_voix: {
        marginLeft: 20, 
        fontSize: 18,
        fontWeight: "bold",
        color: '#B7C0D6',
    },

    searchContainer: {
  flexDirection: "row",
  alignItems: "center",
  backgroundColor: "#fff",
  paddingHorizontal: 10,
  paddingVertical: 8,
  borderRadius: 10,
  marginBottom: 15,
  elevation: 2,
},

    searchIcon: {
        maxWidth: "80%",
        maxHeight: "80%",
        resizeMode: "contain",
        marginRight: 10,
    },
});

export default styles;