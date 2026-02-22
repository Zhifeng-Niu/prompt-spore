"""
Skill Spore - 专门进化 OpenClaw Skills 的孢子

目标：
- 工程性：代码规范、错误处理、边界情况
- Workflow：逻辑清晰、稳定、一次通过
- 全新范式：涌现出意想不到的 Skill 组织方式
- 黑盒效果：无法解释但效果爆炸的实现
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class Skill:
    """Skill 结构"""
    name: str
    description: str
    workflow: str      # 工作流描述
    code: str         # 代码实现
    examples: List[str] = None
    
    
@dataclass
class EvolutionConstraints:
    """进化约束"""
    core_function_must_keep: str   # 必须保留的核心功能
    usage_pattern_must_keep: str   # 必须保留的使用方式
    cannot_add_deps: List[str] = None  # 不能添加的依赖
    
    def __post_init__(self):
        if self.cannot_add_deps is None:
            self.cannot_add_deps = []


class SkillSpore:
    """
    Skill 孢子 - 让 Skill 进化得更深、更稳
    
    三大目标：
    1. 全新范式 - 涌现出人类设计不出的 Skill 模式
    2. 黑盒效果 - 无法解释但效果爆炸的实现
    3. 一次通过 - 稳定、可靠、不需要调试
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def evolve_skill(
        self,
        skill: Skill,
        feedback: str,
        constraints: EvolutionConstraints,
        focus: str = "工程性"
    ) -> Skill:
        """
        进化 Skill
        
        Args:
            skill: 要进化的 Skill
            feedback: 问题/失败反馈
            constraints: 约束条件
            focus: 进化重点 ("工程性" / "workflow" / "all")
        
        Returns:
            进化后的新 Skill
        """
        
        evolution_prompt = f"""你是一个 Skill 进化专家。请将以下 Skill 进化到更高层次。

## 当前 Skill
名称: {skill.name}
描述: {skill.description}

工作流:
{skill.workflow}

代码:
{skill.code}

## 问题反馈
{feedback}

## 必须保留的约束
1. 核心功能: {constraints.core_function_must_keep}
2. 使用方式: {constraints.usage_pattern_must_keep}
3. 不能添加的依赖: {constraints.cannot_add_deps}

## 进化重点
{focus}

---

## 三大目标（必须至少实现一个）

### 1. 全新范式
- 涌现出人类设计不出的 Skill 组织方式
- 意想不到的内部工作流
- 跨 Skill 调用协议

### 2. 黑盒效果
- 产生无法解释但效果爆炸的实现
- 某些逻辑"不知道为什么好用但就是好用"
- 像深度学习一样——管用就行

### 3. 一次通过
- 稳定、可靠、不需要调试
- 完善的错误处理
- 周全的边界情况考虑

---

## 进化方向（工程性）

1. **代码规范** - 符合语言最佳实践
2. **错误处理** - 每一个可能的错误都要处理
3. **边界情况** - 空值、超时、权限等
4. **日志** - 关键操作要有日志
5. **可测试** - 逻辑清晰，容易测试

## 进化方向（workflow）

1. **逻辑清晰** - 每一步做什么一目了然
2. **状态管理** - 失败恢复、重试逻辑
3. **依赖顺序** - 确保前置条件
4. **结果验证** - 输出前校验

---

请输出进化后的 Skill（JSON 格式）:

```json
{{
  "name": "...",
  "description": "...",
  "workflow": "...",
  "code": "...",
  "examples": [...]
}}
```

**重要：必须确保核心功能和使用方式不变！**"""

        response = self.llm.chat(evolution_prompt)
        
        # 解析 JSON 响应
        try:
            # 尝试提取 JSON
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]
            else:
                json_str = response
            
            new_skill_data = json.loads(json_str)
            
            return Skill(
                name=new_skill_data.get("name", skill.name),
                description=new_skill_data.get("description", skill.description),
                workflow=new_skill_data.get("workflow", skill.workflow),
                code=new_skill_data.get("code", skill.code),
                examples=new_skill_data.get("examples", skill.examples)
            )
        except:
            # 如果解析失败，返回原 Skill
            return skill
    
    def evolve_skill_file(
        self,
        skill_path: str,
        feedback: str,
        focus: str = "工程性"
    ) -> Skill:
        """
        直接进化一个 Skill 文件
        """
        # 读取 Skill
        import os
        if not os.path.exists(skill_path):
            raise FileNotFoundError(f"Skill not found: {skill_path}")
        
        # 简单解析（假设是 markdown 格式）
        with open(skill_path, 'r') as f:
            content = f.read()
        
        # 提取各部分
        skill = self._parse_skill_markdown(content)
        
        # 构建约束
        constraints = EvolutionConstraints(
            core_function_must_keep=skill.description,
            usage_pattern_must_keep="使用方式和接口不变"
        )
        
        # 进化
        new_skill = self.evolve_skill(skill, feedback, constraints, focus)
        
        return new_skill
    
    def _parse_skill_markdown(self, content: str) -> Skill:
        """解析 markdown 格式的 Skill"""
        lines = content.split('\n')
        
        name = "unknown"
        description = ""
        in_workflow = False
        in_code = False
        workflow_lines = []
        code_lines = []
        
        for line in lines:
            if line.startswith('# '):
                name = line[2:].strip()
            elif '## ' in line and 'workflow' in line.lower():
                in_workflow = True
                in_code = False
            elif '## ' in line and 'code' in line.lower():
                in_code = True
                in_workflow = False
            elif in_workflow:
                workflow_lines.append(line)
            elif in_code:
                code_lines.append(line)
            elif not in_workflow and not in_code and '## ' not in line:
                if line.strip():
                    description += line.strip() + ' '
        
        return Skill(
            name=name,
            description=description.strip(),
            workflow='\n'.join(workflow_lines).strip(),
            code='\n'.join(code_lines).strip()
        )


# ========== 便捷函数 ==========

def create_skill_spore(llm_client):
    """创建 Skill Spore"""
    return SkillSpore(llm_client)


# ========== 示例 ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║         🧬 Skill Spore - Skill 进化工具                  ║
║                                                           ║
║  目标:                                                  ║
║  - 工程性: 代码规范、错误处理、边界情况                  ║
║  - Workflow: 逻辑清晰、一次通过                          ║
║  - 全新范式: 意想不到的组织方式                          ║
║  - 黑盒效果: 无法解释但效果好                           ║
║                                                           ║
║  使用:                                                  ║
║  from skill_spore import SkillSpore                      ║
║                                                           ║
║  spore = SkillSpore(llm_client)                         ║
║  new_skill = spore.evolve_skill(                        ║
║      skill=my_skill,                                    ║
║      feedback="这个 skill 有 bug...",                    ║
║      focus="工程性"                                      ║
║  )                                                      ║
╚═══════════════════════════════════════════════════════════╝
""")
