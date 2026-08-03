"""
枪械改枪码数据管理模块
负责枪械分类、改枪码的增删改查
"""
import json
import os
import uuid
from datetime import datetime

GUN_CODES_FILE = os.path.join(os.path.dirname(__file__), "data", "gun_codes.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "data", "operation_logs.json")


def load_gun_data():
    """加载枪械改枪码数据"""
    if not os.path.exists(GUN_CODES_FILE):
        return {"categories": []}
    with open(GUN_CODES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_gun_data(data):
    """保存枪械改枪码数据"""
    os.makedirs(os.path.dirname(GUN_CODES_FILE), exist_ok=True)
    with open(GUN_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_categories():
    """获取所有枪械分类"""
    data = load_gun_data()
    return data.get("categories", [])


def get_category_by_id(category_id):
    """根据ID获取分类"""
    categories = get_categories()
    for cat in categories:
        if cat["id"] == category_id:
            return cat
    return None


def get_guns_by_category(category_id):
    """获取指定分类下的所有枪械"""
    category = get_category_by_id(category_id)
    if category:
        return category.get("guns", [])
    return []


def get_gun_by_id(category_id, gun_id):
    """根据ID获取枪械"""
    guns = get_guns_by_category(category_id)
    for gun in guns:
        if gun["id"] == gun_id:
            return gun
    return None


def get_gun_codes(category_id, gun_id):
    """获取指定枪械的所有改枪码"""
    gun = get_gun_by_id(category_id, gun_id)
    if gun:
        return gun.get("codes", [])
    return []


def get_code_by_id(category_id, gun_id, code_id):
    """根据ID获取改枪码"""
    codes = get_gun_codes(category_id, gun_id)
    for code in codes:
        if code["id"] == code_id:
            return code
    return None


def add_category(name, icon="🔫"):
    """添加新分类"""
    data = load_gun_data()
    category_id = str(uuid.uuid4())[:8]
    new_category = {
        "id": category_id,
        "name": name,
        "icon": icon,
        "guns": [],
    }
    data["categories"].append(new_category)
    save_gun_data(data)
    return category_id


def add_gun(category_id, name, description=""):
    """添加新枪械"""
    data = load_gun_data()
    for cat in data["categories"]:
        if cat["id"] == category_id:
            gun_id = str(uuid.uuid4())[:8]
            new_gun = {
                "id": gun_id,
                "name": name,
                "description": description,
                "codes": [],
            }
            cat["guns"].append(new_gun)
            save_gun_data(data)
            return gun_id
    return None


def add_gun_code(category_id, gun_id, code_name, code, parts, tags=None, nickname=None):
    """添加改枪码"""
    data = load_gun_data()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for cat in data["categories"]:
        if cat["id"] == category_id:
            for gun in cat["guns"]:
                if gun["id"] == gun_id:
                    code_id = str(uuid.uuid4())[:8]
                    new_code = {
                        "id": code_id,
                        "name": code_name,
                        "code": code,
                        "parts": parts,
                        "tags": tags or [],
                        "created_at": now,
                        "updated_at": now,
                        "created_by": nickname or "",
                        "updated_by": nickname or "",
                    }
                    gun["codes"].append(new_code)
                    save_gun_data(data)
                    return code_id
    return None


def update_gun_code(category_id, gun_id, code_id, code_name=None, code=None, parts=None, tags=None, nickname=None):
    """更新改枪码"""
    data = load_gun_data()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for cat in data["categories"]:
        if cat["id"] == category_id:
            for gun in cat["guns"]:
                if gun["id"] == gun_id:
                    for c in gun["codes"]:
                        if c["id"] == code_id:
                            if code_name is not None:
                                c["name"] = code_name
                            if code is not None:
                                c["code"] = code
                            if parts is not None:
                                c["parts"] = parts
                            if tags is not None:
                                c["tags"] = tags
                            c["updated_at"] = now
                            if nickname is not None:
                                c["updated_by"] = nickname
                            save_gun_data(data)
                            return True
    return False


def delete_gun_code(category_id, gun_id, code_id):
    """删除改枪码"""
    data = load_gun_data()
    for cat in data["categories"]:
        if cat["id"] == category_id:
            for gun in cat["guns"]:
                if gun["id"] == gun_id:
                    gun["codes"] = [c for c in gun["codes"] if c["id"] != code_id]
                    save_gun_data(data)
                    return True
    return False


def delete_gun(category_id, gun_id):
    """删除枪械"""
    data = load_gun_data()
    for cat in data["categories"]:
        if cat["id"] == category_id:
            cat["guns"] = [g for g in cat["guns"] if g["id"] != gun_id]
            save_gun_data(data)
            return True
    return False


def delete_category(category_id):
    """删除分类"""
    data = load_gun_data()
    data["categories"] = [c for c in data["categories"] if c["id"] != category_id]
    save_gun_data(data)
    return True


def search_guns(keyword):
    """搜索枪械"""
    data = load_gun_data()
    results = []
    keyword = keyword.lower()
    for cat in data["categories"]:
        for gun in cat["guns"]:
            if keyword in gun["name"].lower() or keyword in gun.get("description", "").lower():
                results.append(
                    {
                        "category_id": cat["id"],
                        "category_name": cat["name"],
                        "gun": gun,
                    }
                )
    return results


def search_codes(keyword):
    """搜索改枪码"""
    data = load_gun_data()
    results = []
    keyword = keyword.lower()
    for cat in data["categories"]:
        for gun in cat["guns"]:
            for code in gun["codes"]:
                if (
                    keyword in code["name"].lower()
                    or keyword in code["code"].lower()
                    or any(keyword in tag.lower() for tag in code.get("tags", []))
                ):
                    results.append(
                        {
                            "category_id": cat["id"],
                            "category_name": cat["name"],
                            "gun_id": gun["id"],
                            "gun_name": gun["name"],
                            "code": code,
                        }
                    )
    return results


def log_operation(username, action, target_type, target_name, detail=""):
    """记录用户操作日志"""
    logs = load_logs()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "id": str(uuid.uuid4())[:8],
        "username": username,
        "action": action,          # create / update / delete
        "target_type": target_type,  # category / gun / code
        "target_name": target_name,
        "detail": detail,
        "timestamp": now,
    }
    logs.append(log_entry)
    save_logs(logs)


def load_logs():
    """加载操作日志"""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_logs(logs):
    """保存操作日志"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def get_operation_logs(limit=50):
    """获取最近的操作日志"""
    logs = load_logs()
    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    return logs[:limit]


def get_statistics():
    """获取统计信息"""
    data = load_gun_data()
    categories = data.get("categories", [])
    total_categories = len(categories)
    total_guns = sum(len(cat.get("guns", [])) for cat in categories)
    total_codes = sum(
        len(gun.get("codes", []))
        for cat in categories
        for gun in cat.get("guns", [])
    )
    return {
        "total_categories": total_categories,
        "total_guns": total_guns,
        "total_codes": total_codes,
    }
