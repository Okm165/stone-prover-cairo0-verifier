import subprocess
from colorama import Fore, Style

def log_and_run(commands, description, cwd=None):
    full_command = " && ".join(commands)
    try:
        print(f"{Fore.YELLOW}Starting: {description}...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Command: {full_command}{Style.RESET_ALL}")
        result = subprocess.run(full_command, shell=True, check=True, cwd=cwd, text=True)
        print(f"{Fore.GREEN}Success: {description} completed!\n{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error running command '{full_command}': {e}\n{Style.RESET_ALL}")

log_and_run([
    "cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info --proof_mode", 
], "Compiling verifier program", cwd="cairo-lang")

log_and_run([
    "cairo-compile --cairo_path=./src src/starkware/cairo/bootloaders/simple_bootloader/simple_bootloader.cairo --output simple_bootloader.json --no_debug_info --proof_mode", 
], "Compiling simple bootloader program", cwd="cairo-lang")
