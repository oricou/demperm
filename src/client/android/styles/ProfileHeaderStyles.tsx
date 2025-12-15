import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  headerContainer: {
    padding: 15,
    backgroundColor: '#FFF',
  },
  profileInfoRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    // Espace en bas pour séparer de la ligne des actions
    marginBottom: 15, 
  },
  userInfo: {
    flex: 1,
    marginLeft: 15,
    justifyContent: 'center',
  },
  pseudo: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#00008B',
    marginBottom: 2,
  },
  description: {
    fontSize: 14,
    color: '#A0A0A0',
    fontWeight: '500',
  },
    // --- Nouveaux Styles de Structure ---
    statsAndActionsRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingVertical: 5,
    },
    actionButtonsContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        // Permet aux boutons de prendre de la place
        flexShrink: 0, 
    },
    
    // --- Styles des Boutons d'Action ---
    actionButton: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 8,
        paddingHorizontal: 12,
        borderRadius: 20, // Coins arrondis
        marginLeft: 8, // Espace entre les boutons
    },
    secondaryActionButton: {
        backgroundColor: '#E0E0E0', // Fond gris clair pour les actions secondaires (Message, Bloquer)
        borderWidth: 1,
        borderColor: '#CCC',
    },
    actionButtonText: {
        fontSize: 14,
        fontWeight: '600',
        color: '#FFF',
    },
    editButton: {
        backgroundColor: '#E0E0E0',
        borderWidth: 1,
        borderColor: '#CCC',
    },
    
    // --- Styles de l'Étoile et des Stats (Maintenus mais déplacés dans le flux) ---
  statsContainer: {
    alignItems: 'flex-start',
    marginLeft: 10,
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  circleIcon: {
    width: 30,
    height: 30,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#C00',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFF',
  },
  statNumber: {
    marginLeft: 5,
    fontSize: 13, // Rendu un peu plus petit
    fontWeight: 'bold',
    color: '#00008B',
    maxWidth: 60, // Pour éviter que le texte ne prenne trop de place
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    // Retiré du flux principal, utilisé pour followers/following
  },
  statLabel: {
    fontSize: 13,
    color: '#A0A0A0', 
  },
  statCount: {
    fontWeight: 'bold',
    color: '#00008B', 
    fontSize: 14,
  },
});

export default styles;