import streamlit as st
from datetime import datetime
from config import load_css, load_config, CHAT_COLORS
from login_form import show_login_form
from register_form import show_register_form
from chat_utils import create_chat_interface, display_chat_history_sidebar
from profile_settings import (
    show_user_profile, 
    show_settings, 
    show_sidebar_menu, 
    show_user_info_sidebar,
    apply_custom_css
)
from auth import validate_login_token, cleanup_expired_tokens

API_URL = "https://thuctap365-duanchatbot.onrender.com/api"

def get_query_params():
    try:
        return st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
    except Exception:
        return {}

def set_query_params(params):
    try:
        if hasattr(st, "query_params"):
            st.query_params.update(params)
        else:
            st.experimental_set_query_params(**params)
    except Exception:
        pass

def check_persistent_login():
    cleanup_expired_tokens()
    query_params = get_query_params()
    token_from_url = query_params.get("token", [None])[0] if isinstance(query_params.get("token"), list) else query_params.get("token")
    if token_from_url:
        email = validate_login_token(token_from_url)
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.login_token = token_from_url
            return True
    if 'login_token' in st.session_state and st.session_state.login_token:
        email = validate_login_token(st.session_state.login_token)
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            save_token_to_url(st.session_state.login_token)
            return True
    return False

def save_token_to_url(token):
    if token:
        set_query_params({"token": token})

def main():
    load_css()
    config = load_config()
    apply_custom_css(config)

    st.markdown("""
    <div class="main-header">
        AI Chat Assistant
    </div>
    """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    if 'show_full_history' not in st.session_state:
        st.session_state.show_full_history = False

    if not st.session_state.logged_in:
        check_persistent_login()

    if not st.session_state.logged_in:
        query_params = get_query_params()
        view_param = query_params.get("view")
        if view_param == ["register"] or view_param == "register":
            st.session_state.show_register = True

        if st.session_state.show_register:
            show_register_form()
        else:
            show_login_form()
        return

    user_email = st.session_state.user_email

    with st.sidebar:
        show_user_info_sidebar(user_email)
        st.markdown("---")
        selected_menu = show_sidebar_menu(user_email)

    if selected_menu == "chat":
        if st.session_state.show_full_history:
            st.markdown("### 📚 Lịch sử chat đầy đủ")
            from chat_utils import get_chat_history, group_messages_by_conversation
            chat_history = get_chat_history(user_email)
            if not chat_history:
                st.info("Chưa có lịch sử chat nào.")
            else:
                conversations = group_messages_by_conversation(chat_history)
                for i, conversation in enumerate(reversed(conversations)):
                    conversation_start = conversation[0]["timestamp"]
                    conversation_end = conversation[-1]["timestamp"]
                    message_count = len(conversation)
                    try:
                        start_dt = datetime.fromisoformat(conversation_start)
                        end_dt = datetime.fromisoformat(conversation_end)
                        date_str = start_dt.strftime("%d/%m/%Y")
                        time_range = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                    except:
                        date_str = "Unknown"
                        time_range = "Unknown"
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid {CHAT_COLORS[config.get('chat_color', 'Blue')]};">
                        <strong>📅 Cuộc trò chuyện {len(conversations) - i}</strong><br>
                        <small>🕐 {date_str} | {time_range} | 💬 {message_count} tin nhắn</small>
                    </div>
                    """, unsafe_allow_html=True)
                    for message in conversation:
                        from chat_utils import display_chat_message
                        display_chat_message(message, config.get("chat_color", "Blue"))
                    st.markdown("---")
                if st.button("🔙 Quay lại chat", type="primary"):
                    st.session_state.show_full_history = False
                    st.rerun()
        else:
            with st.container():
                create_chat_interface(user_email, config.get("chat_color", "Blue"))
            display_chat_history_sidebar(user_email, config.get("chat_color", "Blue"))

    elif selected_menu == "profile":
        show_user_profile(user_email)
    elif selected_menu == "settings":
        show_settings()
    elif selected_menu == "history":
        st.markdown("### 📚 Lịch sử chat chi tiết")
        from chat_utils import get_chat_history, group_messages_by_conversation
        chat_history = get_chat_history(user_email)
        if not chat_history:
            st.info("Chưa có lịch sử chat nào.")
        else:
            conversations = group_messages_by_conversation(chat_history)
            for i, conversation in enumerate(reversed(conversations)):
                conversation_start = conversation[0]["timestamp"]
                conversation_end = conversation[-1]["timestamp"]
                message_count = len(conversation)
                try:
                    start_dt = datetime.fromisoformat(conversation_start)
                    end_dt = datetime.fromisoformat(conversation_end)
                    date_str = start_dt.strftime("%d/%m/%Y")
                    time_range = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                except:
                    date_str = "Unknown"
                    time_range = "Unknown"
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; color: black; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 4px solid {CHAT_COLORS[config.get('chat_color', 'Blue')]};">
                    <strong>📅 Cuộc trò chuyện {len(conversations) - i}</strong><br>
                    <small>🕐 {date_str} | {time_range} | 💬 {message_count} tin nhắn</small>
                </div>
                """, unsafe_allow_html=True)
                for message in conversation:
                    from chat_utils import display_chat_message
                    display_chat_message(message, config.get("chat_color", "Blue"))
                st.markdown("---")

if __name__ == "__main__":
    main()
