import tkinter as tk
from tkinter import messagebox
import subprocess
import configparser
import os
import sys
import ctypes

CONFIG_FILE = 'config.ini'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # 重新启动脚本，并要求管理员权限
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

def save_config():
    config = configparser.ConfigParser()
    config['NETWORK1'] = {
        'ip': ip_entry1.get(),
        'subnet': subnet_entry1.get(),
        'gateway': gateway_entry1.get(),
        'dns1': dns1_entry1.get(),
        'dns2': dns2_entry1.get()
    }
    config['NETWORK2'] = {
        'ip': ip_entry2.get(),
        'subnet': subnet_entry2.get(),
        'gateway': gateway_entry2.get(),
        'dns1': dns1_entry2.get(),
        'dns2': dns2_entry2.get()
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    messagebox.showinfo("成功", "已保存配置")

def load_config():
    if os.path.exists(CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        network1 = config['NETWORK1']
        network2 = config['NETWORK2']
        ip_entry1.insert(0, network1['ip'])
        subnet_entry1.insert(0, network1['subnet'])
        gateway_entry1.insert(0, network1['gateway'])
        dns1_entry1.insert(0, network1['dns1'])
        dns2_entry1.insert(0, network1['dns2'])
        ip_entry2.insert(0, network2['ip'])
        subnet_entry2.insert(0, network2['subnet'])
        gateway_entry2.insert(0, network2['gateway'])
        dns1_entry2.insert(0, network2['dns1'])
        dns2_entry2.insert(0, network2['dns2'])

def get_network_info():
    result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
    output_lines = result.stdout.splitlines()
    filtered_lines = [line for line in output_lines if 'vEthernet (Default Switch)' not in line]
    return "\n".join(filtered_lines)

def refresh_network_info():
    network_info.set(get_network_info())

def set_auto_ip():
    try:
        subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', 'name="以太网"', 'source=dhcp'], check=True, shell=True)
        subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', 'name="以太网"', 'source=dhcp'], check=True, shell=True)
        refresh_network_info()
        messagebox.showinfo("成功", "IP已自动获取")
    except subprocess.CalledProcessError:
        messagebox.showerror("错误", "自动获取IP时出错")

def set_manual_ip(ip, subnet, gateway, dns1, dns2):
    try:
        subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', 'name="以太网"', 'static', ip, subnet, gateway], check=True, shell=True)
        subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', 'name="以太网"', 'static', dns1], check=True, shell=True)
        if dns2:
            subprocess.run(['netsh', 'interface', 'ip', 'add', 'dns', 'name="以太网"', dns2, 'index=2'], check=True, shell=True)
        refresh_network_info()
        messagebox.showinfo("成功", "IP已设置为手动配置")
    except subprocess.CalledProcessError:
        messagebox.showerror("错误", "设置IP时出错")

root = tk.Tk()
root.title("自动切换IP和DNS")

# 网络信息显示区
current_network_frame = tk.LabelFrame(root, text="当前网络信息", padx=10, pady=10)
current_network_frame.pack(side=tk.LEFT, padx=10, pady=10)

network_info = tk.StringVar()
network_info.set(get_network_info())
current_network_info = tk.Label(current_network_frame, textvariable=network_info, wraplength=350, justify=tk.LEFT)
current_network_info.pack()

# 刷新按钮
refresh_button = tk.Button(current_network_frame, text="刷新", command=refresh_network_info)
refresh_button.pack(pady=10)

# 配置输入区
config_frame = tk.Frame(root)
config_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# 自动获取IP按钮
auto_get_ip_button = tk.Button(config_frame, text="自动获取IP", command=set_auto_ip)
auto_get_ip_button.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

# IP配置标签和输入框排列——第一组
ip_label1 = tk.Label(config_frame, text="IP地址1:")
ip_label1.grid(row=1, column=0, sticky=tk.E)
ip_entry1 = tk.Entry(config_frame)
ip_entry1.grid(row=1, column=1, padx=(0, 10))

subnet_label1 = tk.Label(config_frame, text="子网掩码1:")
subnet_label1.grid(row=2, column=0, sticky=tk.E)
subnet_entry1 = tk.Entry(config_frame)
subnet_entry1.grid(row=2, column=1, padx=(0, 10))

gateway_label1 = tk.Label(config_frame, text="网关1:")
gateway_label1.grid(row=3, column=0, sticky=tk.E)
gateway_entry1 = tk.Entry(config_frame)
gateway_entry1.grid(row=3, column=1, padx=(0, 10))

dns1_label1 = tk.Label(config_frame, text="DNS1:")
dns1_label1.grid(row=4, column=0, sticky=tk.E)
dns1_entry1 = tk.Entry(config_frame)
dns1_entry1.grid(row=4, column=1, padx=(0, 10))

dns2_label1 = tk.Label(config_frame, text="DNS2:")
dns2_label1.grid(row=5, column=0, sticky=tk.E)
dns2_entry1 = tk.Entry(config_frame)
dns2_entry1.grid(row=5, column=1, padx=(0, 10))

manual_ip_button1 = tk.Button(config_frame, text="手动获取IP模块1", command=lambda: set_manual_ip(ip_entry1.get(), subnet_entry1.get(), gateway_entry1.get(), dns1_entry1.get(), dns2_entry1.get()))
manual_ip_button1.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

# IP配置标签和输入框排列——第二组
ip_label2 = tk.Label(config_frame, text="IP地址2:")
ip_label2.grid(row=1, column=2, sticky=tk.E)
ip_entry2 = tk.Entry(config_frame)
ip_entry2.grid(row=1, column=3, padx=(0, 10))

subnet_label2 = tk.Label(config_frame, text="子网掩码2:")
subnet_label2.grid(row=2, column=2, sticky=tk.E)
subnet_entry2 = tk.Entry(config_frame)
subnet_entry2.grid(row=2, column=3, padx=(0, 10))

gateway_label2 = tk.Label(config_frame, text="网关2:")
gateway_label2.grid(row=3, column=2, sticky=tk.E)
gateway_entry2 = tk.Entry(config_frame)
gateway_entry2.grid(row=3, column=3, padx=(0, 10))

dns1_label2 = tk.Label(config_frame, text="DNS1:")
dns1_label2.grid(row=4, column=2, sticky=tk.E)
dns1_entry2 = tk.Entry(config_frame)
dns1_entry2.grid(row=4, column=3, padx=(0, 10))

dns2_label2 = tk.Label(config_frame, text="DNS2:")
dns2_label2.grid(row=5, column=2, sticky=tk.E)
dns2_entry2 = tk.Entry(config_frame)
dns2_entry2.grid(row=5, column=3, padx=(0, 10))

manual_ip_button2 = tk.Button(config_frame, text="手动获取IP模块2", command=lambda: set_manual_ip(ip_entry2.get(), subnet_entry2.get(), gateway_entry2.get(), dns1_entry2.get(), dns2_entry2.get()))
manual_ip_button2.grid(row=6, column=2, columnspan=2, pady=10, sticky="ew")

# 保存配置按钮
save_button = tk.Button(config_frame, text="保存配置", command=save_config)
save_button.grid(row=7, column=0, columnspan=4, pady=10, sticky="ew")

# 加载配置
load_config()

root.mainloop()