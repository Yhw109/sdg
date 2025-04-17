from sklearn.neural_network import MLPRegressor
from openai import OpenAI


def get_llm_analysis():

    client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

    prompt = f"""
#任务描述：
以下是一份代码原数据的质量评估分析，包括11个维度。每个维度有一个0-100的打分，请你基于这些分数评估这份代码源数据的质量，然后返回你认为对数据质量影响最大的5个维度。
#格式要求：
返回一个Python列表，包括5个影响最大的维度。
"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    metrics = extract_metrics(response)
    print(response.choices[0].message.content)
    return metrics
    #     [
    #         "配置项多样性",  # 权重1.0
    #         "图像与渲染截图的SSIM",  # 权重0.8
    #         "数据量",  # 权重0.7
    #         "联合重复",  # 权重0.5
    #         "类型均衡性"  # 权重0.4
    #     ]

class QualityPredictor:
    """
    构建一个多层感知机（MLP）模型，用于预测数据质量分数。
    """
    def __init__(self):
        """
        初始化 MLPRegressor 模型。
        """
        self.model = MLPRegressor(hidden_layer_sizes=(11, 11), max_iter=500)

    def predict(self, X):
        """
        使用模型进行预测。
        参数：
            X: 输入特征数组，形状为 (10,)。
        返回值：
            预测结果。
        """
        return self.model.predict([X])

def calculate_top_metrics(dataset_quality_scores):
    """
    计算数据集的质量得分，并返回加权后的前三个最高得分指标。
    参数：
        dataset_quality_scores: 字典，包含所有 10 个二级指标的评分。
    返回值：
        前三个最高得分指标的列表。
    """
    # 获取 LLM 分析结果
    llm_result = get_llm_analysis()
    weights = [1.0, 0.8, 0.7, 0.5, 0.4]
    llm_weights = {}
    for metric, weight in zip(llm_result, weights):
        llm_weights[metric] = weight * 0.6

    # 定义所有 10 个二级指标的完整列表
    all_metrics = [
        "语法检测", "可渲染性检测", "配置项完整检测",
        "图像与渲染截图的SSIM", "图像OCR检测的文字与配置项的余弦相似度",
        "图表类型均衡性", "配置项多样性",
        "代码重复", "图像重复", "联合重复",
        "数据量"
    ]

    # 提取输入特征数组 X
    X = [dataset_quality_scores[metric] for metric in all_metrics]

    # 使用神经网络预测质量分数
    predictor = QualityPredictor()
    nn_scores = predictor.predict(X)

    # 创建指标-得分映射
    metric_score_map = {metric: score for metric, score in zip(all_metrics, nn_scores)}

    # 计算加权分数
    weighted_scores = {}

    for metric, weight in llm_weights.items():
        weighted_scores[metric] = llm_weights[metric] + metric_score_map[metric] * 0.4

    # 排序并返回前三
    sorted_metrics = sorted(weighted_scores.items(), key=lambda x: -x[1])
    return [metric for metric, _ in sorted_metrics[:3]]

# 示例调用
if __name__ == "__main__":
    # 示例数据集评分
    dataset_quality_scores = {
        "语法检测": 0.9,
        "可渲染性检测": 0.85,
        "配置项完整检测": 0.88,
        "图像与渲染截图的SSIM": 0.92,
        "图像OCR检测的文字与配置项的余弦相似度": 0.87,
        "图表类型均衡性": 0.89,
        "配置项多样性": 0.91,
        "代码重复": 0.78,
        "图像重复": 0.82,
        "联合重复": 0.86,
        "数据量": 0.95
    }

    # 计算前三个最高得分指标
    top_metrics = calculate_top_metrics(dataset_quality_scores)
    print("Top 3 Metrics:", top_metrics)
