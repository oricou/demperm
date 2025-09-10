# DemPerm Android Client

Android client for the DemPerm (Démocratie permanente) application - a platform for participatory democracy and continuous voting.

## Features

- **Proposals View**: Browse and view all active proposals with current vote counts
- **Voting Interface**: Cast votes (Yes/No/Abstain) on active proposals  
- **User Profile**: Basic user authentication and profile management
- **Material Design**: Modern Android UI following Material Design guidelines

## Architecture

The app follows Android architecture best practices:

- **MVVM Pattern**: Uses ViewModel and LiveData for reactive UI updates
- **Navigation Component**: Fragment-based navigation with bottom navigation
- **View Binding**: Type-safe view references
- **Material Design Components**: Consistent UI using Material Design 3

## Project Structure

```
android/
├── src/main/
│   ├── java/com/demperm/android/
│   │   ├── MainActivity.kt                 # Main activity with navigation
│   │   ├── model/
│   │   │   └── Models.kt                  # Data models (Proposal, Vote, User)
│   │   └── ui/
│   │       ├── proposals/                 # Proposals listing
│   │       │   ├── ProposalsFragment.kt
│   │       │   ├── ProposalsViewModel.kt
│   │       │   └── ProposalsAdapter.kt
│   │       ├── vote/                      # Voting interface
│   │       │   ├── VoteFragment.kt
│   │       │   └── VoteViewModel.kt
│   │       └── profile/                   # User profile
│   │           ├── ProfileFragment.kt
│   │           └── ProfileViewModel.kt
│   ├── res/
│   │   ├── layout/                        # XML layouts
│   │   ├── values/                        # Strings, colors, themes
│   │   ├── menu/                          # Navigation menu
│   │   └── navigation/                    # Navigation graph
│   └── AndroidManifest.xml
├── build.gradle                          # App dependencies and config
└── proguard-rules.pro                    # ProGuard configuration
```

## Setup and Installation

### Prerequisites

- Android Studio Arctic Fox or later
- Android SDK API level 24 or higher
- Gradle 7.0+
- Java 8+

### Building the Project

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd demperm
   ```

2. Open the `android` directory in Android Studio

3. Build the project:
   ```bash
   cd android
   ./gradlew build
   ```

4. Run tests:
   ```bash
   ./gradlew test
   ```

### Running on Device/Emulator

1. Connect an Android device or start an emulator
2. Run from Android Studio or use:
   ```bash
   ./gradlew installDebug
   ```

## Data Models

### Proposal
```kotlin
data class Proposal(
    val id: Long,
    val title: String,
    val description: String,
    val votesYes: Int,
    val votesNo: Int,
    val votesAbstain: Int,
    val isActive: Boolean,
    val createdAt: Long
)
```

### Vote
```kotlin
data class Vote(
    val id: Long,
    val proposalId: Long,
    val userId: Long,
    val voteType: VoteType,
    val timestamp: Long
)

enum class VoteType { YES, NO, ABSTAIN }
```

### User
```kotlin
data class User(
    val id: Long,
    val username: String,
    val email: String,
    val isLoggedIn: Boolean
)
```

## Current Implementation

This is a **mock implementation** with simulated data and functionality:

- Proposals are loaded from hardcoded mock data
- Voting simulates network calls with delays
- User authentication is basic mock login
- No actual backend integration yet

## Future Enhancements

- Backend API integration
- Real-time vote updates
- Push notifications for new proposals
- Proposal creation interface
- Vote history and analytics
- Multi-language support
- Offline voting capability
- Advanced user authentication (OAuth, etc.)

## Dependencies

- AndroidX libraries for modern Android development
- Material Design Components for UI
- Navigation Component for fragment management
- Lifecycle components (ViewModel, LiveData)
- Retrofit (ready for API integration)

## Contributing

1. Follow Android coding standards
2. Use meaningful commit messages
3. Add tests for new features
4. Update documentation as needed

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.