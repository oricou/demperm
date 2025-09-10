package com.demperm.android.ui.vote

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.demperm.android.model.Proposal
import com.demperm.android.model.VoteType

class VoteViewModel : ViewModel() {

    private val _currentProposal = MutableLiveData<Proposal?>()
    val currentProposal: LiveData<Proposal?> = _currentProposal

    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading

    private val _voteSubmitted = MutableLiveData<Boolean>()
    val voteSubmitted: LiveData<Boolean> = _voteSubmitted

    init {
        loadCurrentProposal()
    }

    private fun loadCurrentProposal() {
        _isLoading.value = true
        
        // Simulate loading current proposal
        // In a real app, this would fetch the active proposal for voting
        val currentProposal = Proposal(
            id = 1,
            title = "Improve Public Transportation",
            description = "Proposal to increase funding for public transportation infrastructure and reduce ticket prices. This initiative aims to make public transport more accessible and environmentally friendly for all citizens.",
            votesYes = 142,
            votesNo = 38,
            votesAbstain = 12
        )
        
        _currentProposal.value = currentProposal
        _isLoading.value = false
    }

    fun submitVote(voteType: VoteType) {
        _isLoading.value = true
        
        // Simulate vote submission
        // In a real app, this would send the vote to the server
        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            _voteSubmitted.value = true
            _isLoading.value = false
        }, 1000)
    }
}