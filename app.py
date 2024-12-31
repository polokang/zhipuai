from flask import Flask, request, jsonify
from zhipuai import ZhipuAI
import requests

app = Flask(__name__)

# 初始化智谱AI客户端
client = ZhipuAI(api_key='ab1be9541d6f4cbba1101411d46910ed.GjRZocSAbS05jksR')  # 替换成您的API key

@app.route('/ocr', methods=['POST'])
def extract_text():
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or 'image_url' not in data:
            return jsonify({
                'success': False,
                'error': '请提供image_url参数'
            }), 400
            
        image_url = data['image_url']
        
        # 调用智谱AI的GLM-4V模型
        response = client.chat.completions.create(
            model='glm-4v-flash',
            messages=[{
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': '请提取这张图片中的所有文字内容，只需要返回文字，不需要其他解释。'},
                    {'type': 'image_url', 'image_url': {'url': image_url}}
                ]
            }]
        )
        
        # 提取返回的文本
        extracted_text = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'text': extracted_text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)