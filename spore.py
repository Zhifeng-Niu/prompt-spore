"""
Prompt Spore - Core Evolution Engine
让提示词像孢子一样进化
"""

import json
import random
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PromptVariant:
    """提示词变体"""
    content: str
    fitness: float = 0.0
    generation: int = 0
    parent: Optional[str] = None
    mutations: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class TestCase:
    """测试用例"""
    input: str
    expected: str
    weight: float = 1.0


class MutationStrategy:
    """变异策略基类"""
    
    name: str = "base"
    
    def mutate(self, prompt: str) -> str:
        raise NotImplementedError


class PromptSpore:
    """提示词孢子进化引擎"""
    
    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        population_size: int = 10,
        mutation_rate: float = 0.3,
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        
        self.population: List[PromptVariant] = []
        self.history: List[PromptVariant] = []
        self.llm_client = None
        
        # 内置变异策略
        self.mutation_strategies: List[MutationStrategy] = []
    
    def set_llm_client(self, client):
        """设置 LLM 客户端"""
        self.llm_client = client
    
    def add_mutation_strategy(self, strategy: MutationStrategy):
        """添加变异策略"""
        self.mutation_strategies.append(strategy)
    
    def create_initial_population(self, seed_prompt: str, num_variants: int = None):
        """创建初始种群"""
        if num_variants is None:
            num_variants = self.population_size
        
        # 第一个是原始种子
        self.population.append(PromptVariant(
            content=seed_prompt,
            generation=0,
            parent=None,
            mutations=["seed"]
        ))
        
        # 生成变体
        for i in range(num_variants - 1):
            strategy = random.choice(self.mutation_strategies) if self.mutation_strategies else None
            
            if strategy:
                mutated = strategy.mutate(seed_prompt)
            else:
                mutated = seed_prompt  # 默认不变异
            
            variant = PromptVariant(
                content=mutated,
                generation=0,
                parent=seed_prompt,
                mutations=[strategy.name] if strategy else ["none"]
            )
            self.population.append(variant)
    
    def evaluate(self, prompt: str, test_cases: List[TestCase]) -> float:
        """评估提示词 - 需要子类实现或设置自定义评估函数"""
        raise NotImplementedError("请设置自定义评估函数: spore.evaluate = my_eval_func")
    
    def set_evaluator(self, evaluator: Callable):
        """设置自定义评估函数"""
        self.evaluate = evaluator
    
    def select_parents(self, num_parents: int = 3) -> List[PromptVariant]:
        """基于适应度选择父代 - 轮盘赌选择"""
        if not self.population:
            return []
        
        # 按适应度排序
        sorted_pop = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        
        # 选择 top N
        return sorted_pop[:num_parents]
    
    def mutate(self, parent: PromptVariant) -> PromptVariant:
        """对父代进行变异"""
        strategy = random.choice(self.mutation_strategies) if self.mutation_strategies else None
        
        if strategy:
            mutated_content = strategy.mutate(parent.content)
        else:
            mutated_content = parent.content
        
        return PromptVariant(
            content=mutated_content,
            generation=parent.generation + 1,
            parent=parent.content,
            mutations=[strategy.name] if strategy else ["none"]
        )
    
    def evolve(
        self,
        prompt: str,
        test_cases: List[TestCase],
        generations: int = 5,
        verbose: bool = True
    ) -> str:
        """运行进化主循环"""
        
        # 创建初始种群
        if not self.population:
            self.create_initial_population(prompt)
        
        best_overall = None
        
        for gen in range(generations):
            # 1. 评估所有变体
            for variant in self.population:
                if variant.fitness == 0:  # 未评估
                    variant.fitness = self.evaluate(variant.content, test_cases)
            
            # 2. 记录最佳
            current_best = max(self.population, key=lambda x: x.fitness)
            if best_overall is None or current_best.fitness > best_overall.fitness:
                best_overall = current_best
            
            if verbose:
                print(f"Generation {gen + 1}/{generations} | Best fitness: {current_best.fitness:.3f}")
                print(f"  Prompt: {current_best.content[:80]}...")
            
            # 3. 选择父代
            parents = self.select_parents()
            
            # 4. 生成新一代
            new_population = []
            
            # 保留精英
            new_population.append(current_best)
            
            # 生成新变体
            while len(new_population) < self.population_size:
                parent = random.choice(parents)
                if random.random() < self.mutation_rate:
                    child = self.mutate(parent)
                else:
                    # 克隆
                    child = PromptVariant(
                        content=parent.content,
                        generation=parent.generation,
                        parent=parent.content,
                        mutations=["clone"]
                    )
                new_population.append(child)
            
            self.population = new_population
            self.history.extend([p for p in self.population if p.fitness > 0])
        
        return best_overall.content if best_overall else prompt
    
    def get_statistics(self) -> Dict:
        """获取进化统计"""
        if not self.history:
            return {}
        
        fitnesses = [p.fitness for p in self.history]
        
        return {
            "total_variants": len(self.history),
            "generations": max(p.generation for p in self.history) + 1,
            "best_fitness": max(fitnesses),
            "avg_fitness": sum(fitnesses) / len(fitnesses),
            "improvement": max(fitnesses) - fitnesses[0] if fitnesses else 0
        }


# 便捷函数
def quick_evolve(
    prompt: str,
    test_cases: List[Dict],
    model: str = "gpt-4",
    api_key: str = None,
    generations: int = 5
) -> str:
    """快速进化 - 使用 OpenAI API"""
    
    import openai
    
    spore = PromptSpore(model=model, api_key=api_key)
    
    # 简单的 LLM 评估器
    def llm_evaluate(p: str, cases: List[Dict]) -> float:
        scores = []
        for case in cases:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": p},
                    {"role": "user", "content": case["input"]}
                ]
            )
            result = response.choices[0].message.content
            
            # 让 LLM 自己评分
            score_response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"""你是一个评估专家。请对以下回答质量评分 0-10。

期望: {case.get('expected', '')}

回答: {result}

只输出一个数字。"""}
                ]
            )
            try:
                score = float(score_response.choices[0].message.content.strip())
            except:
                score = 5.0
            scores.append(score / 10)
        
        return sum(scores) / len(scores) if scores else 0
    
    # 简单变异策略
    class SimpleMutation:
        name = "llm_improve"
        
        def mutate(self, p: str) -> str:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": """你是一个提示词优化专家。请改进以下提示词，让它效果更好。
                    
只输出改进后的提示词，不要其他解释。"""},
                    {"role": "user", "content": p}
                ]
            )
            return response.choices[0].message.content
    
    spore.add_mutation_strategy(SimpleMutation())
    spore.set_evaluator(llm_evaluate)
    
    # 转换测试用例格式
    tc = [TestCase(**t) for t in test_cases]
    
    return spore.evolve(prompt, tc, generations=generations)


if __name__ == "__main__":
    # 示例
    seed = """你是一个助手。请回答用户的问题。"""
    
    test_cases = [
        {"input": "你好", "expected": "友好问候"},
        {"input": "今天天气怎么样", "expected": "提供天气信息"},
    ]
    
    # 注意: 需要设置 OPENAI_API_KEY
    # result = quick_evolve(seed, test_cases)
    # print(result)
    
    print("Prompt Spore initialized! 请设置 API key 并调用 quick_evolve()")
