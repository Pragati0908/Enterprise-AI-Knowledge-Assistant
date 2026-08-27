"""
===============================================================
Enterprise AI Knowledge Assistant

Authentication Component
===============================================================
"""

import streamlit as st

from api_client import (
    login_user,
    register_user,
    get_current_user
)


# ==============================================================
# Initialize Authentication State
# ==============================================================

def initialize_auth_state():

    # ----------------------------------------------------------
    # Authentication Status
    # ----------------------------------------------------------

    if "authenticated" not in st.session_state:

        st.session_state.authenticated = False


    # ----------------------------------------------------------
    # JWT Access Token
    # ----------------------------------------------------------

    if "access_token" not in st.session_state:

        st.session_state.access_token = None


    # ----------------------------------------------------------
    # Current User Information
    # ----------------------------------------------------------

    if "current_user" not in st.session_state:

        st.session_state.current_user = None


# ==============================================================
# Login Page
# ==============================================================

def render_login():

    # ----------------------------------------------------------
    # Initialize Authentication State
    # ----------------------------------------------------------

    initialize_auth_state()


    # ----------------------------------------------------------
    # Page Title
    # ----------------------------------------------------------

    st.title(
        "🔐 Login"
    )


    # ----------------------------------------------------------
    # Username Input
    # ----------------------------------------------------------

    username = st.text_input(

        "Username",

        key="login_username"

    )


    # ----------------------------------------------------------
    # Password Input
    # ----------------------------------------------------------

    password = st.text_input(

        "Password",

        type="password",

        key="login_password"

    )


    # ----------------------------------------------------------
    # Login Button
    # ----------------------------------------------------------

    if st.button(

        "Login",

        use_container_width=True

    ):

        # ------------------------------------------------------
        # Validate Input
        # ------------------------------------------------------

        if (

            username.strip() == ""

            or

            password.strip() == ""

        ):

            st.warning(

                "Please enter username and password."

            )

            return


        try:

            # ==================================================
            # Call Login API
            # ==================================================

            result = login_user(

                username,

                password

            )


            # ==================================================
            # Store JWT Token
            # ==================================================

            access_token = (

                result[
                    "access_token"
                ]

            )


            st.session_state.access_token = (

                access_token

            )


            # ==================================================
            # Get Current User Information
            # ==================================================

            current_user = get_current_user(

                access_token

            )


            # ==================================================
            # Store Current User
            # ==================================================

            st.session_state.current_user = (

                current_user

            )


            # ==================================================
            # Mark User as Authenticated
            # ==================================================

            st.session_state.authenticated = True


            # ==================================================
            # Success Message
            # ==================================================

            st.success(

                f"Login successful. Welcome "
                f"{current_user['username']}!"

            )


            # ==================================================
            # Reload Application
            # ==================================================

            st.rerun()


        except Exception as error:

            # --------------------------------------------------
            # Reset Authentication State on Failure
            # --------------------------------------------------

            st.session_state.authenticated = False

            st.session_state.access_token = None

            st.session_state.current_user = None


            st.error(

                f"Login failed: {error}"

            )


# ==============================================================
# Registration Page
# ==============================================================

def render_registration():

    # ----------------------------------------------------------
    # Page Title
    # ----------------------------------------------------------

    st.title(
        "📝 Create Account"
    )


    # ----------------------------------------------------------
    # Username Input
    # ----------------------------------------------------------

    username = st.text_input(

        "Username",

        key="register_username"

    )


    # ----------------------------------------------------------
    # Email Input
    # ----------------------------------------------------------

    email = st.text_input(

        "Email",

        key="register_email"

    )


    # ----------------------------------------------------------
    # Password Input
    # ----------------------------------------------------------

    password = st.text_input(

        "Password",

        type="password",

        key="register_password"

    )


    # ----------------------------------------------------------
    # Create Account Button
    # ----------------------------------------------------------

    if st.button(

        "Create Account",

        use_container_width=True

    ):

        # ------------------------------------------------------
        # Validate Input
        # ------------------------------------------------------

        if (

            username.strip() == ""

            or

            email.strip() == ""

            or

            password.strip() == ""

        ):

            st.warning(

                "Please complete all fields."

            )

            return


        try:

            # ==================================================
            # Register User
            # ==================================================

            result = register_user(

                username,

                email,

                password

            )


            # ==================================================
            # Success Message
            # ==================================================

            st.success(

                f"Account created for "
                f"{result['username']}."

            )


            st.info(

                "You can now log in."

            )


        except Exception as error:

            st.error(

                f"Registration failed: {error}"

            )


# ==============================================================
# Authentication Screen
# ==============================================================

def render_authentication():

    # ----------------------------------------------------------
    # Initialize Authentication State
    # ----------------------------------------------------------

    initialize_auth_state()


    # ----------------------------------------------------------
    # Create Tabs
    # ----------------------------------------------------------

    login_tab, register_tab = st.tabs(

        [

            "🔐 Login",

            "📝 Register"

        ]

    )


    # ----------------------------------------------------------
    # Login Tab
    # ----------------------------------------------------------

    with login_tab:

        render_login()


    # ----------------------------------------------------------
    # Registration Tab
    # ----------------------------------------------------------

    with register_tab:

        render_registration()


# ==============================================================
# Logout
# ==============================================================

def logout():

    # ----------------------------------------------------------
    # Clear Authentication Status
    # ----------------------------------------------------------

    st.session_state.authenticated = False


    # ----------------------------------------------------------
    # Clear JWT Token
    # ----------------------------------------------------------

    st.session_state.access_token = None


    # ----------------------------------------------------------
    # Clear Current User
    # ----------------------------------------------------------

    st.session_state.current_user = None


    # ----------------------------------------------------------
    # Reload Application
    # ----------------------------------------------------------

    st.rerun()