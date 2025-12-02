import { StyleSheet } from 'react-native';

//Styles pour les thèmes
const theme_style = StyleSheet.create({
    container: {
        padding: 16,
        backgroundColor: '#FFFFFF',
        width: '100%',
    },
    theme_name: {
        fontSize: 20,
        color: '#000091',
        marginBottom: 5,
    },
    theme_description: {
        fontSize: 13,
        color: '#B7C0D6',
        marginBottom: 5,
    },
    themeIcon: {
        width: 72,
        height: 67,
        marginRight: 6,
    },
    themeRow: {
        flexDirection: 'row',
        alignItems: 'flex-start',
        justifyContent: 'space-between',
        marginTop: 8,
    },
    themeTextColumn: {
        flex: 1,
        marginLeft: 8,
    },
    themeItem: {
        flexDirection: 'row',
        alignItems: 'center',
        marginLeft: 12,
    },
    starRow: {
        flexDirection: 'row',
        justifyContent: 'flex-end',
        alignItems: 'center',
        marginTop: 8,
    },
    starItem: {
        flexDirection: 'row',
        alignItems: 'center',
        marginLeft: 12,
    },
    starIcon: {
        width: 18,
        height: 18,
        marginRight: 6,
    },
    starText: {
        fontSize: 14,
        color: '#666',
    },
    starContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginLeft: 8,
    },
}
);


const themes_list_style = StyleSheet.create({
  headerBack: {
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  backText: {
    color: '#00008B',
    fontSize: 16,
  },
});

export { theme_style, themes_list_style };