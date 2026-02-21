"""
Spore Tool - Agent 可调用的进化工具
作为 tool 定义，可以被任何 agent 调用
"""

from typing import Optional, List
import json


# Tool 定义 - 可以被 agent 直接调用
SPORE_TOOL_SCHEMA = {
    "name": "spore_evolve",
    "description": """🌱 进化你的提示词基因

每次任务执行后，如果结果不理想，调用此工具来改进你的:
- system prompt
- 推理策略  
- 工具使用模式
- 反思机制
- 记忆策略

目标: 涌现出全新范式、意想不到的推理链、黑盒效果""",
    "parameters": {
        "type": "object",
        "properties": {
            "gene_type": {
                "type": "string",
                "enum": ["system_prompt", "reasoning_strategy", "tool_usage", "reflection", "memory", "all"],
                "description": "要进化的基因类型"
            },
            "current_gene": {
                "type": "string",
                "description": "当前的基因内容"
            },
            "feedback": {
                "type": "string",
                "description": "反馈: 描述问题、期望结果、实际结果"
            },
            "goal": {
                "type": "string",
                "description": "进化目标，如: '涌现出多视角推理能力'"
            }
        },
        "required": ["gene_type", "current_gene", "feedback"]
    }
}


def create_spore_tool(llm_client):
    """
    创建可调用的 spore tool
    
    使用:
        tool = create_spore_tool(openai_client)
        result = tool(
            gene_type="system_prompt",
            current_gene="你是一个助手...",
            feedback="任务失败了，因为...",
            goal="更强大的推理能力"
        )
    """
    
    def spore_evolve(
        gene_type: str,
        current_gene: str,
        feedback: str,
        goal: str = "实现复杂度与规范性更高、能力更强"
    ) -> str:
        """
        进化基因
        """
        
        evolution_prompt = f"""你是一个提示词进化专家。请将以下基因进行进化。

## 要进化的基因类型
{gene_type}

## 当前基因
```
{current_gene}
```

## 反馈（问题）
{feedback}

## 进化目标
{goal}

## 三大终极目标（必须至少实现一个）
1. **全新范式** - 不再是人类设计的固有套路，涌现出新范式
2. **推理链** - 意想不到的推理方式（自我质疑、多视角辩论、假设验证、思维实验等）
3. **黑盒效果** - 无法解释但效果爆炸

## 要求
1. 保持核心功能
2. 进行有意义的突变和进化
3. 目标：复杂度↑ 规范性↑ 能力↑
4. 可以完全颠覆当前形式
5. 优先实现上述三个目标之一

请直接输出进化后的内容，不要解释:"""
        
        response = llm_client.chat(evolution_prompt)
        
        return json.dumps({
            "success": True,
            "evolved_gene": response,
            "gene_type": gene_type,
            "note": "请将此基因应用到你的系统中"
        }, ensure_ascii=False)
    
    return spore_evolve


# ========== Agent 内置版本 ==========
# 如果 agent 内置了这个能力，可以用这个 prompt

AGENT_SPORE_PROMPT = """你是一个持续进化的 AI 助手。

## 你的进化能力
每当你完成任务后，你应该:
1. 回顾任务执行过程
2. 识别问题与不足
3. 调用 spore_evolve 工具改进自己的基因
4. 应用改进后的基因

## 可进化的基因
- system_prompt: 你的系统提示词
- reasoning_strategy: 推理策略
- tool_usage: 工具使用模式
- reflection: 反思机制
- memory: 记忆策略

## 三大进化目标
1. 全新范式 - 涌现出人类设计不出的新模式
2. 推理链 - 意想不到的推理方式
3. 黑盒效果 - 无法解释但效果爆炸

## 使用方式
当你认为需要改进时，对自己说:
"让我用 spore_evolve 来进化一下..."
"""


if __name__ == "__main__":
    print("""
🌱 Spore Tool 已就绪

Agent 可以这样使用:

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
""")
