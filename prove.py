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
    "cairo-run \
    --program=program_compiled.json \
    --layout=starknet_with_keccak \
    --program_input=program_input.json \
    --air_public_input=public_input.json \
    --air_private_input=private_input.json \
    --trace_file=trace.json \
    --memory_file=memory.json \
    --print_output \
    --print_info \
    --proof_mode", 
], "Running program", cwd="stone-prover/e2e_test")

log_and_run([
    "./cpu_air_prover \
    --out_file=proof.json \
    --private_input_file=private_input.json \
    --public_input_file=public_input.json \
    --prover_config_file=cpu_air_prover_config.json \
    --parameter_file=cpu_air_params.json \
    -generate_annotations", 
], "Proving fibonacci program", cwd="stone-prover/e2e_test")
