import { defineStore } from "pinia"

import {
    register,
    login,
    getProfile,
    updateProfile,
    changePassword,
    logout
} from "../services/authservices"

export const useAuthStore = defineStore(
    "auth",
    {
        state: () => ({
            user: JSON.parse(
                localStorage.getItem("user")
            ) || null,

            token: localStorage.getItem("token"),

            loading: false,

            error: null
        }),

        getters: {

            isAuthenticated: (state) => {
                return !!state.token
            },

            isAdmin: (state) => {
                return state.user?.is_staff === true
            }
        },

        actions: {

            async registerUser(userData) {

                this.loading = true
                this.error = null

                try {

                    const response = await register(
                        userData
                    )

                    this.setAuthentication(
                        response.data
                    )

                    return response.data

                } catch (error) {

                    this.error =
                        error.response?.data

                    throw error

                } finally {

                    this.loading = false
                }
            },

            async loginUser(email, password) {

                this.loading = true
                this.error = null

                try {

                    const response = await login({
                        email,
                        password
                    })

                    this.setAuthentication(
                        response.data
                    )

                    return response.data

                } catch (error) {

                    this.error =
                        error.response?.data

                    throw error

                } finally {

                    this.loading = false
                }
            },

            setAuthentication(data) {

                this.token = data.token
                this.user = data.user

                localStorage.setItem(
                    "token",
                    data.token
                )

                localStorage.setItem(
                    "user",
                    JSON.stringify(
                        data.user
                    )
                )
            },

            async fetchProfile() {

                if (!this.token) {
                    return null
                }

                try {

                    const response =
                        await getProfile()

                    this.user =
                        response.data

                    localStorage.setItem(
                        "user",
                        JSON.stringify(
                            response.data
                        )
                    )

                    return response.data

                } catch (error) {

                    if (
                        error.response?.status === 401
                    ) {
                        this.clearAuthentication()
                    }

                    throw error
                }
            },

            async updateUserProfile(userData) {

                const response =
                    await updateProfile(
                        userData
                    )

                this.user =
                    response.data

                localStorage.setItem(
                    "user",
                    JSON.stringify(
                        response.data
                    )
                )

                return response.data
            },

            async changeUserPassword(
                passwordData
            ) {

                const response =
                    await changePassword(
                        passwordData
                    )

                if (response.data.token) {

                    this.token =
                        response.data.token

                    localStorage.setItem(
                        "token",
                        response.data.token
                    )
                }

                return response.data
            },

            async logoutUser() {

                try {

                    if (this.token) {
                        await logout()
                    }

                } finally {

                    this.clearAuthentication()
                }
            },

            clearAuthentication() {

                this.token = null
                this.user = null

                localStorage.removeItem(
                    "token"
                )

                localStorage.removeItem(
                    "user"
                )
            }
        }
    }
)