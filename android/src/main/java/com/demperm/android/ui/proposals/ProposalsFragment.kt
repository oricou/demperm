package com.demperm.android.ui.proposals

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.demperm.android.databinding.FragmentProposalsBinding

class ProposalsFragment : Fragment() {

    private var _binding: FragmentProposalsBinding? = null
    private val binding get() = _binding!!

    private lateinit var proposalsViewModel: ProposalsViewModel
    private lateinit var proposalsAdapter: ProposalsAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        proposalsViewModel = ViewModelProvider(this)[ProposalsViewModel::class.java]

        _binding = FragmentProposalsBinding.inflate(inflater, container, false)
        val root: View = binding.root

        setupRecyclerView()
        observeViewModel()

        return root
    }

    private fun setupRecyclerView() {
        proposalsAdapter = ProposalsAdapter { proposal ->
            // Handle proposal click
        }
        binding.recyclerViewProposals.apply {
            layoutManager = LinearLayoutManager(context)
            adapter = proposalsAdapter
        }
    }

    private fun observeViewModel() {
        proposalsViewModel.proposals.observe(viewLifecycleOwner) { proposals ->
            proposalsAdapter.submitList(proposals)
        }

        proposalsViewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}