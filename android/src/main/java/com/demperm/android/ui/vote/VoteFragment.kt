package com.demperm.android.ui.vote

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.demperm.android.databinding.FragmentVoteBinding
import com.demperm.android.model.VoteType

class VoteFragment : Fragment() {

    private var _binding: FragmentVoteBinding? = null
    private val binding get() = _binding!!

    private lateinit var voteViewModel: VoteViewModel

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        voteViewModel = ViewModelProvider(this)[VoteViewModel::class.java]

        _binding = FragmentVoteBinding.inflate(inflater, container, false)
        val root: View = binding.root

        setupClickListeners()
        observeViewModel()

        return root
    }

    private fun setupClickListeners() {
        binding.apply {
            buttonVoteYes.setOnClickListener {
                submitVote(VoteType.YES)
            }
            
            buttonVoteNo.setOnClickListener {
                submitVote(VoteType.NO)
            }
            
            buttonVoteAbstain.setOnClickListener {
                submitVote(VoteType.ABSTAIN)
            }
        }
    }

    private fun submitVote(voteType: VoteType) {
        voteViewModel.submitVote(voteType)
    }

    private fun observeViewModel() {
        voteViewModel.currentProposal.observe(viewLifecycleOwner) { proposal ->
            proposal?.let {
                binding.textCurrentProposalTitle.text = it.title
                binding.textCurrentProposalDescription.text = it.description
            }
        }

        voteViewModel.voteSubmitted.observe(viewLifecycleOwner) { success ->
            if (success) {
                Toast.makeText(context, "Vote submitted successfully!", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(context, "Failed to submit vote", Toast.LENGTH_SHORT).show()
            }
        }

        voteViewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.buttonVoteYes.isEnabled = !isLoading
            binding.buttonVoteNo.isEnabled = !isLoading
            binding.buttonVoteAbstain.isEnabled = !isLoading
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}