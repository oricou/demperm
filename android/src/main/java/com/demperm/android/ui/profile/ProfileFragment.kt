package com.demperm.android.ui.profile

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.demperm.android.databinding.FragmentProfileBinding

class ProfileFragment : Fragment() {

    private var _binding: FragmentProfileBinding? = null
    private val binding get() = _binding!!

    private lateinit var profileViewModel: ProfileViewModel

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        profileViewModel = ViewModelProvider(this)[ProfileViewModel::class.java]

        _binding = FragmentProfileBinding.inflate(inflater, container, false)
        val root: View = binding.root

        setupClickListeners()
        observeViewModel()

        return root
    }

    private fun setupClickListeners() {
        binding.apply {
            buttonLogin.setOnClickListener {
                val username = editTextUsername.text.toString()
                val email = editTextEmail.text.toString()
                if (username.isNotBlank() && email.isNotBlank()) {
                    profileViewModel.login(username, email)
                } else {
                    Toast.makeText(context, "Please fill in all fields", Toast.LENGTH_SHORT).show()
                }
            }
            
            buttonLogout.setOnClickListener {
                profileViewModel.logout()
            }
        }
    }

    private fun observeViewModel() {
        profileViewModel.user.observe(viewLifecycleOwner) { user ->
            user?.let {
                if (it.isLoggedIn) {
                    binding.layoutLoggedIn.visibility = View.VISIBLE
                    binding.layoutLogin.visibility = View.GONE
                    binding.textLoggedInUsername.text = "Username: ${it.username}"
                    binding.textLoggedInEmail.text = "Email: ${it.email}"
                } else {
                    binding.layoutLoggedIn.visibility = View.GONE
                    binding.layoutLogin.visibility = View.VISIBLE
                }
            }
        }

        profileViewModel.loginSuccess.observe(viewLifecycleOwner) { success ->
            if (success) {
                Toast.makeText(context, "Login successful!", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(context, "Login failed", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}