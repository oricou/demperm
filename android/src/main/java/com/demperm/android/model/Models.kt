package com.demperm.android.model

data class Proposal(
    val id: Long,
    val title: String,
    val description: String,
    val votesYes: Int = 0,
    val votesNo: Int = 0,
    val votesAbstain: Int = 0,
    val isActive: Boolean = true,
    val createdAt: Long = System.currentTimeMillis()
)

data class Vote(
    val id: Long,
    val proposalId: Long,
    val userId: Long,
    val voteType: VoteType,
    val timestamp: Long = System.currentTimeMillis()
)

enum class VoteType {
    YES, NO, ABSTAIN
}

data class User(
    val id: Long,
    val username: String,
    val email: String,
    val isLoggedIn: Boolean = false
)