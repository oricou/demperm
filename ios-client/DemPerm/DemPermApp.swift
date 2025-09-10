import SwiftUI

@main
struct DemPermApp: App {
    @StateObject private var authenticationViewModel = AuthenticationViewModel()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authenticationViewModel)
        }
    }
}

class AuthenticationViewModel: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: String = ""
    
    func login(username: String, password: String) {
        // Mock authentication - in a real app, this would validate against a server
        if !username.isEmpty && !password.isEmpty {
            isAuthenticated = true
            currentUser = username
        }
    }
    
    func logout() {
        isAuthenticated = false
        currentUser = ""
    }
}