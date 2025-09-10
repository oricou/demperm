import SwiftUI

struct VoteView: View {
    let proposal: Proposal
    let onVoteSubmitted: (VoteChoice) -> Void
    
    @State private var selectedVote: VoteChoice?
    @State private var showingConfirmation = false
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        NavigationView {
            VStack(spacing: 30) {
                // Header
                VStack(spacing: 16) {
                    Image(systemName: "checkmark.circle")
                        .font(.system(size: 60))
                        .foregroundColor(.blue)
                    
                    Text("Cast Your Vote")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Text(proposal.title)
                        .font(.headline)
                        .multilineTextAlignment(.center)
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                }
                
                // Vote Options
                VStack(spacing: 16) {
                    ForEach(VoteChoice.allCases, id: \.self) { choice in
                        VoteOptionButton(
                            choice: choice,
                            isSelected: selectedVote == choice,
                            action: {
                                selectedVote = choice
                            }
                        )
                    }
                }
                
                Spacer()
                
                // Vote Description
                if let selectedVote = selectedVote {
                    VStack(spacing: 8) {
                        Text("You are voting: \(selectedVote.rawValue)")
                            .font(.headline)
                            .foregroundColor(.primary)
                        
                        Text(voteDescription(for: selectedVote))
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                }
                
                // Submit Button
                Button(action: {
                    showingConfirmation = true
                }) {
                    Text("Submit Vote")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(selectedVote != nil ? Color.blue : Color.gray)
                        .cornerRadius(12)
                }
                .disabled(selectedVote == nil)
                
                Text("Once submitted, your vote cannot be changed")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding()
            .navigationTitle("Vote")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        presentationMode.wrappedValue.dismiss()
                    }
                }
            }
            .alert("Confirm Your Vote", isPresented: $showingConfirmation) {
                Button("Cancel", role: .cancel) { }
                Button("Submit") {
                    if let vote = selectedVote {
                        onVoteSubmitted(vote)
                    }
                }
            } message: {
                if let selectedVote = selectedVote {
                    Text("You are voting \(selectedVote.rawValue) on this proposal. This action cannot be undone.")
                }
            }
        }
    }
    
    private func voteDescription(for choice: VoteChoice) -> String {
        switch choice {
        case .for:
            return "You support this proposal and want it to be implemented."
        case .against:
            return "You oppose this proposal and don't want it to be implemented."
        case .abstain:
            return "You choose not to take a position on this proposal."
        }
    }
}

struct VoteOptionButton: View {
    let choice: VoteChoice
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Image(systemName: iconName)
                            .font(.title2)
                            .foregroundColor(voteColor)
                        
                        Text(choice.rawValue)
                            .font(.headline)
                            .foregroundColor(.primary)
                        
                        Spacer()
                        
                        if isSelected {
                            Image(systemName: "checkmark.circle.fill")
                                .font(.title2)
                                .foregroundColor(.blue)
                        }
                    }
                    
                    Text(description)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.leading)
                }
                
                Spacer()
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(isSelected ? Color.blue.opacity(0.1) : Color(.systemGray6))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(isSelected ? Color.blue : Color.clear, lineWidth: 2)
                    )
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
    
    private var iconName: String {
        switch choice {
        case .for:
            return "hand.thumbsup"
        case .against:
            return "hand.thumbsdown"
        case .abstain:
            return "minus.circle"
        }
    }
    
    private var voteColor: Color {
        switch choice {
        case .for:
            return .green
        case .against:
            return .red
        case .abstain:
            return .gray
        }
    }
    
    private var description: String {
        switch choice {
        case .for:
            return "Support this proposal"
        case .against:
            return "Oppose this proposal"
        case .abstain:
            return "No position on this proposal"
        }
    }
}

#Preview {
    VoteView(proposal: Proposal.sampleProposals[0]) { _ in }
}