import winreg

def has_value(sub_key, name):
    try:
        winreg.QueryValueEx(sub_key, name)
        return True
    except FileNotFoundError:
        return False

def get_installed_apps():
    uninstall_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    app_list = []

    for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for key_path in uninstall_keys:
            try:
                reg_key = winreg.OpenKey(root, key_path)
                for i in range(winreg.QueryInfoKey(reg_key)[0]):
                    sub_key_name = winreg.EnumKey(reg_key, i)
                    sub_key = winreg.OpenKey(reg_key, sub_key_name)

                    try:
                        name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        uninstall_cmd = winreg.QueryValueEx(sub_key, "UninstallString")[0]

                        if not name or not uninstall_cmd:
                            continue

                        system_component = winreg.QueryValueEx(sub_key, "SystemComponent")[0] if has_value(sub_key, "SystemComponent") else 0
                        if system_component == 1:
                            continue

                        release_type = winreg.QueryValueEx(sub_key, "ReleaseType")[0] if has_value(sub_key, "ReleaseType") else ""
                        if release_type.lower() in ["update", "hotfix"]:
                            continue

                        parent_key_name = winreg.QueryValueEx(sub_key, "ParentKeyName")[0] if has_value(sub_key, "ParentKeyName") else ""
                        if parent_key_name:
                            continue

                        publisher = winreg.QueryValueEx(sub_key, "Publisher")[0] if has_value(sub_key, "Publisher") else ""
                        if not publisher.strip():
                            continue

                        app_list.append((name, uninstall_cmd))

                    except:
                        continue
                    finally:
                        sub_key.Close()
                reg_key.Close()
            except:
                continue

    seen = set()
    filtered = []
    for app in app_list:
        if app[0] not in seen:
            filtered.append(app)
            seen.add(app[0])

    return sorted(filtered, key=lambda x: x[0].lower())
