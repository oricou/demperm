import Foundation

struct Proposal: Identifiable, Codable {
    let id = UUID()
    let title: String
    let description: String
    let category: ProposalCategory
    let status: ProposalStatus
    let votesFor: Int
    let votesAgainst: Int
    let abstentions: Int
    let deadline: Date
    let author: String
    
    var totalVotes: Int {
        votesFor + votesAgainst + abstentions
    }
    
    var forPercentage: Double {
        guard totalVotes > 0 else { return 0 }
        return Double(votesFor) / Double(totalVotes) * 100
    }
    
    var againstPercentage: Double {
        guard totalVotes > 0 else { return 0 }
        return Double(votesAgainst) / Double(totalVotes) * 100
    }
    
    var abstentionPercentage: Double {
        guard totalVotes > 0 else { return 0 }
        return Double(abstentions) / Double(totalVotes) * 100
    }
}

enum ProposalCategory: String, CaseIterable, Codable {
    case infrastructure = "Infrastructure"
    case healthcare = "Healthcare"
    case education = "Education"
    case environment = "Environment"
    case economy = "Economy"
    case social = "Social"
    
    var color: String {
        switch self {
        case .infrastructure: return "blue"
        case .healthcare: return "red"
        case .education: return "green"
        case .environment: return "mint"
        case .economy: return "orange"
        case .social: return "purple"
        }
    }
}

enum ProposalStatus: String, CaseIterable, Codable {
    case active = "Active"
    case passed = "Passed"
    case rejected = "Rejected"
    case pending = "Pending"
}

enum VoteChoice: String, CaseIterable {
    case `for` = "For"
    case against = "Against"
    case abstain = "Abstain"
    
    var color: String {
        switch self {
        case .for: return "green"
        case .against: return "red"
        case .abstain: return "gray"
        }
    }
}

// Mock data for development
extension Proposal {
    static let sampleProposals = [
        Proposal(
            title: "New Public Transportation System",
            description: "Proposal to implement a comprehensive public transportation network including electric buses and light rail connections to reduce carbon emissions and improve accessibility.",
            category: .infrastructure,
            status: .active,
            votesFor: 1250,
            votesAgainst: 320,
            abstentions: 180,
            deadline: Calendar.current.date(byAdding: .day, value: 7, to: Date()) ?? Date(),
            author: "City Planning Committee"
        ),
        Proposal(
            title: "Universal Healthcare Coverage",
            description: "Implementation of universal healthcare coverage for all citizens, including preventive care, mental health services, and prescription drug coverage.",
            category: .healthcare,
            status: .active,
            votesFor: 2100,
            votesAgainst: 890,
            abstentions: 210,
            deadline: Calendar.current.date(byAdding: .day, value: 14, to: Date()) ?? Date(),
            author: "Healthcare Reform Coalition"
        ),
        Proposal(
            title: "Renewable Energy Initiative",
            description: "Transition to 100% renewable energy sources within 10 years, including solar, wind, and hydroelectric power infrastructure investments.",
            category: .environment,
            status: .active,
            votesFor: 1890,
            votesAgainst: 456,
            abstentions: 154,
            deadline: Calendar.current.date(byAdding: .day, value: 21, to: Date()) ?? Date(),
            author: "Environmental Action Group"
        ),
        Proposal(
            title: "Education Technology Upgrade",
            description: "Modernize educational infrastructure with new technology, including tablets for students, high-speed internet, and digital learning platforms.",
            category: .education,
            status: .passed,
            votesFor: 1650,
            votesAgainst: 280,
            abstentions: 70,
            deadline: Calendar.current.date(byAdding: .day, value: -3, to: Date()) ?? Date(),
            author: "Education Board"
        ),
        Proposal(
            title: "Minimum Wage Increase",
            description: "Increase the minimum wage to $20/hour to address cost of living increases and ensure a living wage for all workers.",
            category: .economy,
            status: .active,
            votesFor: 1420,
            votesAgainst: 1180,
            abstentions: 300,
            deadline: Calendar.current.date(byAdding: .day, value: 10, to: Date()) ?? Date(),
            author: "Workers' Rights Alliance"
        )
    ]
}