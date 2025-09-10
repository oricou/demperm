# DemPerm - Démocratie permanente

A platform for participatory democracy and continuous voting, enabling citizens to participate in democratic decision-making processes.

## Components

### Android Client

The Android client provides a mobile interface for citizens to:
- View active proposals and their descriptions
- Cast votes (Yes/No/Abstain) on proposals
- Manage user profiles and authentication
- See real-time voting results

**Location**: `android/`  
**Documentation**: See [android/README.md](android/README.md) for detailed setup instructions.

**Quick Start**:
```bash
cd android
./gradlew build
./gradlew test
```

## Project Structure

```
demperm/
├── android/              # Android mobile client
│   ├── src/              # Source code
│   ├── build.gradle      # Android dependencies
│   └── README.md         # Android-specific documentation
├── README.md             # This file
├── LICENSE              # GPL-3.0 License
└── .gitignore           # Git ignore rules
```

## Features

- **Democratic Voting**: Citizens can vote on proposals with multiple options
- **Proposal Management**: View active proposals with descriptions and vote counts
- **User Authentication**: Basic user login and profile management
- **Real-time Updates**: Live vote count updates (planned)
- **Mobile-First**: Native Android interface for accessibility

## Technology Stack

- **Android**: Kotlin, Material Design 3, AndroidX
- **Architecture**: MVVM with ViewModel and LiveData
- **UI**: Fragment-based navigation with bottom navigation
- **Testing**: JUnit for unit tests, Espresso for UI tests

## Getting Started

1. Clone the repository
2. Open the `android/` directory in Android Studio
3. Build and run the Android client
4. See component-specific README files for detailed instructions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
