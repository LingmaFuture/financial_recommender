import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialRecommender:
    def __init__(self):
        # 定义特征列
        self.numeric_features = ['AGE', '3YEAR_RETURN', 'STD_DEV', 'DIVIDEND']
        self.categorical_features = ['GENDER', 'MARITAL', 'HAVE_CHILD', 'EDU_LEVEL', 'ASSET_CLASS']
        
        # 初始化预处理器和编码器
        self.preprocessor = None
        self.label_encoder = None
        self.is_fitted = False
        
        # 加载产品数据以获取产品数量
        try:
            data = pd.read_csv('data/CUST_INVESTMENT.csv')
            self.n_products = len(data['CODE'].unique())
        except Exception as e:
            logger.warning(f"Could not determine number of products: {e}")
            self.n_products = 10
        
        # 创建模型
        self.model = self._build_model()
    
    def _create_preprocessor(self):
        """创建特征预处理器"""
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)
        
        return ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)
            ])
    
    def _build_model(self):
        """构建深度学习模型"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(self.n_products, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, X, y):
        """训练模型"""
        try:
            logger.info("开始训练模型...")
            
            # 创建并拟合预处理器
            self.preprocessor = self._create_preprocessor()
            X_processed = self.preprocessor.fit_transform(X)
            
            # 创建并拟合标签编码器
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
            
            # 训练模型
            history = self.model.fit(
                X_processed, y_encoded,
                epochs=50,
                batch_size=32,
                validation_split=0.2,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        patience=5,
                        restore_best_weights=True
                    )
                ]
            )
            
            # 标记为已训练
            self.is_fitted = True
            
            logger.info("模型训练完成")
            return history
            
        except Exception as e:
            logger.error(f"模型训练失败: {str(e)}")
            raise
    
    def predict(self, user_data):
        """预测推荐产品"""
        try:
            if not self.is_fitted:
                raise ValueError("Model is not fitted yet. Call 'train' before making predictions.")
                
            logger.info(f"预处理用户数据: {user_data}")
            # 预处理用户数据
            X_processed = self.preprocessor.transform(user_data)
            logger.info(f"预处理后的数据形状: {X_processed.shape}")
            
            # 获取预测结果
            predictions = self.model.predict(X_processed)
            logger.info(f"预测结果形状: {predictions.shape}")
            
            return predictions
            
        except Exception as e:
            logger.error(f"预测失败: {str(e)}")
            raise
    
    def recommend(self, user_data, top_k=5):
        """为用户推荐前K个产品"""
        try:
            # 预测
            predictions = self.predict(user_data)
            
            # 获取前K个推荐产品的索引
            top_indices = np.argsort(predictions[0])[-top_k:][::-1]
            
            # 将索引转换回产品代码
            recommended_products = self.label_encoder.inverse_transform(top_indices)
            
            # 获取对应的置信度分数
            confidence_scores = predictions[0][top_indices]
            
            return {
                'recommended_products': recommended_products.tolist(),
                'confidence_scores': confidence_scores.tolist()
            }
        except Exception as e:
            print(f"Recommendation error: {str(e)}")
            raise