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
    "pip install --upgrade pip", 
    "zip -r cairo-lang-0.12.0.zip cairo-lang-0.12.0", 
    "pip install cairo-lang-0.12.0.zip"
], "Installing cairo-lang", cwd="cairo-lang")

log_and_run([
    "docker build --tag prover .",
    "container_id=$(docker create prover)",
    "docker cp -L ${container_id}:/bin/cpu_air_prover ./e2e_test",
    "docker cp -L ${container_id}:/bin/cpu_air_verifier ./e2e_test",
], "Building stone-prover", cwd="stone-prover")

log_and_run([
    "cairo-compile fibonacci.cairo --output fibonacci_compiled.json --proof_mode --no_debug_info",
], "Compile fibonacci program", cwd="stone-prover/e2e_test")

log_and_run([
    "cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --proof_mode --no_debug_info",
], "Compile cairo_verifier program", cwd="cairo-lang")

log_and_run([
    "cairo-compile --cairo_path=./src src/starkware/cairo/bootloaders/simple_bootloader/simple_bootloader.cairo --output simple_bootloader.json --proof_mode --no_debug_info",
], "Compile simple_bootloader program", cwd="cairo-lang")
