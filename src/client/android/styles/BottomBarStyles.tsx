import { StyleSheet } from 'react-native';

//Styles pour la bottombar
const styles = StyleSheet.create({
  container: {
    position: 'relative',
    backgroundColor: '#FFFFFF',
    borderTopWidth: 2,
    borderTopColor: '#FF0000',
    paddingTop: 10,
  },
  bump: {
    position: 'absolute',
    top: 0,
    transform: [{ translateY: -20 }],
    width: 120,
    height: 6, 
    marginTop: -7,
    backgroundColor: '#FF0000',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingBottom: 20,
    paddingTop: 10,
  },
  iconContainer: {
    alignItems: 'center',
    padding: 10,
  },
  iconWrapper: {
    padding: 10,
  }
});

export default styles;