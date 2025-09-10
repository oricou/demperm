# DemPerm iOS Client

A modern iOS application for participating in democratic processes through a mobile-first interface.

## Overview

DemPerm (Démocratie Permanente) is an iOS client that enables citizens to:
- Browse and search democratic proposals
- View detailed proposal information and voting statistics
- Cast votes on active proposals
- Filter proposals by category and status
- Stay informed about democratic processes

## Features

### 🔐 Authentication
- Mock authentication system (demo credentials: username: "demo", password: "demo")
- Secure login flow with form validation

### 📋 Proposal Management
- Browse all available proposals
- Search proposals by title and description
- Filter by category (Infrastructure, Healthcare, Education, Environment, Economy, Social)
- Filter by status (Active, Passed, Rejected, Pending)
- Real-time voting statistics display

### 🗳️ Voting System
- Cast votes on active proposals (For, Against, Abstain)
- Confirmation dialog to prevent accidental votes
- Visual vote choice indicators
- Vote results with percentage breakdowns

### 📱 Modern iOS Design
- SwiftUI-based interface with iOS design guidelines
- Dark mode support
- Pull-to-refresh functionality
- Responsive layout for iPhone and iPad
- Accessibility features

## Technical Details

### Requirements
- iOS 16.0+
- Xcode 15.0+
- Swift 5.0+

### Architecture
- **SwiftUI** for the user interface
- **MVVM pattern** with ObservableObject for state management
- **NavigationView** for app navigation
- **Mock data** for demonstration purposes

### Project Structure
```
DemPerm/
├── DemPermApp.swift          # App entry point and authentication model
├── ContentView.swift         # Main content view with navigation
├── AuthenticationView.swift  # Login screen
├── ProposalListView.swift    # Proposal browsing and filtering
├── ProposalDetailView.swift  # Detailed proposal view
├── VoteView.swift           # Voting interface
├── Proposal.swift           # Data models and mock data
└── Assets.xcassets/         # App icons and assets
```

## Getting Started

### Installation
1. Clone the repository
2. Navigate to the `ios-client` directory
3. Open `DemPerm.xcodeproj` in Xcode
4. Build and run the project

### Demo Usage
1. Launch the app
2. Use the demo credentials:
   - Username: `demo`
   - Password: `demo`
3. Browse proposals and cast votes on active ones

## Development Features

- **Live Previews** for all SwiftUI views
- **Mock data** with realistic proposals
- **Comprehensive filtering** and search capabilities
- **Responsive design** that adapts to different screen sizes
- **Accessibility support** with VoiceOver compatibility

## Future Enhancements

- [ ] Real API integration
- [ ] Push notifications for new proposals
- [ ] User profile management
- [ ] Proposal creation and submission
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Biometric authentication
- [ ] Offline mode support

## Contributing

This is a demo implementation. For production use, consider:
- Implementing proper authentication and authorization
- Adding network layer for API communication
- Implementing proper error handling
- Adding comprehensive testing
- Security hardening

## License

This project is part of the DemPerm repository and follows the same licensing terms.