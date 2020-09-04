import platform
import subprocess
import sys
import os

server_fusion = '192.168.5.110/glpi/plugins/fusioninventory/'


def get_computer_platform():
    so = platform.platform()
    arch = platform.architecture()

    return [so, arch]

def git_install():
    so, arch = get_computer_platform()
    if '64' in arch:
        path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\Git-2.26.2-64-bit.exe"
    else:
        path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\Git-2.26.2-32-bit.exe"

    response = subprocess.run(["copy", path_installer, "C:\\install\\inst.exe"], shell=True)
    if response.returncode != 0:
        raise Exception('Não foi possível copiar o git para a máquina')

    with open('inst.bat', 'w') as bat:
        script = """
        cd C:\\install
        start inst.exe /VERYSILENT
        """
        bat.write(script)
    response = subprocess.run(['inst.bat'])
    if response.returncode != 0:
        raise Exception('Não foi possível instalar o git para a máquina')


def python_install():
    so, arch = get_computer_platform()
    if '64' in arch:
        path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\python-3.7.4-amd64.exe"
    else:
        path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\python-3.7.4.exe"
    response = subprocess.run(["copy", path_installer, "C:\\install\\inst.exe"], shell=True)
    with open('inst.bat', 'w') as bat:
        script = f"""
        cd C:\\install
        start inst.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        """
        bat.write(script)
    response = subprocess.run(['inst.bat'])
    if response.returncode != 0:
        raise Exception('Não foi possível instalar o python para a máquina')


def sesp_install():
    with open('inst.bat', 'w') as bat: 
        script = f"""
        cd C:\\install
        git clone https://github.com/duzzsys/SESP.git
        cd SESP
        git clone -b master_version https://github.com/duzzsys/SESP.git Atualizações       
        start main.py  True
        """
        bat.write(script)
    response = subprocess.run(['inst.bat'])
    if response.returncode != 0:
        raise Exception('Não foi possível instalar o sesp para a máquina')
    exclude()
    os.system('shutdown -r -t 1')


def fusion_install():
    os, arch = get_computer_platform()
    if '64' in arch:
        path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Internet e Rede\\Fusion Inventory\\fusioninventory-agent_windows-x64_2.5.1.exe"
    else:
        path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Internet e Rede\\Fusion Inventory\\fusioninventory-agent_windows-x86_2.5.1.exe"
    
    response = subprocess.run(["copy", path_installer, "C:\\install\\inst.exe"], shell=True)
    if response.returncode != 0:
        raise Exception('Não foi possível copiar o fusion agent para a máquina')

    with open('inst.bat', 'w') as bat:
        script = f"""
        cd C:\\install
        start inst.exe /S /acceptlicense /add-firewall-exception /execmode=Service /httpd /server={server_fusion}"
        """


def exclude():
    response = subprocess.run(["erase", "/q", "C:\\install\\inst.exe"], shell=True)
    if response.returncode != 0:
        raise Exception('Não foi possível apagar o executável')
    response = subprocess.run(["erase", "/q", "inst.bat"], shell=True)
    if response.returncode != 0:
        raise Exception('Não foi possível apagar o script')


if __name__ == "__main__":
    response = subprocess.run(["mkdir", "C:\\install"], shell=True)
    if response.returncode != 0:
        print('Não foi preciso criar o diretório\n')
    inventory_number = sys.argv[1]
    git_install()
    python_install()
    sesp_install()
    fusion_install()