import { auth } from "./firebase.js";
import { onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

/**
 * Handles automatic redirection based on Firebase Auth State.
 * Prevents users from getting stuck on the login page or accessing protected areas.
 */
export function initRedirects(pageType) {
    onAuthStateChanged(auth, async (user) => {
        if (user && pageType === 'auth') {
            // If authenticated and on login/register -> redirect to dashboard
            window.location.href = "/dashboard";
        } else if (!user && pageType === 'protected') {
            // If logged out and on a protected page -> redirect to login
            window.location.href = "/login";
        }
    });
}