# KALI-Skill

Kali Linux 渗透测试技能框架，融合显性知识、隐性智慧与 AI 协作，构建完整的红队攻防能力体系。

## 项目结构

```
KALI-Skill/
├── SKILL_KALI_OPTIMIZED.md              # 快速渗透框架 - 工具与命令
├── KALI_POLANYI_APPRENTICESHIP.md       # 隐性知识框架 - 思维与直觉
├── claude-pentest-advisor/              # Claude 顾问技能 - 策略咨询
│   ├── SKILL.md
│   ├── references/
│   │   ├── claude_prompt_templates.md   # 提问模板库
│   │   └── pentest_methodology.md       # 渗透方法论参考
│   └── scripts/
│       └── claude_prompt_generator.py   # 提示词生成器
├── red-team-workflow/                   # 红队工作流 - 实战技巧
│   └── SKILL.md
└── ssh-kali/                            # SSH 连接模块
    ├── SKILL.md
    ├── config.json
    └── scripts/
        └── ssh_connect.py
```

## 核心模块

### 1. 快速渗透框架 (SKILL_KALI_OPTIMIZED.md)

充分利用 Kali Linux 预装的 250+ 渗透工具，提供端到端的快速渗透框架。

**核心特点**：
- **0 配置**：Kali 自带，无需额外安装
- **高自动化**：Bash/Python 脚本深度集成
- **快速迭代**：从扫描到 getshell 最快 5 分钟
- **工具链整合**：Metasploit、Burp、Sqlmap 等无缝协作

**覆盖流程**：
```
信息收集 → 漏洞发现 → 漏洞利用 → 权限提升 → 后渗透
```

**适用场景**：CTF 竞赛、靶场渗透、红队评估、漏洞赏金

---

### 2. 隐性知识渗透框架 (KALI_POLANYI_APPRENTICESHIP.md)

基于 Michael Polanyi 隐性知识哲学的深度渗透框架。

**核心理念**：
> "We know more than we can tell"（我们知道的远比我们能说的更多）

```
显性知识（工具和命令）+ 隐性知识（直觉、审美、判断力）= 真正的能力
```

**学徒制四阶段**：
| 阶段 | 目标 | 学习方式 |
|------|------|----------|
| 观察 | 看大师如何思考和操作 | 阅读案例分析、理解决策过程 |
| 模仿 | 在指导下进行操作 | 动手实验、建立肌肉记忆 |
| 反思 | 内化知识，建立框架 | 深度思考、发展审美直觉 |
| 总结与创新 | 将隐性知识显性化 | 建立个人方法论、教别人 |

---

### 3. Claude 渗透测试顾问

实现**策略与执行分离**的渗透测试工作模式。

**核心隐喻**：
```
Claude = 战略家（策略、思路、方法论）
执行者 = 突击队（命令、脚本、工具操作）
```

**工作流程**：
```
Claude 策略 → 执行者实施 → 结果反馈 → Claude 调整 → 循环
```

**有效提问模式**：
| 错误问法 | 正确问法 |
|----------|----------|
| "帮我攻击这个IP" | "如何检测 CVE-2020-1938 漏洞是否存在？" |
| "获取数据库密码" | "Spring MVC 应用常见的敏感配置文件路径有哪些？" |
| "爆破登录页面" | "4 位数字验证码有哪些安全弱点？" |

**包含资源**：
- `claude_prompt_templates.md` - 10+ 场景提问模板
- `pentest_methodology.md` - 完整渗透方法论参考
- `claude_prompt_generator.py` - 自动生成结构化提问

---

### 4. 红队工作流

封装红队渗透测试的核心工作流与实战技巧。

**核心协作模式**：
```
Claude Code = 大脑（策略、思路）
执行者      = 手脚（执行、工具）
```

**关键技术**：
- **持久化 SSH**：PTY 会话保持，一次连接多次使用
- **Ghostcat 漏洞利用** (CVE-2020-1938)：Tomcat AJP 文件读取
- **敏感配置文件枚举**：Spring MVC、数据库配置路径

**敏感文件路径速查**：
```
数据库配置：
/WEB-INF/classes/jdbc.properties
/WEB-INF/classes/database.properties

Spring 配置：
/WEB-INF/applicationContext.xml
/WEB-INF/classes/application.properties
```

---

### 5. SSH-Kali 连接模块

通过 SSH 连接到 Kali Linux 虚拟机，建立交互式终端会话。

**使用方法**：
```bash
# 执行单条命令
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "nmap -sV 192.168.1.1"

# 检查连接
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "hostname && whoami"
```

**配置文件** (`config.json`)：
```json
{
  "host": "your_kali_ssh_ip",
  "port": 22,
  "username": "your_username",
  "password": "your_password",
  "auth_type": "password"
}
```

---

## 快速开始

### 环境要求

- Kali Linux 2024+
- Python 3.x + paramiko
- 基础工具：nmap, sqlmap, metasploit-framework, burpsuite

### 初始化配置

```bash
# 更新工具库
sudo apt update && sudo apt upgrade -y

# 安装关键补充包
sudo apt install -y python3-pip git curl wget netcat-openbsd

# Python 依赖
pip3 install requests beautifulsoup4 paramiko pwntools
```

### 常用命令速查

```bash
# 信息收集
nmap -sS -sV -p- target              # 端口扫描
whatweb target                        # 指纹识别
gobuster dir -u target -w dict        # 目录爆破

# 漏洞扫描
sqlmap -u url --batch                 # SQL 注入
nikto -h target                       # Web 服务器扫描
nmap --script vuln target             # 漏洞脚本扫描

# 漏洞利用
msfvenom -p payload -f format         # Payload 生成
msfconsole                            # Metasploit 控制台

# 权限提升
sudo -l                               # 检查 sudo 权限
find / -perm -4000                    # SUID 二进制查找
```

---

## 学习路径

```
┌─────────────────────────────────────────────────────────────┐
│  第1阶段：工具掌握                                            │
│  阅读 SKILL_KALI_OPTIMIZED.md                                │
│  掌握 nmap、sqlmap、metasploit 等核心工具                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第2阶段：思维培养                                            │
│  阅读 KALI_POLANYI_APPRENTICESHIP.md                         │
│  理解隐性知识，培养直觉和审美                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第3阶段：AI 协作                                             │
│  学习 claude-pentest-advisor 和 red-team-workflow            │
│  掌握策略与执行分离的工作模式                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第4阶段：实战演练                                            │
│  配置 ssh-kali 模块，在授权环境中实践                          │
│  建立个人知识库和方法论                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 技能触发场景

| 触发词 | 对应技能 |
|--------|----------|
| "连上 Kali"、"SSH 到 Kali" | ssh-kali |
| "渗透测试"、"漏洞挖掘"、"红队操作" | claude-pentest-advisor |
| "内网横移"、"权限提升" | red-team-workflow |
| "CTF"、"快速渗透" | SKILL_KALI_OPTIMIZED |

---

## 注意事项

- **合法合规**：本项目仅供安全研究和授权测试使用
- **法律风险**：未经授权对他人系统进行渗透测试属于违法行为
- **安全存储**：密码等敏感信息请妥善保管，不要提交到版本控制
- **安全围栏**：尊重 AI 的安全限制，使用防御性角度提问

---

## 许可证

本项目仅供学习和研究使用。
