def install_pip_packages(package_names: list[str]):
    for name in package_names:
        try:
            subprocess.check_call(["pip", "install", name])
        except subprocess.CalledProcessError as e:
            print(f"Error installing package {name}: {e}")