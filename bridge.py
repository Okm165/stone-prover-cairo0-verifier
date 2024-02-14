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
    "jq '{ proof: . }' ../stone-prover/e2e_test/zerosync_proof.json > cairo_verifier_input.json", 
], "Preparing cairo_verifier input", cwd="cairo-lang")

log_and_run([
    "time cairo-run \
    --program=cairo_verifier.json \
    --layout=recursive \
    --program_input=cairo_verifier_input.json \
    --air_public_input=cairo_verifier_public_input.json \
    --air_private_input=cairo_verifier_private_input.json \
    --trace_file=cairo_verifier_trace.bin \
    --memory_file=cairo_verifier_memory.bin \
    --print_info \
    --proof_mode \
    --print_output",
], "Running cairo_verifier program", cwd="cairo-lang")