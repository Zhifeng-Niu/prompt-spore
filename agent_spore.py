"""
Agent Self-Evolution Tool
让 Agent 可以用这个工具来进化自己的"基因"
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class EvolutionFeedback:
    """进化反馈 - 描述需要改进的点"""
    task: str              # 什么任务
    expected: str          # 期望结果
    actual: str            # 实际结果
    problem: str           # 问题描述
    severity: int = 1      # 严重程度 1-5


@dataclass
class AgentGene:
    """Agent 的基因片段"""
    name: str              # 基因名 (如: system_prompt, reasoning_strategy)
    current: str           # 当前状态
    description: str       # 描述


class AgentSpore:
    """
    Agent 自我进化孢子
    
    使用方式:
        from agent_spore import AgentSpore
        
        spore = AgentSpore(llm_client=your_llm)
        
        # 方式1: 进化整个 Agent
        new_genes = spore.evolve_agent(
            genes=[
                AgentGene("system_prompt", current_system_prompt, "你的system prompt"),
                AgentGene("reasoning", current_reasoning_style, "推理策略"),
            ],
            feedback=[
                EvolutionFeedback("...", "...", "...", "..."),
            ]
        )
        
        # 方式2: 只进化特定基因
        improved = spore.evolve_gene(
            gene=AgentGene("system_prompt", my_prompt, "..."),
            feedback=[...],
            goal="涌现出全新的推理模式"
        )
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    # ========== 核心进化方法 ==========
    
    def evolve_agent(
        self,
        genes: List[AgentGene],
        feedback: List[EvolutionFeedback],
        goal: str = "实现复杂度与规范性更高、能力更强",
        max_iterations: int = 3
    ) -> List[AgentGene]:
        """
        进化整个 Agent 的所有基因
        
        Returns:
            进化后的新基因列表
        """
        
        # 构建进化上下文
        context = self._build_evolution_context(genes, feedback, goal)
        
        # 迭代进化
        current_genes = genes
        
        for i in range(max_iterations):
            # 生成新基因
            new_genes = self._generate_evolved_genes(
                current_genes, 
                context,
                iteration=i+1
            )
            
            # 评估新基因
            if self._evaluate_genes(new_genes, feedback):
                current_genes = new_genes
                print(f"✅ Iteration {i+1}: 进化成功!")
            else:
                print(f"⚠️ Iteration {i+1}: 进化效果不佳，保留原基因")
                break
        
        return current_genes
    
    def evolve_gene(
        self,
        gene: AgentGene,
        feedback: List[EvolutionFeedback],
        goal: str = "涌现出意想不到的新能力"
    ) -> AgentGene:
        """
        进化单个基因
        
        Args:
            gene: 要进化的基因
            feedback: 反馈列表
            goal: 进化目标
        
        Returns:
            进化后的新基因
        """
        
        mutation_prompt = f"""你是一个提示词进化专家。你的任务是把以下"基因"进化到更高层次。

## 当前基因
```
{gene.description}:
{gene.current}
```

## 反馈（需要改进的问题）
{self._format_feedback(feedback)}

## 进化目标
{goal}

## 三大终极目标（必须至少实现一个）
1. 全新范式：涌现出人类设计不出的新模式
2. 推理链：发展出"自我质疑"、"多视角辩论"等推理方式
3. 黑盒效果：产生无法解释但效果爆炸的提示词

## 要求
1. 保持原基因的核心功能
2. 在此基础上进行突变和进化
3. 目标：复杂度↑ 规范性↑ 能力↑
4. 可以完全颠覆当前形式

请输出进化后的基因（只输出内容，不要解释）:
"""
        
        response = self.llm.chat(mutation_prompt)
        
        return AgentGene(
            name=gene.name,
            current=response,
            description=gene.description
        )
    
    # ========== 内部方法 ==========
    
    def _build_evolution_context(
        self, 
        genes: List[AgentGene], 
        feedback: List[EvolutionFeedback],
        goal: str
    ) -> str:
        """构建进化上下文"""
        
        genes_desc = "\n".join([
            f"- {g.name}: {g.description}\n  当前: {g.current[:200]}..."
            for g in genes
        ])
        
        feedback_desc = self._format_feedback(feedback)
        
        return f"""
## Agent 当前基因
{genes_desc}

## 反馈
{feedback_desc}

## 进化目标
{goal}
"""
    
    def _format_feedback(self, feedback: List[EvolutionFeedback]) -> str:
        """格式化反馈"""
        return "\n".join([
            f"""
### 反馈 {i+1}
- 任务: {f.task}
- 期望: {f.expected}
- 实际: {f.actual}
- 问题: {f.problem}
- 严重程度: {f.severity}/5
"""
            for i, f in enumerate(feedback)
        ])
    
    def _generate_evolved_genes(
        self,
        genes: List[AgentGene],
        context: str,
        iteration: int
    ) -> List[AgentGene]:
        """生成进化后的基因"""
        
        prompt = f"""你是 Agent 基因进化引擎。请在第 {iteration} 轮迭代中进化以下基因。

{context}

## 三大终极目标
1. **全新范式** - 不再是人类设计的固有套路，涌现出新范式
2. **推理链** - 意想不到的推理方式（自我质疑、多视角辩论、假设验证等）
3. **黑盒效果** - 无法解释但效果爆炸

## 输出格式
请为每个基因输出进化后的版本:

### 基因1: [基因名]
[进化后的内容]

### 基因2: [基因名]
[进化后的内容]
...
"""
        
        response = self.llm.chat(prompt)
        
        # 解析响应，生成新基因
        # 这里需要简单的解析逻辑
        evolved_genes = []
        
        # 简化处理：假设返回格式正确
        current_name = None
        current_content = []
        
        for line in response.split('\n'):
            if line.startswith('### 基因'):
                if current_name and current_content:
                    evolved_genes.append(AgentGene(
                        name=current_name,
                        current='\n'.join(current_content),
                        description=''
                    ))
                # 提取基因名
                current_name = line.split(':')[1].strip() if ':' in line else 'unknown'
                current_content = []
            elif line.strip():
                current_content.append(line.strip())
        
        # 最后一个基因
        if current_name and current_content:
            evolved_genes.append(AgentGene(
                name=current_name,
                current='\n'.join(current_content),
                description=''
            ))
        
        # 如果解析失败，返回原基因
        if not evolved_genes:
            return genes
        
        return evolved_genes
    
    def _evaluate_genes(
        self,
        genes: List[AgentGene],
        feedback: List[EvolutionFeedback]
    ) -> bool:
        """
        评估进化后的基因是否有改进
        这里可以调用 LLM 来判断
        """
        
        # 简化版本：总是接受进化结果
        # 实际可以设计更复杂的评估逻辑
        return True


