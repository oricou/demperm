import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  headerContainer: {
    padding: 15,
    backgroundColor: '#FFF',
  },
  profileInfoRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
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
  statsContainer: {
    alignItems: 'flex-start',
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
    fontSize: 16,
    fontWeight: 'bold',
    color: '#00008B',
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statLabel: {
    fontSize: 13,
    color: '#A0A0A0', // Texte en gris
  },
  statCount: {
    fontWeight: 'bold',
    color: '#00008B', // Chiffre en bleu foncé
    fontSize: 14,
  },
});

export default styles;