"""
Flask Mock服务
提供模拟的API接口，用于测试
"""
from flask import Flask, jsonify, request
from datetime import datetime
import random
import string

app = Flask(__name__)

# 模拟数据存储（内存中）
users_db = {}
messages_db = []


def generate_id() -> int:
    """生成随机ID"""
    return random.randint(1000, 9999)


@app.route('/api/user/info', methods=['GET'])
def get_user_info():
    """
    获取用户信息接口
    
    请求参数:
        user_id: 用户ID（必填）
        
    返回:
        {
            "code": 200,
            "message": "success",
            "data": {
                "user_id": 1001,
                "username": "test_user",
                "email": "test@example.com",
                "age": 25,
                "created_at": "2024-01-01 10:00:00"
            }
        }
    """
    user_id = request.args.get('user_id', type=int)
    
    if not user_id:
        return jsonify({
            "code": 400,
            "message": "参数错误: user_id不能为空",
            "data": None
        }), 400
    
    # 如果用户存在，返回用户信息
    if user_id in users_db:
        return jsonify({
            "code": 200,
            "message": "success",
            "data": users_db[user_id]
        })
    
    # 如果用户不存在，返回默认用户信息
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "user_id": user_id,
            "username": f"user_{user_id}",
            "email": f"user_{user_id}@example.com",
            "age": random.randint(18, 60),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    })


@app.route('/api/user/add', methods=['POST'])
def add_user():
    """
    添加用户接口
    
    请求体（JSON）:
        {
            "username": "test_user",
            "email": "test@example.com",
            "age": 25  // 可选
        }
        
    返回:
        {
            "code": 200,
            "message": "用户创建成功",
            "data": {
                "user_id": 1001,
                "username": "test_user",
                "email": "test@example.com"
            }
        }
    """
    data = request.get_json()
    
    # 参数校验
    if not data:
        return jsonify({
            "code": 400,
            "message": "请求体不能为空",
            "data": None
        }), 400
    
    username = data.get('username')
    email = data.get('email')
    
    if not username:
        return jsonify({
            "code": 400,
            "message": "参数错误: username不能为空",
            "data": None
        }), 400
    
    if not email:
        return jsonify({
            "code": 400,
            "message": "参数错误: email不能为空",
            "data": None
        }), 400
    
    # 检查邮箱格式（简单验证）
    if '@' not in email:
        return jsonify({
            "code": 400,
            "message": "参数错误: 邮箱格式不正确",
            "data": None
        }), 400
    
    # 检查用户名是否已存在
    for user in users_db.values():
        if user.get('username') == username:
            return jsonify({
                "code": 409,
                "message": "用户已存在",
                "data": None
            }), 409
    
    # 创建用户
    user_id = generate_id()
    user_data = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "age": data.get('age', 0),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users_db[user_id] = user_data
    
    return jsonify({
        "code": 200,
        "message": "用户创建成功",
        "data": {
            "user_id": user_id,
            "username": username,
            "email": email
        }
    }), 200


@app.route('/api/message/list', methods=['GET'])
def get_message_list():
    """
    获取消息列表接口
    
    请求参数:
        page: 页码（默认1）
        page_size: 每页数量（默认10）
        
    返回:
        {
            "code": 200,
            "message": "success",
            "data": {
                "total": 25,
                "page": 1,
                "page_size": 10,
                "messages": [
                    {
                        "message_id": 1,
                        "title": "测试消息",
                        "content": "这是一条测试消息",
                        "sender_id": 1001,
                        "receiver_id": 1002,
                        "created_at": "2024-01-01 10:00:00"
                    }
                ]
            }
        }
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    # 如果消息列表为空，生成一些示例消息
    if not messages_db:
        for i in range(1, 26):
            messages_db.append({
                "message_id": i,
                "title": f"消息标题 {i}",
                "content": f"这是第 {i} 条消息的内容",
                "sender_id": random.randint(1000, 1005),
                "receiver_id": random.randint(1006, 1010),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    # 分页计算
    total = len(messages_db)
    start = (page - 1) * page_size
    end = start + page_size
    messages = messages_db[start:end]
    
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "messages": messages
        }
    })


@app.route('/api/message/send', methods=['POST'])
def send_message():
    """
    发送消息接口
    
    请求体（JSON）:
        {
            "receiver_id": 1002,
            "content": "消息内容",
            "title": "消息标题"  // 可选
        }
        
    返回:
        {
            "code": 200,
            "message": "消息发送成功",
            "data": {
                "message_id": 1
            }
        }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "code": 400,
            "message": "请求体不能为空",
            "data": None
        }), 400
    
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    
    if not receiver_id:
        return jsonify({
            "code": 400,
            "message": "参数错误: receiver_id不能为空",
            "data": None
        }), 400
    
    if not content:
        return jsonify({
            "code": 400,
            "message": "参数错误: content不能为空",
            "data": None
        }), 400
    
    # 创建消息
    message_id = len(messages_db) + 1
    message = {
        "message_id": message_id,
        "title": data.get('title', '无标题'),
        "content": content,
        "sender_id": 1001,  # 模拟发送者ID
        "receiver_id": receiver_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    messages_db.append(message)
    
    return jsonify({
        "code": 200,
        "message": "消息发送成功",
        "data": {
            "message_id": message_id
        }
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


if __name__ == '__main__':
    print("=" * 50)
    print("Mock服务启动中...")
    print("服务地址: http://127.0.0.1:5000")
    print("健康检查: http://127.0.0.1:5000/health")
    print("=" * 50)
    app.run(host='127.0.0.1', port=5000, debug=True)

