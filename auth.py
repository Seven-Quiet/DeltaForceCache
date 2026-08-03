"""
用户认证模块
负责用户登录、登出、会话管理
"""
import json
import os
import streamlit as st

USERS_FILE = os.path.join(os.path.dirname(__file__), "data", "users.json")
USERS_TEMPLATE = os.path.join(os.path.dirname(__file__), "data", "users_template.json")


def _ensure_data_file(filepath, template_path):
    """确保数据文件存在，不存在则从模板复制"""
    if not os.path.exists(filepath) and os.path.exists(template_path):
        import shutil
        shutil.copy(template_path, filepath)


def load_users():
    """加载用户数据"""
    _ensure_data_file(USERS_FILE, USERS_TEMPLATE)
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    """保存用户数据"""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def login(username, password):
    """
    用户登录验证
    返回 (success, message)
    """
    users = load_users()
    if username not in users:
        return False, "用户不存在"
    if users[username]["password"] != password:
        return False, "密码错误"
    # 登录成功，设置 session
    st.session_state["logged_in"] = True
    st.session_state["username"] = username
    st.session_state["role"] = users[username]["role"]
    st.session_state["nickname"] = users[username].get("nickname", username)
    return True, "登录成功"


def logout():
    """用户登出"""
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.session_state["nickname"] = None


def is_logged_in():
    """检查是否已登录"""
    return st.session_state.get("logged_in", False)


def get_current_user():
    """获取当前登录用户"""
    if is_logged_in():
        return {
            "username": st.session_state.get("username"),
            "role": st.session_state.get("role"),
            "nickname": st.session_state.get("nickname"),
        }
    return None


def register(username, password, nickname, role="user"):
    """
    注册新用户
    返回 (success, message)
    """
    users = load_users()
    if username in users:
        return False, "用户名已存在"
    if not username or not password:
        return False, "用户名和密码不能为空"
    if not nickname:
        return False, "昵称不能为空"
    users[username] = {
        "password": password,
        "nickname": nickname,
        "role": role,
        "created_at": "2026-08-03",
    }
    save_users(users)
    return True, "注册成功"


def init_session():
    """初始化会话状态"""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "nickname" not in st.session_state:
        st.session_state["nickname"] = None
