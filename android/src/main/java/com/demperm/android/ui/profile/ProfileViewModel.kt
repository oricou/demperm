package com.demperm.android.ui.profile

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.demperm.android.model.User

class ProfileViewModel : ViewModel() {

    private val _user = MutableLiveData<User?>()
    val user: LiveData<User?> = _user

    private val _loginSuccess = MutableLiveData<Boolean>()
    val loginSuccess: LiveData<Boolean> = _loginSuccess

    init {
        // Initialize with logged out state
        _user.value = User(
            id = 0,
            username = "",
            email = "",
            isLoggedIn = false
        )
    }

    fun login(username: String, email: String) {
        // Simulate login process
        // In a real app, this would authenticate with a server
        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            val loggedInUser = User(
                id = 1,
                username = username,
                email = email,
                isLoggedIn = true
            )
            
            _user.value = loggedInUser
            _loginSuccess.value = true
        }, 1000)
    }

    fun logout() {
        _user.value = User(
            id = 0,
            username = "",
            email = "",
            isLoggedIn = false
        )
    }
}