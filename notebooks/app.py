from flask import Flask, request, jsonify, render_template, Response
import pandas as pd
from recommender import FinancialRecommender
import logging
import traceback
from ollama import OllamaAPI
import joblib
import os
from models import db, Comment

# 设置日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
ollama = OllamaAPI()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize db with app
db.init_app(app)

# 存储每个会话的消息历史
chat_histories = {}
# 初始化推荐系统
recommender = None

# 确保在所有路由之前初始化数据库表
with app.app_context():
    db.create_all()  # 只创建不存在的表
    db.session.commit()

def init_recommender():
    global recommender
    try:
        logger.info("正在初始化推荐系统...")
        model_path = 'models/financial_recommender.joblib'
        
        # 如果存在已训练的模型文件，直接加载
        if os.path.exists(model_path):
            logger.info("加载已存在的模型...")
            recommender = joblib.load(model_path)
            logger.info("模型加载完成")
            return True
            
        # 如果没有已训练的模型，才进行训练
        logger.info("未找到已训练模型，开始训练新模型...")
        data = pd.read_csv('data/CUST_INVESTMENT.csv')
        
        if data.empty:
            raise ValueError("训练数据为空")
        
        logger.info(f"加载了 {len(data)} 条训练数据")
        
        X = data.drop(['CODE'], axis=1)
        y = data['CODE']
        
        recommender = FinancialRecommender()
        recommender.train(X, y)
        
        if not recommender.is_fitted:
            raise ValueError("模型训练失败")
            
        # 确保模型目录存在
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        # 保存训练好的模型
        joblib.dump(recommender, model_path)
        logger.info("模型训练完成并保存")
        
        return True
        
    except Exception as e:
        logger.error(f"推荐系统初始化失败: {str(e)}")
        logger.error(traceback.format_exc())
        return False

# 在应用启动时初始化推荐系统
init_recommender()

@app.route('/api/recommend', methods=['POST'])
def recommend_api():
    try:
        global recommender
        # 检查推荐系统是否已初始化
        if recommender is None or not recommender.is_fitted:
            # 尝试重新初始化
            if not init_recommender():
                raise ValueError("推荐系统未正确初始化且无法重新初始化")
            
        # 获取用户输入数据
        user_data = request.json
        logger.info(f"收到推荐请求，用户数据: {user_data}")
        
        if not user_data:
            raise ValueError("未收到有效的请求数据")
        
        # 数据验证和转换
        user_data = validate_and_transform_data(user_data)
        
        # 转换为DataFrame
        user_df = pd.DataFrame([user_data])
        logger.info(f"转换后的DataFrame: {user_df}")
        
        # 获取推荐结果
        recommendations = recommender.recommend(user_df)
        logger.info(f"推荐结果: {recommendations}")
        
        return jsonify({
            'status': 'success',
            'data': recommendations,
            'message': '推荐成功'
        })
        
    except ValueError as e:
        logger.error(f"数据验证错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f"推荐失败: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': f'推荐失败: {str(e)}'
        }), 500

