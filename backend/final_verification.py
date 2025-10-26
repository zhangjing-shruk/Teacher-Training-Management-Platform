#!/usr/bin/env python3
"""
最终验证脚本 - 确认所有修复都成功
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"
TEST_EMAIL = "zhangjing32@51talk.com"
TEST_PASSWORD = "admin123456"

def final_verification():
    print("🎯 最终验证 - 确认所有修复都成功")
    print("=" * 50)
    
    # 1. 验证后端服务器
    print("\n1. 验证后端服务器...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务器运行正常")
        else:
            print(f"❌ 后端服务器异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端服务器连接失败: {e}")
        return False
    
    # 2. 验证前端服务器
    print("\n2. 验证前端服务器...")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务器运行正常")
        else:
            print(f"❌ 前端服务器异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务器连接失败: {e}")
        return False
    
    # 3. 验证登录API
    print("\n3. 验证登录API...")
    login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ 登录API正常")
        else:
            print(f"❌ 登录API失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 登录API请求失败: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. 验证课程主题获取API
    print("\n4. 验证课程主题获取API...")
    try:
        response = requests.get(f"{BASE_URL}/api/manager/course-topics", headers=headers, timeout=10)
        if response.status_code == 200:
            topics = response.json()
            print(f"✅ 课程主题获取API正常 (返回{len(topics)}个主题)")
        else:
            print(f"❌ 课程主题获取API失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 课程主题获取API请求失败: {e}")
        return False
    
    # 5. 验证课程主题批量更新API
    print("\n5. 验证课程主题批量更新API...")
    test_topics = [
        "数学基础概念",
        "语文阅读理解", 
        "英语口语交流",
        "科学实验探索",
        "历史文化传承",
        "最终验证测试主题"
    ]
    
    try:
        batch_data = {"topics": test_topics}
        response = requests.post(
            f"{BASE_URL}/api/manager/course-topics/batch", 
            json=batch_data, 
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 课程主题批量更新API正常")
        else:
            print(f"❌ 课程主题批量更新API失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 课程主题批量更新API请求失败: {e}")
        return False
    
    # 6. 验证CORS配置
    print("\n6. 验证CORS配置...")
    try:
        headers_cors = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Authorization'
        }
        response = requests.options(f"{BASE_URL}/api/manager/course-topics", headers=headers_cors, timeout=5)
        
        if response.status_code == 200:
            cors_headers = response.headers
            if 'access-control-allow-origin' in cors_headers:
                print("✅ CORS配置正常")
            else:
                print("❌ CORS配置可能有问题")
                return False
        else:
            print(f"❌ CORS预检请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS验证失败: {e}")
        return False
    
    # 7. 模拟浏览器请求
    print("\n7. 模拟浏览器请求...")
    try:
        # 模拟浏览器环境
        browser_headers = {
            'Origin': FRONTEND_URL,
            'Referer': f'{FRONTEND_URL}/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        # 登录
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, headers=browser_headers, timeout=10)
        if login_response.status_code == 200:
            browser_token = login_response.json().get("access_token")
            
            # 获取课程主题
            auth_headers = {**browser_headers, 'Authorization': f'Bearer {browser_token}'}
            topics_response = requests.get(f"{BASE_URL}/api/manager/course-topics", headers=auth_headers, timeout=10)
            
            if topics_response.status_code == 200:
                print("✅ 浏览器环境模拟请求成功")
            else:
                print(f"❌ 浏览器环境模拟请求失败: {topics_response.status_code}")
                return False
        else:
            print(f"❌ 浏览器环境模拟登录失败: {login_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 浏览器环境模拟失败: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 所有验证都通过了！")
    print("\n📋 修复总结:")
    print("1. ✅ 修复了API请求URL路径问题")
    print("2. ✅ 修复了token获取key名称问题")
    print("3. ✅ 添加了详细的调试信息")
    print("4. ✅ 验证了CORS配置")
    print("5. ✅ 确认了所有API功能正常")
    
    print("\n🌐 浏览器使用指南:")
    print(f"1. 访问: {FRONTEND_URL}/manager/lectures")
    print("2. 使用管理员账户登录")
    print("3. 点击'管理课程主题'按钮")
    print("4. 现在应该可以正常加载和保存课程主题了！")
    
    print("\n🔍 如果仍有问题，请检查:")
    print("- 浏览器控制台的详细调试信息")
    print("- 网络面板中的API请求状态")
    print("- localStorage中的access_token")
    
    return True

if __name__ == "__main__":
    success = final_verification()
    if success:
        print("\n✅ 验证完成 - 所有功能正常！")
    else:
        print("\n❌ 验证失败 - 仍有问题需要解决")