#!/usr/bin/env python3
"""
初始化数据库脚本
创建默认的角色和权限
"""

import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session
from backend.app.core.deps import engine, create_db_and_tables
from backend.app.models.user import User, Role, Permission, UserRole, RolePermission
from backend.app.models.videos import Category
from backend.app.core.security import get_password_hash
from datetime import datetime, UTC

def init_database():
    # 创建数据库表
    create_db_and_tables()
    
    with Session(engine) as session:
        # 检查是否已有数据
        existing_roles = session.query(Role).count()
        if existing_roles > 0:
            print("数据库已经初始化，跳过")
            return
        
        # 创建权限
        permissions = [
            Permission(code="user:list", description="查看用户列表"),
            Permission(code="user:add", description="添加用户"),
            Permission(code="user:edit", description="编辑用户"),
            Permission(code="user:delete", description="删除用户"),
            Permission(code="video:list", description="查看视频列表"),
            Permission(code="video:upload", description="上传视频"),
            Permission(code="video:edit", description="编辑视频"),
            Permission(code="video:delete", description="删除视频"),
            Permission(code="role:list", description="查看角色列表"),
            Permission(code="role:add", description="添加角色"),
            Permission(code="role:edit", description="编辑角色"),
            Permission(code="role:delete", description="删除角色"),
            Permission(code="permission:list", description="查看权限列表"),
            Permission(code="permission:add", description="添加权限"),
            Permission(code="permission:edit", description="编辑权限"),
            Permission(code="permission:delete", description="删除权限"),
        ]
        session.add_all(permissions)
        session.commit()
        
        # 创建角色
        admin_role = Role(name="admin", description="管理员")
        user_role = Role(name="user", description="普通用户")
        session.add_all([admin_role, user_role])
        session.commit()
        
        # 为管理员角色分配所有权限
        for permission in permissions:
            role_permission = RolePermission(
                role_id=admin_role.id,
                permission_id=permission.id
            )
            session.add(role_permission)
        
        # 为普通用户分配部分权限
        user_permissions = [p for p in permissions if p.code in ["video:list", "video:upload"]]
        for permission in user_permissions:
            role_permission = RolePermission(
                role_id=user_role.id,
                permission_id=permission.id
            )
            session.add(role_permission)
        
        # 创建 admin 用户
        admin_user = User(
            username="admin",
            password="admin",
            hashed_password=get_password_hash("admin"),
            gender=1,
            status=1,
            email="admin@example.com"
        )
        session.add(admin_user)
        session.commit()
        
        # 创建默认分类
        categories = [
            Category(name="Comedy", description=""),
            Category(name="Romance", description=""),
            Category(name="Horror", description=""),
            Category(name="Action", description=""),
            Category(name="Sci-Fi", description=""),
            Category(name="Drama", description=""),
            Category(name="Adventure", description=""),
            Category(name="Animation", description=""),
            Category(name="Crime", description=""),
            Category(name="Documentary", description=""),
            Category(name="Family", description=""),
            Category(name="Fantasy", description=""),
            Category(name="History", description=""),
            Category(name="Music", description=""),
            Category(name="Mystery", description=""),
            Category(name="News", description=""),
            Category(name="Reality", description=""),
            Category(name="Sport", description=""),
            Category(name="Talk Show", description=""),
            Category(name="Thriller", description=""),
            Category(name="War", description=""),
            Category(name="Western", description=""),
            Category(name="Biography", description=""),
            Category(name="Musical", description=""),
            Category(name="Superhero", description=""),
            Category(name="Disaster", description=""),
        ]
        session.add_all(categories)
        session.commit()

        # 为 admin 用户分配 admin 角色
        user_role_link = UserRole(
            user_id=admin_user.id,
            role_id=admin_role.id
        )
        session.add(user_role_link)
        
        session.commit()
        print("数据库初始化完成！")
        print("默认管理员账号：admin / admin")
        print("默认分类：喜剧、爱情、恐怖、动作、科幻、剧情")

if __name__ == "__main__":
    init_database()