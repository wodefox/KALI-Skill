#!/usr/bin/env python3
"""
SSH 连接脚本 - 通过 paramiko 连接到 Kali Linux
用法: python ssh_connect.py [--cmd "命令"] [--config <config.json路径>]
"""
import json
import sys
import os
import paramiko
from pathlib import Path

def load_config(config_path=None):
    """加载配置文件"""
    if config_path is None:
        config_path = Path.home() / ".qclaw" / "skills" / "ssh-kali" / "config.json"
    else:
        config_path = Path(config_path)
    
    if not config_path.exists():
        print(f"[ERROR] 配置文件不存在: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def connect_and_execute(config, command=None):
    """建立 SSH 连接并执行命令"""
    host = config['host']
    port = config.get('port', 22)
    username = config['username']
    password = config.get('password', '')
    
    print(f"[INFO] 连接到 {username}@{host}:{port} ...", file=sys.stderr)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, port=port, username=username, password=password, timeout=10)
        print(f"[OK] 已连接到 {host}", file=sys.stderr)
        
        if command:
            # 执行单条命令
            stdin, stdout, stderr = client.exec_command(command)
            out = stdout.read().decode('utf-8', errors='ignore')
            err = stderr.read().decode('utf-8', errors='ignore')
            if out:
                print(out, end='')
            if err:
                print(err, end='', file=sys.stderr)
        else:
            # 交互式 shell
            channel = client.invoke_shell()
            print("[INFO] 进入交互模式 (输入 'exit' 退出)", file=sys.stderr)
            
            # 简单交互循环
            import select
            while True:
                if channel.recv_ready():
                    data = channel.recv(1024).decode('utf-8', errors='replace')
                    print(data, end='', flush=True)
                
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    channel.send(line)
                
                if channel.exit_status_ready():
                    break
            
            channel.close()
        
        client.close()
        print("\n[INFO] 连接已关闭", file=sys.stderr)
        
    except paramiko.AuthenticationException:
        print(f"[ERROR] 认证失败 - 检查用户名/密码", file=sys.stderr)
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"[ERROR] SSH 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='SSH 连接到 Kali')
    parser.add_argument('--cmd', type=str, help='要执行的命令')
    parser.add_argument('--config', type=str, help='配置文件路径')
    args = parser.parse_args()
    
    config = load_config(args.config)
    connect_and_execute(config, args.cmd)

if __name__ == '__main__':
    main()