def validate_and_transform_data(data):
    """验证和转换用户输入数据"""
    required_fields = [
        'AGE', 'GENDER', 'MARITAL', 'HAVE_CHILD', 'EDU_LEVEL',
        '3YEAR_RETURN', 'STD_DEV', 'DIVIDEND', 'ASSET_CLASS'
    ]
    
    # 检查数据是否为空
    if not data:
        logger.error('请求数据为空')
        raise ValueError('请求数据为空')
    
    # 检查必需字段
    for field in required_fields:
        if field not in data:
            logger.error(f'缺少必要字段: {field}')
            raise ValueError(f'缺少必要字段: {field}')
        if data[field] is None:
            logger.error(f'字段 {field} 的值不能为空')
            raise ValueError(f'字段 {field} 的值不能为空')
    
    # 转换数值字段
    try:
        data['AGE'] = float(data['AGE'])
        data['3YEAR_RETURN'] = float(data['3YEAR_RETURN'])
        data['STD_DEV'] = float(data['STD_DEV'])
        data['DIVIDEND'] = float(data['DIVIDEND'])
    except (ValueError, TypeError) as e:
        logger.error(f'数值字段格式错误: {e}')
        raise ValueError('数值字段格式错误')
    
    # 验证数值范围
    if not (20 <= data['AGE'] <= 70):
        logger.error('年龄必须在20-70岁之间')
        raise ValueError('年龄必须在20-70岁之间')
    
    # 验证分类字段的值
    valid_gender = ['M', 'F']
    valid_marital = ['SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED']
    valid_have_child = ['Y', 'N']
    valid_edu_level = ['PRIMARY', 'SECONDARY', 'UNIVERSITY', 'POSTGRADUATE']
    valid_asset_class = [
        'Equity Developed Market',
        'Equity Developing Market',
        'Fixed Income',
        'Multi Asset'
    ]
    
    if data['GENDER'] not in valid_gender:
        raise ValueError('无效的性别值')
    if data['MARITAL'] not in valid_marital:
        raise ValueError('无效的婚姻状况值')
    if data['HAVE_CHILD'] not in valid_have_child:
        raise ValueError('无效的子女状况值')
    if data['EDU_LEVEL'] not in valid_edu_level:
        raise ValueError('无效的教育水平值')
    if data['ASSET_CLASS'] not in valid_asset_class:
        raise ValueError('无效的资产类别值')
    
    logger.info(f'数据验证通过: {data}')
    return data


# 首页
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/recommend')
def recommend_page():
    return render_template('recommend.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/api')
def api_docs():
    return render_template('api.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # 获取或创建会话历史
        session_id = request.headers.get('X-Session-ID', 'default')
        if session_id not in chat_histories:
            chat_histories[session_id] = []
            
        # 添加用户消息到历史
        chat_histories[session_id].append({
            "role": "user",
            "content": question
        })

        # 获取可用模型
        models = ollama.list_models()
        if not models:
            return jsonify({'error': 'No models available'}), 500
            
        model_name = models[0]['name']  # 使用第一个可用模型
        
        # 发送聊天请求并获取响应
        response = ollama.chat(
            model_name=model_name,
            messages=chat_histories[session_id],
            stream=False  # 对于Web API,禁用流式响应
        )
        
        # 添加助手响应到历史
        if response:
            chat_histories[session_id].append({
                "role": "assistant",
                "content": response
            })
            
        return jsonify({
            'answer': response or '抱歉,我现在无法回答这个问题。'
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

# 获取所有顶级评论
@app.route('/api/comments', methods=['GET'])
def get_comments():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 查询顶级评论（没有父评论的评论）
        comments = Comment.query.filter_by(parent_id=None)\
            .order_by(Comment.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
            
        return jsonify({
            'comments': [comment.to_dict() for comment in comments.items],
            'total': comments.total,
            'pages': comments.pages,
            'current_page': comments.page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 添加新评论
@app.route('/api/comments', methods=['POST'])
def add_comment():
    try:
        data = request.json
        
        if not data.get('content') or not data.get('author'):
            return jsonify({'error': '内容和作者不能为空'}), 400
            
        comment = Comment(
            author=data['author'],
            content=data['content'],
            parent_id=data.get('parent_id')  # 如果是回复，则包含父评论ID
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify(comment.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 点赞评论
@app.route('/api/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    try:
        comment = Comment.query.get_or_404(comment_id)
        comment.likes += 1
        db.session.commit()
        return jsonify({'likes': comment.likes})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 讨论区
@app.route('/discussion')
def discussion():
    return render_template('discussion.html')

# 启动API
if __name__ == '__main__':
    # 使用 80 端口（需要管理员权限）
    #app.run(host='0.0.0.0', port=80, debug=True)
    
    # 或者使用 8080 端口（不需要管理员权限）
    app.run(host='0.0.0.0', port=8080, debug=True)

@app.route('/test-db')
def test_db():
    try:
        # 测试数据库连接
        db.session.execute('SELECT 1')
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection failed: {str(e)}'

