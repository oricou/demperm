import SwiftUI

struct ProposalListView: View {
    @EnvironmentObject var authViewModel: AuthenticationViewModel
    @State private var proposals = Proposal.sampleProposals
    @State private var selectedCategory: ProposalCategory?
    @State private var selectedStatus: ProposalStatus?
    @State private var searchText = ""
    
    var filteredProposals: [Proposal] {
        var filtered = proposals
        
        if let category = selectedCategory {
            filtered = filtered.filter { $0.category == category }
        }
        
        if let status = selectedStatus {
            filtered = filtered.filter { $0.status == status }
        }
        
        if !searchText.isEmpty {
            filtered = filtered.filter { 
                $0.title.localizedCaseInsensitiveContains(searchText) || 
                $0.description.localizedCaseInsensitiveContains(searchText)
            }
        }
        
        return filtered
    }
    
    var body: some View {
        NavigationView {
            VStack {
                // Search and Filter Section
                VStack(spacing: 12) {
                    SearchBar(text: $searchText)
                    
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 10) {
                            FilterChip(
                                title: "All Categories",
                                isSelected: selectedCategory == nil,
                                action: { selectedCategory = nil }
                            )
                            
                            ForEach(ProposalCategory.allCases, id: \.self) { category in
                                FilterChip(
                                    title: category.rawValue,
                                    isSelected: selectedCategory == category,
                                    action: { selectedCategory = selectedCategory == category ? nil : category }
                                )
                            }
                        }
                        .padding(.horizontal)
                    }
                    
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 10) {
                            FilterChip(
                                title: "All Status",
                                isSelected: selectedStatus == nil,
                                action: { selectedStatus = nil }
                            )
                            
                            ForEach(ProposalStatus.allCases, id: \.self) { status in
                                FilterChip(
                                    title: status.rawValue,
                                    isSelected: selectedStatus == status,
                                    action: { selectedStatus = selectedStatus == status ? nil : status }
                                )
                            }
                        }
                        .padding(.horizontal)
                    }
                }
                .padding(.vertical, 8)
                
                // Proposals List
                List(filteredProposals) { proposal in
                    NavigationLink(destination: ProposalDetailView(proposal: proposal)) {
                        ProposalRowView(proposal: proposal)
                    }
                }
                .listStyle(PlainListStyle())
                .refreshable {
                    // In a real app, this would refresh data from the server
                    proposals = Proposal.sampleProposals
                }
            }
            .navigationTitle("DemPerm")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Logout") {
                        authViewModel.logout()
                    }
                }
            }
        }
    }
}

struct SearchBar: View {
    @Binding var text: String
    
    var body: some View {
        HStack {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.secondary)
            
            TextField("Search proposals...", text: $text)
                .textFieldStyle(PlainTextFieldStyle())
            
            if !text.isEmpty {
                Button(action: { text = "" }) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(Color(.systemGray6))
        .cornerRadius(10)
        .padding(.horizontal)
    }
}

struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.caption)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(isSelected ? Color.blue : Color(.systemGray6))
                .foregroundColor(isSelected ? .white : .primary)
                .cornerRadius(16)
        }
    }
}

struct ProposalRowView: View {
    let proposal: Proposal
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(proposal.title)
                    .font(.headline)
                    .lineLimit(2)
                
                Spacer()
                
                StatusBadge(status: proposal.status)
            }
            
            Text(proposal.description)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .lineLimit(2)
            
            HStack {
                CategoryTag(category: proposal.category)
                
                Spacer()
                
                VStack(alignment: .trailing, spacing: 2) {
                    Text("Deadline")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                    
                    Text(proposal.deadline, style: .date)
                        .font(.caption)
                        .foregroundColor(.primary)
                }
            }
            
            // Voting Progress Bar
            if proposal.totalVotes > 0 {
                VStack(alignment: .leading, spacing: 4) {
                    Text("\(proposal.totalVotes) votes")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    HStack(spacing: 0) {
                        Rectangle()
                            .fill(Color.green)
                            .frame(width: CGFloat(proposal.forPercentage) * 2.5)
                        
                        Rectangle()
                            .fill(Color.red)
                            .frame(width: CGFloat(proposal.againstPercentage) * 2.5)
                        
                        Rectangle()
                            .fill(Color.gray)
                            .frame(width: CGFloat(proposal.abstentionPercentage) * 2.5)
                        
                        Spacer()
                    }
                    .frame(height: 4)
                    .background(Color(.systemGray6))
                    .cornerRadius(2)
                }
            }
        }
        .padding(.vertical, 4)
    }
}

struct CategoryTag: View {
    let category: ProposalCategory
    
    var body: some View {
        Text(category.rawValue)
            .font(.caption)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(Color.blue.opacity(0.1))
            .foregroundColor(.blue)
            .cornerRadius(8)
    }
}

struct StatusBadge: View {
    let status: ProposalStatus
    
    var body: some View {
        Text(status.rawValue)
            .font(.caption)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(statusColor.opacity(0.1))
            .foregroundColor(statusColor)
            .cornerRadius(8)
    }
    
    private var statusColor: Color {
        switch status {
        case .active:
            return .green
        case .passed:
            return .blue
        case .rejected:
            return .red
        case .pending:
            return .orange
        }
    }
}

#Preview {
    ProposalListView()
        .environmentObject(AuthenticationViewModel())
}