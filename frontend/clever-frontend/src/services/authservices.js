import api from "./api"

export const register = (userData) => {
    return api.post(
        "/accounts/register/",
        userData
    )
}

export const login = (credentials) => {
    return api.post(
        "/accounts/login/",
        credentials
    )
}

export const getProfile = () => {
    return api.get(
        "/accounts/profile/"
    )
}

export const updateProfile = (userData) => {
    return api.patch(
        "/accounts/profile/",
        userData
    )
}

export const changePassword = (passwordData) => {
    return api.patch(
        "/accounts/change-password/",
        passwordData
    )
}

export const logout = () => {
    return api.post(
        "/accounts/logout/"
    )
}