# ========== 便捷函数 ==========

def create_feedback(
    task: str,
    expected: str,
    actual: str,
    problem: str,
    severity: int = 3
) -> EvolutionFeedback:
    """创建反馈的便捷函数"""
    return EvolutionFeedback(
        task=task,
        expected=expected,
        actual=actual,
        problem=problem,
        severity=severity
    )


# ========== 示例使用 ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║         🌱 Agent Spore - 自我进化工具                     ║
║                                                           ║
║  使用示例:                                                ║
║                                                           ║
║  from agent_spore import AgentSpore, AgentGene, create_feedback
║                                                           ║
║  spore = AgentSpore(llm_client=your_llm)                ║
║                                                           ║
║  # 定义当前基因                                           ║
║  genes = [                                               ║
║      AgentGene(                                          ║
║          name="system_prompt",                          ║
║          current="你是一个有用的助手",                   ║
║          description="Agent的系统提示词"                 ║
║      ),                                                  ║
║  ]                                                       ║
║                                                           ║
║  # 提供反馈                                               ║
║  feedback = [                                            ║
║      create_feedback(                                    ║
║          task="处理复杂问题",                             ║
║          expected="深度分析并给出方案",                   ║
║          actual="简单回答，没有分析",                     ║
║          problem="缺乏深度思考模式"                      ║
║      ),                                                  ║
║  ]                                                       ║
║                                                           ║
║  # 进化!                                                 ║
║  new_genes = spore.evolve_agent(genes, feedback)        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
