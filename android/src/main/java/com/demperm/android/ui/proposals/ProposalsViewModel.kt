package com.demperm.android.ui.proposals

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.demperm.android.model.Proposal

class ProposalsViewModel : ViewModel() {

    private val _proposals = MutableLiveData<List<Proposal>>()
    val proposals: LiveData<List<Proposal>> = _proposals

    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading

    init {
        loadProposals()
    }

    private fun loadProposals() {
        _isLoading.value = true
        
        // Simulate loading with mock data
        // In a real app, this would be a network call
        val mockProposals = listOf(
            Proposal(
                id = 1,
                title = "Improve Public Transportation",
                description = "Proposal to increase funding for public transportation infrastructure and reduce ticket prices.",
                votesYes = 142,
                votesNo = 38,
                votesAbstain = 12
            ),
            Proposal(
                id = 2,
                title = "Green Energy Initiative",
                description = "Transition to 100% renewable energy sources within the next 10 years.",
                votesYes = 89,
                votesNo = 67,
                votesAbstain = 25
            ),
            Proposal(
                id = 3,
                title = "Education Budget Increase",
                description = "Increase education budget by 15% to improve school facilities and teacher salaries.",
                votesYes = 203,
                votesNo = 45,
                votesAbstain = 18
            )
        )
        
        _proposals.value = mockProposals
        _isLoading.value = false
    }

    fun refreshProposals() {
        loadProposals()
    }
}