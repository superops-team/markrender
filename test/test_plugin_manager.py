#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件管理器测试文件
验证插件管理器的功能实现
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.editor.plugin_manager import PluginManager, PluginInfo, PluginValidator


async def test_plugin_manager():
    """测试插件管理器功能"""
    print("🧪 开始测试插件管理器...")
    
    try:
        # 创建临时插件目录结构用于测试
        with tempfile.TemporaryDirectory() as temp_dir:
            plugins_dir = Path(temp_dir) / "plugins"
            plugins_dir.mkdir()
            
            # 创建共享目录
            shared_dir = plugins_dir / "shared"
            shared_dir.mkdir()
            
            # 创建共享文件
            (shared_dir / "webchannel-core.js").write_text("// WebChannel核心库")
            (shared_dir / "common.css").write_text("/* 通用样式 */")
            
            # 创建测试插件1
            plugin1_dir = plugins_dir / "test-plugin-1"
            plugin1_dir.mkdir()
            
            plugin1_config = {
                "id": "test-plugin-1",
                "name": "测试插件1",
                "description": "第一个测试插件",
                "version": "1.0.0",
                "author": "Test Author",
                "license": "MIT",
                "engine": {
                    "name": "test-engine",
                    "version": "^1.0.0"
                },
                "capabilities": {
                    "pageTypes": ["markdown", "text"],
                    "supportedFormats": ["md", "txt"],
                    "features": ["auto-save", "export"]
                },
                "entry": {
                    "main": "index.html"
                },
                "assets": {
                    "styles": ["assets/style.css"],
                    "scripts": ["assets/main.js"]
                },
                "permissions": ["read-data", "write-data"],
                "dependencies": {
                    "shared": ["webchannel-core"],
                    "external": []
                },
                "settings": {
                    "configurable": True,
                    "schema": {
                        "theme": {
                            "type": "string",
                            "default": "light"
                        }
                    }
                }
            }
            
            # 写入插件配置
            with open(plugin1_dir / "plugin.json", "w", encoding="utf-8") as f:
                import json
                json.dump(plugin1_config, f, ensure_ascii=False, indent=2)
            
            # 创建插件文件
            (plugin1_dir / "index.html").write_text("<html><body>Test Plugin 1</body></html>")
            assets_dir = plugin1_dir / "assets"
            assets_dir.mkdir()
            (assets_dir / "style.css").write_text("/* Plugin 1 Style */")
            (assets_dir / "main.js").write_text("// Plugin 1 Script")
            
            # 创建测试插件2
            plugin2_dir = plugins_dir / "test-plugin-2"
            plugin2_dir.mkdir()
            
            plugin2_config = {
                "id": "test-plugin-2",
                "name": "测试插件2",
                "description": "第二个测试插件",
                "version": "1.0.0",
                "author": "Test Author",
                "license": "MIT",
                "engine": {
                    "name": "test-engine",
                    "version": "^1.0.0"
                },
                "capabilities": {
                    "pageTypes": ["excalidraw"],
                    "supportedFormats": ["json"],
                    "features": ["real-time-editing", "export"]
                },
                "entry": {
                    "main": "index.html"
                },
                "permissions": ["read-data", "write-data", "export-data"],
                "dependencies": {
                    "shared": ["webchannel-core", "common.css"],
                    "external": []
                }
            }
            
            # 写入插件配置
            with open(plugin2_dir / "plugin.json", "w", encoding="utf-8") as f:
                json.dump(plugin2_config, f, ensure_ascii=False, indent=2)
            
            # 创建插件文件
            (plugin2_dir / "index.html").write_text("<html><body>Test Plugin 2</body></html>")
            
            # 创建无效插件（缺少必需字段）
            invalid_plugin_dir = plugins_dir / "invalid-plugin"
            invalid_plugin_dir.mkdir()
            
            invalid_config = {
                "id": "invalid-plugin",
                "name": "无效插件",
                # 缺少description, version, author, license等必需字段
                "entry": {
                    "main": "index.html"
                }
            }
            
            with open(invalid_plugin_dir / "plugin.json", "w", encoding="utf-8") as f:
                json.dump(invalid_config, f, ensure_ascii=False, indent=2)
            
            (invalid_plugin_dir / "index.html").write_text("<html><body>Invalid Plugin</body></html>")
            
            # 初始化插件管理器
            print("1️⃣ 测试插件管理器初始化...")
            plugin_manager = PluginManager(str(plugins_dir))
            
            # 测试插件发现
            print("2️⃣ 测试插件发现...")
            discovered_plugins = await plugin_manager.discover_plugins()
            assert len(discovered_plugins) == 3, f"期望发现3个插件，实际发现{len(discovered_plugins)}个"
            print(f"   ✅ 成功发现 {len(discovered_plugins)} 个插件")
            
            # 测试获取插件
            print("3️⃣ 测试获取插件...")
            plugin1 = plugin_manager.get_plugin("test-plugin-1")
            assert plugin1 is not None, "无法获取test-plugin-1"
            assert plugin1.id == "test-plugin-1", "插件ID不匹配"
            assert plugin1.name == "测试插件1", "插件名称不匹配"
            print("   ✅ 成功获取插件信息")
            
            # 测试插件验证
            print("4️⃣ 测试插件验证...")
            validation_results = await plugin_manager.validate_plugins()
            
            # 检查验证结果
            valid_plugins = [pid for pid, errors in validation_results.items() if not errors]
            invalid_plugins = [pid for pid, errors in validation_results.items() if errors]
            
            assert "test-plugin-1" in valid_plugins, "有效插件验证失败"
            assert "test-plugin-2" in valid_plugins, "有效插件验证失败"
            assert "invalid-plugin" in invalid_plugins, "无效插件应该验证失败"
            
            print(f"   ✅ 验证完成: {len(valid_plugins)} 个有效插件, {len(invalid_plugins)} 个无效插件")
            
            # 测试按类型获取插件
            print("5️⃣ 测试按类型获取插件...")
            markdown_plugins = plugin_manager.get_plugins_by_type("markdown")
            assert len(markdown_plugins) == 1, "应该找到1个markdown插件"
            assert markdown_plugins[0].id == "test-plugin-1", "插件ID不匹配"
            print("   ✅ 按类型获取插件功能正常")
            
            # 测试激活插件
            print("6️⃣ 测试激活插件...")
            activate_result = await plugin_manager.activate_plugin("test-plugin-1")
            assert activate_result, "插件激活失败"
            
            plugin1_after_activate = plugin_manager.get_plugin("test-plugin-1")
            assert plugin1_after_activate.status.value == "active", "插件状态应该是active"
            print("   ✅ 插件激活功能正常")
            
            # 测试获取所有插件
            print("7️⃣ 测试获取所有插件...")
            all_plugins = plugin_manager.get_all_plugins()
            assert len(all_plugins) == 2, f"应该有2个有效插件，实际有{len(all_plugins)}个"
            
            all_plugins_with_error = plugin_manager.get_all_plugins(include_error=True)
            assert len(all_plugins_with_error) == 3, f"包含错误插件应该有3个，实际有{len(all_plugins_with_error)}个"
            print("   ✅ 获取插件列表功能正常")
            
            # 测试统计信息
            print("8️⃣ 测试统计信息...")
            stats = plugin_manager.get_statistics()
            assert stats["total_plugins"] == 3, "总插件数应该为3"
            assert stats["active_plugins"] == 1, "激活插件数应该为1"
            print("   ✅ 统计信息功能正常")
            
            # 测试插件信息转换
            print("9️⃣ 测试插件信息转换...")
            plugin1_dict = plugin1.to_dict()
            assert plugin1_dict["id"] == "test-plugin-1", "转换后的ID不匹配"
            assert "status" in plugin1_dict, "转换后应该包含状态信息"
            print("   ✅ 插件信息转换功能正常")
            
            print("🎉 所有插件管理器测试通过！")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_plugin_validator():
    """测试插件验证器"""
    print("\n🔍 开始测试插件验证器...")
    
    try:
        # 测试有效配置
        valid_config = {
            "id": "valid-plugin",
            "name": "有效插件",
            "description": "这是一个有效的插件",
            "version": "1.0.0",
            "author": "Test Author",
            "license": "MIT",
            "entry": {
                "main": "index.html"
            }
        }
        
        is_valid, errors = PluginValidator.validate_config(valid_config)
        assert is_valid, f"有效配置验证失败: {errors}"
        print("   ✅ 有效配置验证通过")
        
        # 测试无效配置（缺少必需字段）
        invalid_config = {
            "id": "invalid-plugin",
            "name": "无效插件"
            # 缺少description, version, author, license等必需字段
        }
        
        is_valid, errors = PluginValidator.validate_config(invalid_config)
        assert not is_valid, "无效配置应该验证失败"
        assert len(errors) > 0, "应该有错误信息"
        print("   ✅ 无效配置验证正确识别错误")
        
        # 测试版本号验证
        assert PluginValidator._is_valid_version("1.0.0"), "应该接受1.0.0格式"
        assert PluginValidator._is_valid_version("2.1.3-beta.1"), "应该接受语义化版本"
        assert not PluginValidator._is_valid_version("invalid"), "应该拒绝无效版本"
        print("   ✅ 版本号验证功能正常")
        
        print("🎉 插件验证器测试通过！")
        
    except Exception as e:
        print(f"❌ 验证器测试失败: {e}")
        raise


async def main():
    """主测试函数"""
    print("🚀 开始测试插件管理器功能\n")
    
    try:
        test_plugin_validator()
        await test_plugin_manager()
        
        print("\n🎊 所有测试通过！插件管理器功能正常！")
        print("\n📋 功能验证摘要:")
        print("   ✅ 插件发现和加载")
        print("   ✅ 插件配置验证")
        print("   ✅ 插件按类型筛选")
        print("   ✅ 插件激活和状态管理")
        print("   ✅ 插件统计信息")
        print("   ✅ 插件信息转换")
        print("\n🎯 插件管理器已准备好集成到主应用中！")
        
    except Exception as e:
        print(f"\n💥 测试失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)