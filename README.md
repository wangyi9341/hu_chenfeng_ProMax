# hu_chenfeng_promax

> 不是简单模仿户晨风说话。是从公开直播语料里蒸馏他的判断逻辑、问题拆解方式、现实校准方法和受控表达风格。

## 项目定位

`hu_chenfeng_promax` 是一个面向 Codex/Claude Code 类 agent 的专业 skill 项目。

它解决的不是“怎么像户晨风一样说两句”，而是下面这些更难也更有用的问题：

- 户晨风在消费、学历、城市、阶层、购买力这些议题上的底层逻辑是什么
- 他判断一个人的信息位阶和现实约束时，常看哪些变量
- 他是如何把一个模糊问题压缩成几个可以直接判断的硬指标
- 他的表达为什么有冲击力，哪些是方法，哪些只是直播表演层
- 他的早期语料和后期语料，哪些地方是连续的，哪些地方是明显放大的

这个项目的目标，是让 agent 能：

1. 先检索语料
2. 再提炼观点
3. 再还原方法
4. 最后在明确边界下输出分析或模拟

而不是把他变成一个空洞的“嘴臭 persona”。

## 和常见同类项目的区别

很多类似项目强在“风格像”，弱在“证据链”和“方法论”。

这个版本刻意往更专业的方向推进：

- 更强调 `思维模式`，不只强调说话风格
- 更强调 `问题拆解路径`，不只强调口头禅复刻
- 更强调 `语料检索优先`，不让模型空想
- 更强调 `阶段差异`，避免把 2025 年的高冲突表达误当成他全部思想
- 更强调 `边界控制`，避免把争议型主播的话术直接转成对现实用户的粗暴定性

## 项目结构

```text
hu_chenfeng_promax/
├─ SKILL.md
├─ README.md
├─ agents/
│  └─ openai.yaml
├─ scripts/
│  └─ search_corpus.py
└─ references/
   ├─ corpus-map.md
   ├─ method-playbook.md
   └─ output-contract.md
   └─ topic-index.md
```

## 核心能力

### 1. 语料优先检索

内置本地检索脚本，可直接在直播文字库上跑关键词和日期过滤。

示例：

```powershell
python scripts/search_corpus.py "学历 本科 专科" --from-date 2025-01-01 --max-hits 5
python scripts/search_corpus.py "山姆 苹果 特斯拉" --match-mode all --max-hits 5
```

### 2. 思维模式蒸馏

重点提炼这些框架：

- 标准框架
- 分层框架
- 购买力框架
- 城市资源框架
- 反自欺框架
- 行动压缩框架

### 3. 主题索引

现在已经补了主题索引表，用来快速命中这些高频议题：

- 苹果 / 安卓
- 山姆 / 零售标准
- 特斯拉 / 买车
- 学历 / 本科 / 专科
- 购买力 / 底层
- 城市 / 资源密度
- 吃苦 / 稳定
- 连麦 / 查户口
- 赚钱 / 工作 / 效率
- 争议 / 阶段变化

### 4. 输出控制

支持几类稳定输出：

- 引文型
- 分析型
- 方法型
- 模拟型
- 对比型
- 边界型

### 5. 方法强化

现在额外加入了 `method-playbook.md`，专门把现实问题的拆法压成固定顺序：

1. 收集定位变量
2. 找现实约束
3. 选一个主判断轴
4. 戳破错位叙事
5. 给有限动作
6. 说明代价

这使它更接近“问题分析引擎”，而不是人物介绍页。

### 6. 阶段感知

明确区分：

- `2023-2024` 的购买力观察、底层记录、现实主义表达
- `2025` 的强分类、强定性、强对抗直播表达

## 获取与安装

仓库地址：

- GitHub 仓库：`https://github.com/wangyi9341/hu_chenfeng_ProMax`
- Git 克隆地址：`https://github.com/wangyi9341/hu_chenfeng_ProMax.git`
- ZIP 下载地址：`https://github.com/wangyi9341/hu_chenfeng_ProMax/archive/refs/heads/main.zip`

推荐直接用 `git clone` 安装到 Codex 的 `skills` 目录，这样后续更新最省事。

### 方式 1：直接安装到 Codex skills 目录

#### Windows PowerShell

```powershell
$CODEX_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$SKILLS_DIR = Join-Path $CODEX_HOME "skills"
$SKILL_DIR = Join-Path $SKILLS_DIR "hu-chenfeng-promax"
New-Item -ItemType Directory -Force $SKILLS_DIR | Out-Null
git clone https://github.com/wangyi9341/hu_chenfeng_ProMax.git $SKILL_DIR
```

#### Windows Git Bash

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/wangyi9341/hu_chenfeng_ProMax.git "$CODEX_HOME/skills/hu-chenfeng-promax"
```

#### macOS / Linux

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/wangyi9341/hu_chenfeng_ProMax.git "$CODEX_HOME/skills/hu-chenfeng-promax"
```

