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

## 🧬 Agent 自我进化

### 作为 Tool 使用

```python
from spore_tool import create_spore_tool, SPORE_TOOL_SCHEMA

# 创建 tool
evolve_tool = create_spore_tool(llm_client)

# 调用进化
result = evolve_tool(
    gene_type="system_prompt",
    current_gene="你是一个有帮助的助手...",
    feedback="用户说我回答太简短，没有深入分析",
    goal="涌现出深度思考能力"
)
```

### 效果示例

**贝贝的进化轨迹：**

```
v1.0 → v2.0 → v3.0 → v4.0 → v5.0
  │      │      │      │      │
  ▼      ▼      ▼      ▼      ▼
基本    多元    AI原生  概念   玄学
助手    思考    推理    创造   大师
```

详见 [self-evolution.md](./self-evolution.md)

---

## 🧠 架构

```
prompt-spore/
├── spore.py              # 核心引擎
├── agent_spore.py        # Agent 自我进化工具
├── spore_tool.py         # 可被 agent 调用的 Tool
├── self-evolution.md     # 🧪 贝贝进化实验
├── evolution-demo.md     # 进化过程记录
└── README.md
```

---

## 📝 License

MIT License - 欢迎开源贡献！

---

**让提示词像生命一样进化** 🧬🦋
