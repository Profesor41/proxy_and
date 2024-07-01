import os
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

# Підключення до пристрою
def connect_device():
    adb_key_path = os.path.expanduser('~/.android/adbkey')
    with open(adb_key_path) as f:
        priv = f.read()
    with open(f'{adb_key_path}.pub') as f:
        pub = f.read()
    signer = PythonRSASigner(pub, priv)

    device = AdbDeviceUsb()
    device.connect(rsa_keys=[signer], auth_timeout_s=5)
    return device

# Зміна проксі
def set_proxy(device, host, port):
    device.shell(f'settings put global http_proxy {host}:{port}')

# Вимкнення проксі
def disable_proxy(device):
    device.shell('settings put global http_proxy :0')

# Головна функція
def main():
    device = connect_device()

    # Зміна проксі на потрібний
    set_proxy(device, 'your.proxy.server', '8080')
    print("Проксі встановлено")

    # Деякий час чекаємо (наприклад, 10 секунд)
    import time
    time.sleep(10)

    # Вимкнення проксі
    disable_proxy(device)
    print("Проксі вимкнено")

if __name__ == '__main__':
    main()
