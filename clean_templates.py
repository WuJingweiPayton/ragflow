#!/usr/bin/env python3
"""
清理数据库中的模板记录
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.db.db_models import init_database_tables as init_web_db
from api.db.services.canvas_service import CanvasTemplateService
from api.db.db_models import CanvasTemplate

def clean_templates():
    """清理数据库中的特定模板记录"""
    
    # 初始化数据库连接
    init_web_db()
    
    # 要删除的模板标题
    templates_to_delete = [
        "Custom Template",
        "llm",
        "Custom Template Template"
    ]
    
    print("开始清理模板记录...")
    
    for title in templates_to_delete:
        try:
            # 查找匹配的模板记录
            templates = CanvasTemplateService.query(title=title)
            
            if templates:
                for template in templates:
                    print(f"删除模板: {template.title} (ID: {template.id})")
                    CanvasTemplateService.delete_by_id(template.id)
                print(f"成功删除 {len(templates)} 个标题为 '{title}' 的模板")
            else:
                print(f"未找到标题为 '{title}' 的模板")
                
        except Exception as e:
            print(f"删除模板 '{title}' 时出错: {e}")
    
    print("模板清理完成！")

if __name__ == "__main__":
    clean_templates() 