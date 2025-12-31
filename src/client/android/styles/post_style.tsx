import { StyleSheet } from 'react-native';

//Styles pour les posts et commentaires
const styles = StyleSheet.create({
    container: {
        padding: 16,
        backgroundColor: '#FFFFFF',
    },
    replyContainer: {
        marginLeft: 20,
        borderLeftWidth: 3,
        borderLeftColor: '#ccc',
        paddingLeft: 12,
        paddingVertical: 4,
        marginBottom: 12,
    },
    alias: {
        fontSize: 10,
        color: '#EF4135',
        marginBottom: 5,
        textDecorationLine: 'underline',
    },
    timestamp: {
        fontSize: 10,
        color: '#b7c0d6',
        marginLeft: 6,
        marginBottom: 5,
    },
    headerRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8,
    },
    leftColumn: {
        flexDirection: 'row',
        alignItems: 'center',
        flex: 1,
    },
    theme: {
        fontSize: 14,
        color: '#EF4135',
        marginBottom: 5,
        marginLeft: 8,
    },
    title: {
        fontSize: 20,
        fontWeight: '700',
        marginBottom: 8,
        color: '#0055A4',
    },
    
    paragraph: {
        fontSize: 16,
        marginBottom: 8,
        color: '#b7c0d6',
    },
    actionsRow: {
        flexDirection: 'row',
        justifyContent: 'flex-end',
        alignItems: 'center',
        marginTop: 8,
    },
    actionItem: {
        flexDirection: 'row',
        alignItems: 'center',
        marginLeft: 12,
    },
    actionIcon: {
        width: 18,
        height: 18,
        marginRight: 6,
    },
    actionText: {
        fontSize: 14,
        color: '#666',
    },
    lineSeparator: {
        height: 2,
        backgroundColor: '#ccc',
        marginHorizontal: 1,
    },
    showRepliesButton: {
        marginTop: 12,
        flexDirection: 'row',
        alignItems: 'center',
    },
    showRepliesText: {
        fontSize: 12,
        fontWeight: '600',
        color: '#666',
        marginLeft: 8,
    },
    separatorLine: {
        width: 20,
        height: 1,
        backgroundColor: '#ccc',
    }
}
);

export default styles;
