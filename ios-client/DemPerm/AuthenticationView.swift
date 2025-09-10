import SwiftUI

struct AuthenticationView: View {
    @EnvironmentObject var authViewModel: AuthenticationViewModel
    @State private var username = ""
    @State private var password = ""
    @State private var showingAlert = false
    
    var body: some View {
        VStack(spacing: 30) {
            Spacer()
            
            VStack(spacing: 20) {
                Image(systemName: "person.crop.circle.badge.checkmark")
                    .font(.system(size: 80))
                    .foregroundColor(.blue)
                
                Text("DemPerm")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(.primary)
                
                Text("Démocratie Permanente")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            
            VStack(spacing: 20) {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Username")
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    TextField("Enter your username", text: $username)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                }
                
                VStack(alignment: .leading, spacing: 8) {
                    Text("Password")
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    SecureField("Enter your password", text: $password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                
                Button(action: {
                    if username.isEmpty || password.isEmpty {
                        showingAlert = true
                    } else {
                        authViewModel.login(username: username, password: password)
                    }
                }) {
                    Text("Sign In")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .cornerRadius(10)
                }
                .disabled(username.isEmpty || password.isEmpty)
            }
            .padding(.horizontal, 20)
            
            Spacer()
            
            VStack(spacing: 10) {
                Text("Demo Account")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text("Username: demo")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text("Password: demo")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding(.bottom, 20)
        }
        .alert("Invalid Credentials", isPresented: $showingAlert) {
            Button("OK", role: .cancel) { }
        } message: {
            Text("Please enter both username and password")
        }
        .navigationBarHidden(true)
    }
}

#Preview {
    AuthenticationView()
        .environmentObject(AuthenticationViewModel())
}