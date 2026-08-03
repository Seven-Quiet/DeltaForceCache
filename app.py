"""
三角洲枪械改枪码管理系统
类似飞书云文档风格的 Streamlit 应用
"""
import streamlit as st
from auth import init_session, is_logged_in, login, logout, get_current_user, register
from data_manager import (
    get_categories,
    get_guns_by_category,
    get_gun_codes,
    get_code_by_id,
    add_category,
    add_gun,
    add_gun_code,
    update_gun_code,
    delete_gun_code,
    delete_gun,
    delete_category,
    search_codes,
    get_statistics,
)

# 页面配置
st.set_page_config(
    page_title="三角洲枪械改枪码库",
    page_icon="🔫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 初始化会话
init_session()

# 自定义 CSS 样式 - 飞书风格
st.markdown(
    """
<style>
    /* 全局样式 */
    .stApp {
        background-color: #f5f6f7;
    }
    
    /* 主标题样式 */
    .main-title {
        font-size: 24px;
        font-weight: 600;
        color: #1f2329;
        padding: 16px 0;
        border-bottom: 1px solid #e5e6eb;
        margin-bottom: 16px;
    }
    
    /* 卡片样式 */
    .doc-card {
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid transparent;
    }
    .doc-card:hover {
        background: #f0f1f3;
        border-color: #3370ff;
    }
    .doc-card.selected {
        background: #e8f3ff;
        border-color: #3370ff;
    }
    
    /* 分类标题 */
    .category-title {
        font-size: 14px;
        font-weight: 600;
        color: #646a73;
        padding: 8px 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* 文档标题 */
    .doc-title {
        font-size: 15px;
        font-weight: 500;
        color: #1f2329;
        margin-bottom: 4px;
    }
    
    /* 文档描述 */
    .doc-desc {
        font-size: 13px;
        color: #8f959e;
        margin-bottom: 8px;
    }
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    .tag-blue {
        background: #e8f3ff;
        color: #3370ff;
    }
    .tag-green {
        background: #e8ffea;
        color: #00b42a;
    }
    .tag-orange {
        background: #fff7e8;
        color: #ff7d00;
    }
    .tag-red {
        background: #ffece8;
        color: #f53f3f;
    }
    
    /* 代码块样式 */
    .code-box {
        background: #272e3b;
        color: #00ff88;
        padding: 12px 16px;
        border-radius: 6px;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 14px;
        margin: 12px 0;
        letter-spacing: 1px;
    }
    
    /* 配件表格 */
    .parts-table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
    }
    .parts-table th {
        background: #f7f8fa;
        padding: 10px 12px;
        text-align: left;
        font-weight: 600;
        color: #4e5969;
        border-bottom: 1px solid #e5e6eb;
    }
    .parts-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #f2f3f5;
        color: #1f2329;
    }
    .parts-table tr:hover {
        background: #f7f8fa;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e6eb;
    }
    
    /* 按钮样式 */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border-radius: 6px;
    }
    
    /* 登录页面样式 */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    .login-title {
        text-align: center;
        font-size: 28px;
        font-weight: 700;
        color: #1f2329;
        margin-bottom: 8px;
    }
    .login-subtitle {
        text-align: center;
        font-size: 14px;
        color: #86909c;
        margin-bottom: 32px;
    }
    
    /* 统计卡片 */
    .stat-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .stat-number {
        font-size: 32px;
        font-weight: 700;
        color: #3370ff;
        margin-bottom: 4px;
    }
    .stat-label {
        font-size: 14px;
        color: #86909c;
    }
    
    /* 空状态 */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #86909c;
    }
    .empty-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }
    .empty-text {
        font-size: 16px;
        margin-bottom: 8px;
    }
    .empty-hint {
        font-size: 13px;
    }
    
    /* 面包屑 */
    .breadcrumb {
        font-size: 14px;
        color: #86909c;
        margin-bottom: 16px;
    }
    .breadcrumb a {
        color: #3370ff;
        text-decoration: none;
        cursor: pointer;
    }
    .breadcrumb a:hover {
        text-decoration: underline;
    }
    .breadcrumb .separator {
        margin: 0 8px;
        color: #c9cdd4;
    }
</style>
""",
    unsafe_allow_html=True,
)


def render_login_page():
    """渲染登录页面"""
    st.markdown(
        """
    <div class="login-container">
        <div class="login-title">🔫 三角洲枪械库</div>
        <div class="login-subtitle">改枪码管理系统</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 使用表单
    with st.form("login_form"):
        username = st.text_input("用户名", placeholder="请输入用户名")
        password = st.text_input("密码", type="password", placeholder="请输入密码")
        submit = st.form_submit_button("登录", use_container_width=True)

        if submit:
            success, message = login(username, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    # 注册选项
    with st.expander("没有账号？点击注册"):
        with st.form("register_form"):
            new_nickname = st.text_input("昵称", placeholder="请输入您的昵称")
            new_username = st.text_input("用户名", placeholder="请输入用户名")
            new_password = st.text_input("密码", type="password", placeholder="请输入密码")
            confirm_password = st.text_input("确认密码", type="password", placeholder="请再次输入密码")
            register_submit = st.form_submit_button("注册", use_container_width=True)

            if register_submit:
                if not new_nickname:
                    st.error("昵称不能为空")
                elif new_password != confirm_password:
                    st.error("两次密码不一致")
                else:
                    success, message = register(new_username, new_password, new_nickname)
                    if success:
                        # 注册成功，自动登录
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = new_username
                        st.session_state["nickname"] = new_nickname
                        st.session_state["role"] = "user"
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)



def render_sidebar():
    """渲染侧边栏 - 飞书风格导航"""
    with st.sidebar:
        # 顶部标题
        st.markdown("### 🔫 三角洲枪械库")
        st.markdown("---")

        # 用户信息
        user = get_current_user()
        if user:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("👤")
            with col2:
                st.markdown(f"**{user['username']}**")
                st.caption(f"角色：{user['role']}")

            if st.button("退出登录", use_container_width=True):
                logout()
                st.rerun()

        st.markdown("---")

        # 导航菜单
        st.markdown("**📁 我的文档**")

        # 首页按钮
        if st.button("🏠 首页", use_container_width=True, key="btn_home"):
            st.session_state["current_page"] = "home"
            st.session_state["selected_category"] = None
            st.session_state["selected_gun"] = None
            st.session_state["selected_code"] = None
            st.rerun()

        st.markdown("---")

        # 分类列表
        st.markdown("**📂 枪械分类**")

        categories = get_categories()
        for cat in categories:
            gun_count = len(cat.get("guns", []))
            btn_label = f"{cat['icon']} {cat['name']} ({gun_count})"
            if st.button(btn_label, use_container_width=True, key=f"cat_{cat['id']}"):
                st.session_state["current_page"] = "category"
                st.session_state["selected_category"] = cat["id"]
                st.session_state["selected_gun"] = None
                st.session_state["selected_code"] = None
                st.rerun()

        st.markdown("---")

        # 搜索
        st.markdown("**🔍 搜索**")
        search_query = st.text_input("搜索改枪码", placeholder="输入关键词...", key="sidebar_search")
        if search_query:
            st.session_state["current_page"] = "search"
            st.session_state["search_query"] = search_query

        # 管理功能（仅管理员）
        if user and user["role"] == "admin":
            st.markdown("---")
            st.markdown("**⚙️ 管理**")
            if st.button("➕ 新建分类", use_container_width=True, key="btn_add_category"):
                st.session_state["show_add_category"] = True
                st.rerun()


def render_home_page():
    """渲染首页"""
    from datetime import datetime
    hour = datetime.now().hour
    time_icon = "☀️" if 6 <= hour < 18 else "🌙"

    user = get_current_user()
    col_title, col_greet = st.columns([3, 1])
    with col_title:
        st.markdown('<div class="main-title">🏠 首页</div>', unsafe_allow_html=True)
    with col_greet:
        if user:
            st.markdown(
                f'<div style="text-align:right;font-size:16px;font-weight:500;color:#1f2329;padding-top:16px;">'
                f'Hi, {user["nickname"]} {time_icon}'
                f'</div>',
                unsafe_allow_html=True,
            )

    # 统计卡片
    stats = get_statistics()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_categories']}</div>
            <div class="stat-label">枪械分类</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_guns']}</div>
            <div class="stat-label">枪械数量</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_codes']}</div>
            <div class="stat-label">改枪方案</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # 快速访问 - 所有分类
    st.markdown("### 📂 枪械分类")

    categories = get_categories()
    if not categories:
        st.markdown(
            """
        <div class="empty-state">
            <div class="empty-icon">📁</div>
            <div class="empty-text">暂无分类</div>
            <div class="empty-hint">点击左侧「新建分类」开始添加</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    # 分类网格
    cols = st.columns(3)
    for i, cat in enumerate(categories):
        with cols[i % 3]:
            gun_count = len(cat.get("guns", []))
            code_count = sum(len(g.get("codes", [])) for g in cat.get("guns", []))
            st.markdown(
                f"""
            <div class="doc-card" onclick="">
                <div class="doc-title">{cat['icon']} {cat['name']}</div>
                <div class="doc-desc">{gun_count} 把枪械 · {code_count} 套方案</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            if st.button("进入", key=f"home_cat_{cat['id']}", use_container_width=True):
                st.session_state["current_page"] = "category"
                st.session_state["selected_category"] = cat["id"]
                st.session_state["selected_gun"] = None
                st.session_state["selected_code"] = None
                st.rerun()



def render_breadcrumb(items):
    """渲染可点击的面包屑导航
    items: list of (label, state_updates) tuples
        label: 显示文本
        state_updates: dict of session_state 更新
    """
    # 动态计算列宽：每个按钮+分隔符一组，最后一列占满剩余空间
    num_items = len(items)
    # 每个面包屑项占1份，分隔符占0.3份，剩余空间占3份
    col_specs = []
    for i in range(num_items):
        col_specs.append(1.2)  # 按钮列
        if i < num_items - 1:
            col_specs.append(0.25)  # 分隔符 /
    col_specs.append(5)  # 剩余空间

    cols = st.columns(col_specs)
    col_idx = 0
    for i, (label, state_updates) in enumerate(items):
        with cols[col_idx]:
            if st.button(
                label,
                key=f"bc_{i}_{label}",
                use_container_width=True,
            ):
                for k, v in state_updates.items():
                    st.session_state[k] = v
                st.rerun()
        col_idx += 1
        if i < num_items - 1:
            with cols[col_idx]:
                st.markdown(
                    '<span style="color:#c9cdd4;font-size:16px;line-height:2.4;">/</span>',
                    unsafe_allow_html=True,
                )
            col_idx += 1


def render_category_page():
    """渲染分类页面 - 枪械列表"""
    category_id = st.session_state.get("selected_category")
    if not category_id:
        render_home_page()
        return

    categories = get_categories()
    category = None
    for cat in categories:
        if cat["id"] == category_id:
            category = cat
            break

    if not category:
        st.error("分类不存在")
        return

    # 面包屑导航
    render_breadcrumb([
        ("🏠 首页", {"current_page": "home", "selected_category": None, "selected_gun": None, "selected_code": None}),
        (f"{category['icon']} {category['name']}", {}),
    ])

    st.markdown(f'<div class="main-title">{category["icon"]} {category["name"]}</div>', unsafe_allow_html=True)

    # 添加枪械按钮
    user = get_current_user()
    if user:
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("➕ 添加枪械", use_container_width=True, key="btn_add_gun"):
                st.session_state["show_add_gun"] = True
                st.rerun()

    # 枪械列表
    guns = get_guns_by_category(category_id)
    if not guns:
        st.markdown(
            """
        <div class="empty-state">
            <div class="empty-icon">🔫</div>
            <div class="empty-text">该分类下暂无枪械</div>
            <div class="empty-hint">点击右上角「添加枪械」开始创建</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    # 枪械卡片列表
    for gun in guns:
        code_count = len(gun.get("codes", []))
        st.markdown(
            f"""
        <div class="doc-card">
            <div class="doc-title">🔫 {gun['name']}</div>
            <div class="doc-desc">{gun.get('description', '暂无描述')} · {code_count} 套改枪方案</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("查看改枪方案", key=f"gun_{gun['id']}", use_container_width=True):
            st.session_state["current_page"] = "gun_detail"
            st.session_state["selected_gun"] = gun["id"]
            st.session_state["selected_code"] = None
            st.rerun()


def render_gun_detail_page():
    """渲染枪械详情页面 - 改枪码列表"""
    category_id = st.session_state.get("selected_category")
    gun_id = st.session_state.get("selected_gun")

    if not category_id or not gun_id:
        render_home_page()
        return

    categories = get_categories()
    category = None
    gun = None
    for cat in categories:
        if cat["id"] == category_id:
            category = cat
            for g in cat.get("guns", []):
                if g["id"] == gun_id:
                    gun = g
                    break
            break

    if not category or not gun:
        st.error("枪械不存在")
        return

    # 面包屑导航
    render_breadcrumb([
        ("🏠 首页", {"current_page": "home", "selected_category": None, "selected_gun": None, "selected_code": None}),
        (f"{category['icon']} {category['name']}", {"current_page": "category", "selected_gun": None, "selected_code": None}),
        (f"🔫 {gun['name']}", {}),
    ])

    st.markdown(f'<div class="main-title">🔫 {gun["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f"*{gun.get('description', '暂无描述')}*")
    st.markdown("---")

    # 添加改枪码按钮
    user = get_current_user()
    if user:
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("➕ 添加改枪码", use_container_width=True, key="btn_add_code"):
                st.session_state["show_add_code"] = True
                st.rerun()

    # 改枪码列表
    codes = gun.get("codes", [])
    if not codes:
        st.markdown(
            """
        <div class="empty-state">
            <div class="empty-icon">📋</div>
            <div class="empty-text">暂无改枪方案</div>
            <div class="empty-hint">点击右上角「添加改枪码」开始创建</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(f"### 📋 改枪方案 ({len(codes)})")

    for code in codes:
        tags_html = "".join(
            f'<span style="display:inline-block;padding:2px 8px;border-radius:4px;font-size:12px;margin-right:4px;background:#e8f3ff;color:#3370ff;">{tag}</span>'
            for tag in code.get("tags", [])
        )

        # 卡片：标题栏带编辑/删除按钮
        col_title, col_act1, col_act2 = st.columns([6, 1, 1])
        with col_title:
            st.markdown(f"**⚙️ {code['name']}**")
        with col_act1:
            if st.button("编辑", key=f"edit_{code['id']}", use_container_width=True):
                st.session_state["selected_code"] = code["id"]
                st.session_state["show_edit_code"] = True
                st.session_state["delete_code_id"] = None
                st.rerun()
        with col_act2:
            if st.button("删除", key=f"del_{code['id']}", use_container_width=True):
                st.session_state["delete_code_id"] = code["id"]
                st.session_state["selected_code"] = None
                st.rerun()

        escaped_code = code['code'].replace("\\", "\\\\").replace("'", "\\'").replace("`", "\\`")
        st.components.v1.html(
            f"""
        <div style="
            background: white;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 8px;
            border: 1px solid #e5e6eb;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        ">
            <div style="
                background: #272e3b;
                color: #00ff88;
                padding: 12px 16px;
                border-radius: 6px;
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 14px;
                margin-bottom: 8px;
                letter-spacing: 1px;
            ">{code['code']}</div>
            <div style="font-size:13px;color:#8f959e;margin-bottom:8px;display:flex;justify-content:space-between;"><span>更新于 {code['updated_at']}</span>{f"<span>by: {code['updated_by']}</span>" if code.get('updated_by') else ""}</div>
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <div>{tags_html}</div>
                <button onclick="
                    var btn = this;
                    navigator.clipboard.writeText('{escaped_code}').then(function(){{
                        btn.innerText = '✅ 已复制';
                        btn.style.background = '#00b42a';
                        btn.style.borderColor = '#00b42a';
                        btn.style.color = '#fff';
                        setTimeout(function(){{ btn.innerText = '📋 复制'; btn.style.background = '#f0f0f0'; btn.style.borderColor = '#d9d9d9'; btn.style.color = '#333'; }}, 1500);
                    }}).catch(function(){{ alert('复制失败'); }});
                " style="
                    padding: 4px 12px;
                    background: #f0f0f0;
                    border: 1px solid #d9d9d9;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                    color: #333;
                    white-space: nowrap;
                ">📋 复制</button>
            </div>
        </div>
        """,
            height=130,
        )

        # 删除确认：显示在对应卡片下方
        if st.session_state.get("delete_code_id") == code["id"]:
            st.warning(f"确定要删除改枪方案「{code['name']}」吗？此操作不可恢复！")
            col_confirm, col_cancel = st.columns([1, 1])
            with col_confirm:
                if st.button("确认删除", key=f"confirm_del_{code['id']}", use_container_width=True):
                    delete_gun_code(category_id, gun_id, code["id"])
                    st.session_state["delete_code_id"] = None
                    st.success("删除成功")
                    st.rerun()
            with col_cancel:
                if st.button("取消", key=f"cancel_del_{code['id']}", use_container_width=True):
                    st.session_state["delete_code_id"] = None
                    st.rerun()


def render_code_detail_page():
    """渲染改枪码详情页面"""
    category_id = st.session_state.get("selected_category")
    gun_id = st.session_state.get("selected_gun")
    code_id = st.session_state.get("selected_code")

    if not category_id or not gun_id or not code_id:
        render_home_page()
        return

    code = get_code_by_id(category_id, gun_id, code_id)
    if not code:
        st.error("改枪码不存在")
        return

    # 获取分类和枪械信息
    categories = get_categories()
    category = None
    gun = None
    for cat in categories:
        if cat["id"] == category_id:
            category = cat
            for g in cat.get("guns", []):
                if g["id"] == gun_id:
                    gun = g
                    break
            break

    # 面包屑导航
    render_breadcrumb([
        ("🏠 首页", {"current_page": "home", "selected_category": None, "selected_gun": None, "selected_code": None}),
        (f"{category['icon']} {category['name']}", {"current_page": "category", "selected_gun": None, "selected_code": None}),
        (f"🔫 {gun['name']}", {"current_page": "gun_detail", "selected_code": None}),
        (f"⚙️ {code['name']}", {}),
    ])

    st.markdown(f'<div class="main-title">⚙️ {code["name"]}</div>', unsafe_allow_html=True)

    # 操作按钮
    user = get_current_user()
    if user:
        col1, col2, col3 = st.columns([5, 1, 1])
        with col2:
            if st.button("✏️ 编辑", use_container_width=True, key="btn_edit_code"):
                st.session_state["show_edit_code"] = True
                st.rerun()
        with col3:
            if st.button("🗑️ 删除", use_container_width=True, key="btn_delete_code"):
                st.session_state["show_delete_confirm"] = True
                st.rerun()

    # 改枪码
    st.markdown("### 🎯 改枪码")
    st.markdown(
        f"""
    <div class="code-box">{code['code']}</div>
    """,
        unsafe_allow_html=True,
    )

    # 一键复制到剪贴板
    st.components.v1.html(
        f"""
    <div style="display:flex; align-items:center; gap:8px; margin:12px 0;">
        <button id="copyBtn" onclick="
            navigator.clipboard.writeText('{code['code']}').then(function(){{
                var b = document.getElementById('copyBtn');
                b.innerText = '✅ 已复制';
                b.style.background = '#00b42a';
                b.style.borderColor = '#00b42a';
                setTimeout(function(){{ b.innerText = '📋 复制改枪码'; b.style.background = '#3370ff'; b.style.borderColor = '#3370ff'; }}, 2000);
            }}).catch(function(){{
                alert('复制失败，请手动复制');
            }});
        " style="
            padding: 8px 16px;
            background: #3370ff;
            color: white;
            border: 1px solid #3370ff;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        ">📋 复制改枪码</button>
    </div>
    """,
        height=50,
    )

    st.markdown("---")

    # 标签
    st.markdown("### 🏷️ 标签")
    tags = code.get("tags", [])
    if tags:
        tags_html = "".join(
            f'<span class="tag tag-blue">{tag}</span>' for tag in tags
        )
        st.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.info("暂无标签")

    st.markdown("---")

    # 元信息
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**创建时间：** {code.get('created_at', '未知')}")
    with col2:
        st.markdown(f"**更新时间：** {code.get('updated_at', '未知')}")


def render_search_page():
    """渲染搜索结果页面"""
    query = st.session_state.get("search_query", "")
    if not query:
        render_home_page()
        return

    st.markdown(f'<div class="main-title">🔍 搜索结果："{query}"</div>', unsafe_allow_html=True)

    results = search_codes(query)

    if not results:
        st.markdown(
            f"""
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <div class="empty-text">未找到相关结果</div>
            <div class="empty-hint">试试其他关键词吧</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(f"找到 {len(results)} 个结果")
    st.markdown("---")

    for item in results:
        code = item["code"]
        tags_html = "".join(
            f'<span class="tag tag-blue">{tag}</span>' for tag in code.get("tags", [])
        )
        st.markdown(
            f"""
        <div class="doc-card">
            <div class="doc-title">{item['gun_name']} - {code['name']}</div>
            <div class="doc-desc">{item['category_name']} · 更新于 {code['updated_at']}</div>
            <div class="code-box">{code['code']}</div>
            <div>{tags_html}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("查看详情", key=f"search_{code['id']}", use_container_width=True):
            st.session_state["current_page"] = "code_detail"
            st.session_state["selected_category"] = item["category_id"]
            st.session_state["selected_gun"] = item["gun_id"]
            st.session_state["selected_code"] = code["id"]
            st.rerun()


def render_add_category_modal():
    """渲染添加分类弹窗"""
    if st.session_state.get("show_add_category"):
        with st.form("add_category_form"):
            st.markdown("### ➕ 新建分类")
            name = st.text_input("分类名称", placeholder="例如：突击步枪")
            icon = st.text_input("图标（emoji）", value="🔫")
            submitted = st.form_submit_button("创建", use_container_width=True)

            if submitted:
                if name:
                    add_category(name, icon)
                    st.session_state["show_add_category"] = False
                    st.success("分类创建成功！")
                    st.rerun()
                else:
                    st.error("请输入分类名称")

        if st.button("取消", use_container_width=True, key="cancel_add_category"):
            st.session_state["show_add_category"] = False
            st.rerun()


def render_add_gun_modal():
    """渲染添加枪械弹窗"""
    if st.session_state.get("show_add_gun"):
        category_id = st.session_state.get("selected_category")
        with st.form("add_gun_form"):
            st.markdown("### ➕ 添加枪械")
            name = st.text_input("枪械名称", placeholder="例如：M4A1")
            description = st.text_area("描述", placeholder="简单描述这把枪的特点")
            submitted = st.form_submit_button("添加", use_container_width=True)

            if submitted:
                if name:
                    add_gun(category_id, name, description)
                    st.session_state["show_add_gun"] = False
                    st.success("枪械添加成功！")
                    st.rerun()
                else:
                    st.error("请输入枪械名称")

        if st.button("取消", use_container_width=True, key="cancel_add_gun"):
            st.session_state["show_add_gun"] = False
            st.rerun()


def render_add_code_modal():
    """渲染添加改枪码弹窗"""
    if st.session_state.get("show_add_code"):
        category_id = st.session_state.get("selected_category")
        gun_id = st.session_state.get("selected_gun")

        with st.form("add_code_form"):
            st.markdown("### ➕ 添加改枪码")

            code_name = st.text_input("方案名称", placeholder="例如：标准配置")
            code = st.text_input("改枪码", placeholder="输入改枪码字符串")

            tags_input = st.text_input("标签（用逗号分隔）", placeholder="例如：通用,新手推荐")

            submitted = st.form_submit_button("添加", use_container_width=True)

            if submitted:
                if code_name and code:
                    tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []
                    user = get_current_user()
                    add_gun_code(category_id, gun_id, code_name, code, {}, tags, user["nickname"] if user else None)
                    st.session_state["show_add_code"] = False
                    st.success("改枪码添加成功！")
                    st.rerun()
                else:
                    st.error("请填写方案名称和改枪码")

        if st.button("取消", use_container_width=True, key="cancel_add_code"):
            st.session_state["show_add_code"] = False
            st.rerun()


def render_edit_code_modal():
    """渲染编辑改枪码弹窗"""
    if st.session_state.get("show_edit_code"):
        category_id = st.session_state.get("selected_category")
        gun_id = st.session_state.get("selected_gun")
        code_id = st.session_state.get("selected_code")

        code = get_code_by_id(category_id, gun_id, code_id)
        if not code:
            st.error("改枪码不存在")
            return

        with st.form("edit_code_form"):
            st.markdown("### ✏️ 编辑改枪码")

            code_name = st.text_input("方案名称", value=code["name"])
            code_value = st.text_input("改枪码", value=code["code"])

            tags_input = st.text_input(
                "标签（用逗号分隔）",
                value=",".join(code.get("tags", [])),
            )

            submitted = st.form_submit_button("保存", use_container_width=True)

            if submitted:
                if code_name and code_value:
                    tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []
                    current_user = get_current_user()
                    update_gun_code(category_id, gun_id, code_id, code_name, code_value, {}, tags, current_user["nickname"] if current_user else None)
                    st.session_state["show_edit_code"] = False
                    st.success("改枪码更新成功！")
                    st.rerun()
                else:
                    st.error("请填写方案名称和改枪码")

        if st.button("取消", use_container_width=True, key="cancel_edit_code"):
            st.session_state["show_edit_code"] = False
            st.rerun()


def render_delete_confirm():
    """渲染删除确认弹窗"""
    if st.session_state.get("show_delete_confirm"):
        category_id = st.session_state.get("selected_category")
        gun_id = st.session_state.get("selected_gun")
        code_id = st.session_state.get("selected_code")

        code = get_code_by_id(category_id, gun_id, code_id)

        st.warning(f"确定要删除改枪码「{code['name']}」吗？此操作不可恢复！")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("确认删除", use_container_width=True, type="primary"):
                delete_gun_code(category_id, gun_id, code_id)
                st.session_state["show_delete_confirm"] = False
                st.session_state["selected_code"] = None
                st.session_state["current_page"] = "gun_detail"
                st.success("删除成功")
                st.rerun()
        with col2:
            if st.button("取消", use_container_width=True):
                st.session_state["show_delete_confirm"] = False
                st.rerun()


def main():
    """主函数"""
    # 初始化页面状态
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = None
    if "selected_gun" not in st.session_state:
        st.session_state["selected_gun"] = None
    if "selected_code" not in st.session_state:
        st.session_state["selected_code"] = None

    # 检查登录状态
    if not is_logged_in():
        render_login_page()
        return

    # 离开改枪方案列表页时，清除删除确认状态
    if st.session_state.get("current_page") != "gun_detail":
        st.session_state["delete_code_id"] = None

    # 已登录，渲染主界面
    render_sidebar()

    # 主内容区
    current_page = st.session_state.get("current_page", "home")

    if current_page == "home":
        render_home_page()
    elif current_page == "category":
        render_category_page()
    elif current_page == "gun_detail":
        render_gun_detail_page()
    elif current_page == "code_detail":
        render_code_detail_page()
    elif current_page == "search":
        render_search_page()
    else:
        render_home_page()

    # 渲染弹窗
    render_add_category_modal()
    render_add_gun_modal()
    render_add_code_modal()
    render_edit_code_modal()
    render_delete_confirm()


if __name__ == "__main__":
    main()
