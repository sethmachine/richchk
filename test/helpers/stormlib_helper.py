import platform


def run_test_if_mac_m1() -> bool:
    return (
        platform.system().lower() == "darwin" and platform.machine().lower() == "arm64"
    )


def run_test_if_linux_x86_64() -> bool:
    return (
        platform.system().lower() == "linux" and platform.machine().lower() == "x86_64"
    )
