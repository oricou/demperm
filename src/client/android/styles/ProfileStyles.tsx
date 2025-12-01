import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF',
  },
  lineSeparator: {
    height: 2,
    backgroundColor: '#E0E0E0',
    marginHorizontal: 15,
    marginVertical: 10,
  },
  feedHeaderContainer: {
    paddingHorizontal: 15,
    paddingBottom: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#00008B',
  },
  errorText: {
      fontSize: 16,
      color: '#D00',
      textAlign: 'center',
      padding: 20,
      fontWeight: '500',
  },
});

export default styles;