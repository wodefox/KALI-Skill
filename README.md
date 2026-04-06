# KALI-Skill

Kali Linux 渗透测试技能框架，包含完整的渗透测试工作流和隐性知识传承体系。

## 项目结构

```
KALI-Skill/
├── SKILL_KALI_OPTIMIZED.md       # Kali Linux Web 渗透技能 - 快速渗透框架
├── KALI_POLANYI_APPRENTICESHIP.md # 隐性知识渗透框架 - 学徒制学习体系
└── ssh-kali/                     # SSH 连接技能模块
    ├── SKILL.md                  # 技能说明文档
    ├── config.json               # SSH 连接配置
    └── scripts/
        └── ssh_connect.py        # SSH 连接脚本
```

## 核心模块

### 1. 快速渗透框架 (SKILL_KALI_OPTIMIZED.md)

充分利用 Kali Linux 预装的 250+ 渗透工具，提供端到端的快速渗透框架。

**核心特点**：
- 0 配置：Kali 自带，无需额外安装
- 高自动化：Bash/Python 脚本深度集成
- 快速迭代：从扫描到 getshell 最快 5 分钟
- 工具链整合：充分利用 Metasploit、Burp、Sqlmap 等

**覆盖流程**：
```
信息收集 → 漏洞发现 → 漏洞利用 → 权限提升 → 后渗透
```

**适用场景**：
- CTF Web 题目快速通关
- 实际靶场渗透
- 红队评估
- 漏洞赏金计划

### 2. 隐性知识渗透框架 (KALI_POLANYI_APPRENTICESHIP.md)

基于 Michael Polanyi 隐性知识哲学的深度渗透框架，强调"我知道的远比我能说的更多"。

**核心理念**：
- 显性知识：工具和命令
- 隐性知识：直觉、审美、经验、判断力
- 真正的能力 = 显性知识 + 隐性知识

**学徒制四阶段**：
1. **观察** - 看大师如何思考和操作
2. **模仿** - 在导师指导下进行操作
3. **反思** - 内化知识，建立思维框架
4. **总结与创新** - 将隐性知识显性化

### 3. SSH-Kali 技能模块

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

## 学习路径

1. **入门**：阅读 `SKILL_KALI_OPTIMIZED.md`，掌握基础工具和命令
2. **进阶**：阅读 `KALI_POLANYI_APPRENTICESHIP.md`，理解隐性知识
3. **实践**：配置 `ssh-kali` 模块，在真实环境中练习
4. **总结**：建立个人知识库，形成自己的方法论

## 注意事项

- 本项目仅供安全研究和授权测试使用
- 未经授权对他人系统进行渗透测试属于违法行为
- 密码等敏感信息请妥善保管，不要提交到版本控制

## 许可证

本项目仅供学习和研究使用。
