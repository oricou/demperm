package com.demperm.android.ui.proposals

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.demperm.android.databinding.ItemProposalBinding
import com.demperm.android.model.Proposal

class ProposalsAdapter(
    private val onProposalClick: (Proposal) -> Unit
) : ListAdapter<Proposal, ProposalsAdapter.ProposalViewHolder>(ProposalDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProposalViewHolder {
        val binding = ItemProposalBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ProposalViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProposalViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ProposalViewHolder(
        private val binding: ItemProposalBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(proposal: Proposal) {
            binding.apply {
                textProposalTitle.text = proposal.title
                textProposalDescription.text = proposal.description
                textVotesYes.text = "Yes: ${proposal.votesYes}"
                textVotesNo.text = "No: ${proposal.votesNo}"
                textVotesAbstain.text = "Abstain: ${proposal.votesAbstain}"
                
                root.setOnClickListener {
                    onProposalClick(proposal)
                }
            }
        }
    }

    private class ProposalDiffCallback : DiffUtil.ItemCallback<Proposal>() {
        override fun areItemsTheSame(oldItem: Proposal, newItem: Proposal): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: Proposal, newItem: Proposal): Boolean {
            return oldItem == newItem
        }
    }
}