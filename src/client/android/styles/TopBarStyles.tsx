import Constants from 'expo-constants';
import { StyleSheet } from 'react-native';

//Styles pour la topbar
const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    paddingTop: Constants.statusBarHeight + 10,
    paddingBottom: 10,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#FF0000',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#00008B',
  },
  iconWrapper: {
    padding: 5,
  }
});

export default styles;