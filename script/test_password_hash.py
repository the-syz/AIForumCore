import sys
import os

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.security import get_password_hash

# 测试密码哈希函数
def test_password_hash():
    test_passwords = [
        "123456",  # 短密码
        "password123",  # 中等长度密码
        "a" * 72,  # 刚好72字节的密码
        "a" * 100,  # 超过72字节的密码
    ]
    
    for password in test_passwords:
        try:
            print(f"测试密码: {password}")
            print(f"密码长度: {len(password)}")
            print(f"密码字节长度: {len(password.encode('utf-8'))}")
            hash_value = get_password_hash(password)
            print(f"哈希值: {hash_value}")
            print("测试通过！")
        except Exception as e:
            print(f"测试失败: {str(e)}")
        print("-" * 50)

if __name__ == "__main__":
    test_password_hash()
