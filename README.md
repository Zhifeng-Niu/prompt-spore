# 🌱 Prompt Spore

> 让提示词像孢子一样进化 —— AI Prompt Evolution Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## 🎯 核心理念

**Prompt Spore** 是一个让提示词能够自主进化、自我迭代的系统。它的核心思想来源于遗传算法，但专为提示词优化设计。

```
种子(Spore) → 变异(Mutate) → 评估(Evaluate) → 选择(Select) → 进化(Evolve)
```

### 三大目标

1. **全新类型的 prompt 模板** —— 进化出人类未曾设计的提示范式
2. **意想不到的推理链** —— 涌现出超越人类的思考方式
3. **"黑盒" prompt** —— 产生无法解释但效果惊人的提示词

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/Zhifeng-Niu/prompt-spore.git
cd prompt-spore
pip install -r requirements.txt
```

### 使用

```python
from spore import PromptSpore

# 初始化（需要 LLM API）
spore = PromptSpore(
    model="gpt-4",
    api_key="your-api-key"
)

# 播种一个初始提示词种子
initial_prompt = """你是一个代码审查专家。审查以下代码的问题。"""

# 运行进化
best_prompt = spore.evolve(
    prompt=initial_prompt,
    test_cases=[
        {"input": "def foo():\n    return 1/0", "expected": "发现除零错误"}
    ],
    generations=5
)

print(best_prompt)
```

---

## 🧬 架构

```
prompt-spore/
├── spore.py              # 核心引擎
├── mutation/             # 变异策略
│   ├── lexical.py        # 词法变异
│   ├── structural.py     # 结构变异
│   ├── llm_generated.py  # LLM 生成变异
│   └── meta.py          # 元变异
├── evaluator.py          # 评估器
├── population.py         # 种群管理
├── examples/             # 示例
└── tests/               # 测试
```

---

## 🔄 变异策略

| 策略 | 描述 |
|------|------|
| **词法变异** | 替换关键词/短语 |
| **结构变异** | 调整提示词结构 |
| **风格变异** | 改变语气/风格 |
| **逻辑变异** | 改进推理链 |
| **LLM 变异** | 用 LLM 生成改进版本 |
| **元变异** | 优化变异策略本身 |

---

## 📊 评估维度

```
评估分数 = 任务完成度 × w₁ + 输出质量 × w₂ + 复杂度 × w₃ + 规范度 × w₄
```

---

## 🌟 高级特性

- **跨域授粉**：不同领域的孢子交换基因
- **思想病毒**：孢子在不同 agent 间传播
- **涌现式进化**：自动涌现新的提示模式

---

## 📝 License

MIT License - 欢迎开源贡献！

---

**让提示词像生命一样进化** 🧬