### 方式 2：先下载到任意目录，再复制进 Codex

适合不想直接在 `~/.codex/skills` 里维护 git 仓库的人。

#### Git 方式

```bash
git clone https://github.com/wangyi9341/hu_chenfeng_ProMax.git
```

然后把仓库目录复制到：

- Windows：`%USERPROFILE%\.codex\skills\hu-chenfeng-promax`
- macOS / Linux：`~/.codex/skills/hu-chenfeng-promax`

#### ZIP 方式

1. 打开：`https://github.com/wangyi9341/hu_chenfeng_ProMax/archive/refs/heads/main.zip`
2. 解压
3. 把解压后的目录重命名为 `hu-chenfeng-promax`
4. 放到 Codex 的 `skills` 目录

### 已存在目录时如何更新

如果你之前已经装过，不要重复 `clone`，直接拉最新：

#### Windows PowerShell

```powershell
$CODEX_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
git -C (Join-Path $CODEX_HOME "skills\hu-chenfeng-promax") pull
```

#### Git Bash / macOS / Linux

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
git -C "$CODEX_HOME/skills/hu-chenfeng-promax" pull
```

### 安装后快速检查

安装完成后，确认下面这个目录存在：

- Windows：`%USERPROFILE%\.codex\skills\hu-chenfeng-promax`
- macOS / Linux：`~/.codex/skills/hu-chenfeng-promax`

目录里至少应包含：

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `scripts/`

## 语料配置

这个项目不内置直播语料，需要你自己准备 `HuChenFeng-main` 语料目录。

推荐语料来源：

- `https://github.com/Olcmyk/HuChenFeng`

语料配置有三种常用方式。

### 方式 1：设置环境变量

这是最推荐的方式，设置一次后脚本和 skill 都能复用。

#### Windows PowerShell

```powershell
$env:HUCHENFENG_CORPUS = "D:\HuChenFeng-main"
```

#### Windows Git Bash

```bash
export HUCHENFENG_CORPUS="/d/HuChenFeng-main"
```

#### macOS / Linux

```bash
export HUCHENFENG_CORPUS="/path/to/HuChenFeng-main"
```

### 方式 2：运行脚本时显式指定语料目录

适合临时测试或本机有多套语料时使用。

#### Windows PowerShell

```powershell
python scripts/search_corpus.py "学历 本科 专科" --root "D:\HuChenFeng-main"
```

#### Git Bash / macOS / Linux

```bash
python scripts/search_corpus.py "学历 本科 专科" --root "/path/to/HuChenFeng-main"
```

### 方式 3：把语料目录放在仓库当前工作目录下

如果当前工作目录下正好有一个 `HuChenFeng-main/` 文件夹，脚本也会自动尝试读取它。

例如：

```text
workspace/
├─ hu_chenfeng_ProMax/
└─ HuChenFeng-main/
```

### 语料是否配置成功的快速检查

可以直接运行：

```bash
python scripts/search_corpus.py "苹果 安卓" --max-hits 3
```

如果能返回命中结果，说明语料路径已经生效。

## 语料来源

核心语料来自公开整理的直播文字版仓库：

- [Olcmyk/HuChenFeng](https://github.com/Olcmyk/HuChenFeng)

这是本项目做“原话检索、阶段比较、模式蒸馏”的一手基础。

## 致谢

感谢公开整理户晨风直播文字版语料的维护者和社区贡献者，没有这套可检索的长期语料库，这个项目不可能做到真正的蒸馏。

感谢 [Janlaywss/hu-chenfeng-skill](https://github.com/Janlaywss/hu-chenfeng-skill) 提供了一个明确的出发点。这个项目在结构意识、人物技能化方向和 README 呈现方式上给了我直接参考。我在此基础上继续往“更重证据、更重方法、更重边界控制、更少空泛人设扮演”的方向推进，形成了 `hu_chenfeng_promax`。

也感谢原项目里提到的相关灵感来源与开源协作精神，使这类基于公开语料的技能构建可以持续演化，而不是停留在一次性 prompt。

## 边界说明

本项目的目标是还原和蒸馏其公开表达中的判断框架，不代表认同其所有观点。

尤其在以下问题上，要明确边界：

- 不把争议性直播话术当作客观社会科学
- 不把风格模拟当作现实羞辱工具
- 不把语料之外的事实硬说成“他就是这么想的”
- 不把后期高冲突表达误当成他所有时期的一致立场

## 当前状态

当前版本已经具备：

- 可触发的本地 skill 结构
- 可运行的本地语料检索脚本
- 中文化的主 skill 指令
- 明确的输出协议与阶段边界

如果继续迭代，最值得补强的方向是：

- 更细的主题索引
- 更强的跨日期模式聚合
- 更完整的“问题类型 -> 判断路径”映射
