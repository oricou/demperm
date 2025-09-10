import SwiftUI

struct ProposalDetailView: View {
    let proposal: Proposal
    @State private var showingVoteView = false
    @State private var userVote: VoteChoice?
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Header Section
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        CategoryTag(category: proposal.category)
                        Spacer()
                        StatusBadge(status: proposal.status)
                    }
                    
                    Text(proposal.title)
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .lineLimit(nil)
                    
                    HStack {
                        Text("By \(proposal.author)")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Spacer()
                        
                        VStack(alignment: .trailing) {
                            Text("Deadline")
                                .font(.caption)
                                .foregroundColor(.secondary)
                            
                            Text(proposal.deadline, style: .date)
                                .font(.subheadline)
                                .fontWeight(.medium)
                        }
                    }
                }
                
                Divider()
                
                // Description Section
                VStack(alignment: .leading, spacing: 12) {
                    Text("Description")
                        .font(.headline)
                    
                    Text(proposal.description)
                        .font(.body)
                        .lineSpacing(4)
                }
                
                Divider()
                
                // Voting Results Section
                VStack(alignment: .leading, spacing: 16) {
                    Text("Voting Results")
                        .font(.headline)
                    
                    if proposal.totalVotes > 0 {
                        VStack(spacing: 12) {
                            // Vote Counts
                            HStack {
                                VStack {
                                    Text("\(proposal.votesFor)")
                                        .font(.title2)
                                        .fontWeight(.bold)
                                        .foregroundColor(.green)
                                    Text("For")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                .frame(maxWidth: .infinity)
                                
                                VStack {
                                    Text("\(proposal.votesAgainst)")
                                        .font(.title2)
                                        .fontWeight(.bold)
                                        .foregroundColor(.red)
                                    Text("Against")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                .frame(maxWidth: .infinity)
                                
                                VStack {
                                    Text("\(proposal.abstentions)")
                                        .font(.title2)
                                        .fontWeight(.bold)
                                        .foregroundColor(.gray)
                                    Text("Abstain")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                .frame(maxWidth: .infinity)
                            }
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(12)
                            
                            // Progress Bar
                            VStack(spacing: 8) {
                                HStack(spacing: 0) {
                                    Rectangle()
                                        .fill(Color.green)
                                        .frame(width: CGFloat(proposal.forPercentage) * 3)
                                    
                                    Rectangle()
                                        .fill(Color.red)
                                        .frame(width: CGFloat(proposal.againstPercentage) * 3)
                                    
                                    Rectangle()
                                        .fill(Color.gray)
                                        .frame(width: CGFloat(proposal.abstentionPercentage) * 3)
                                    
                                    Spacer()
                                }
                                .frame(height: 8)
                                .background(Color(.systemGray6))
                                .cornerRadius(4)
                                
                                HStack {
                                    Text("For: \(String(format: "%.1f", proposal.forPercentage))%")
                                        .font(.caption)
                                        .foregroundColor(.green)
                                    
                                    Spacer()
                                    
                                    Text("Against: \(String(format: "%.1f", proposal.againstPercentage))%")
                                        .font(.caption)
                                        .foregroundColor(.red)
                                    
                                    Spacer()
                                    
                                    Text("Abstain: \(String(format: "%.1f", proposal.abstentionPercentage))%")
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                }
                            }
                            
                            Text("Total votes: \(proposal.totalVotes)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                                .frame(maxWidth: .infinity, alignment: .center)
                        }
                    } else {
                        Text("No votes yet")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .frame(maxWidth: .infinity, alignment: .center)
                            .padding(.vertical, 20)
                    }
                }
                
                // User Vote Section
                if let userVote = userVote {
                    Divider()
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Your Vote")
                            .font(.headline)
                        
                        HStack {
                            Image(systemName: "checkmark.circle.fill")
                                .foregroundColor(.green)
                            
                            Text("You voted: \(userVote.rawValue)")
                                .font(.subheadline)
                                .fontWeight(.medium)
                        }
                        .padding()
                        .background(Color.green.opacity(0.1))
                        .cornerRadius(8)
                    }
                }
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                if proposal.status == .active && userVote == nil {
                    Button("Vote") {
                        showingVoteView = true
                    }
                    .foregroundColor(.blue)
                    .fontWeight(.semibold)
                }
            }
        }
        .sheet(isPresented: $showingVoteView) {
            VoteView(proposal: proposal) { voteChoice in
                userVote = voteChoice
                showingVoteView = false
            }
        }
    }
}

#Preview {
    NavigationView {
        ProposalDetailView(proposal: Proposal.sampleProposals[0])
    }
}