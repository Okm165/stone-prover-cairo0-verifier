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
    'verifier_program_file="cairo-lang/cairo_verifier.json"', 
    'proof_file="cairo-lang/simple_bootloader_proof.json"',
    'recursion_program_file="stone-prover/e2e_test/fibonacci_compiled.json"',
    'simple_bootloader_input_tamplate="cairo-lang/simple_bootloader_input_tamplate.json"',
    'outputFile="cairo-lang/simple_bootloader_input.json"',
    'jq -n \
    --argfile verifier_program "$verifier_program_file" \
    --argfile proof "$proof_file" \
    --argfile recursion_program "$recursion_program_file" \
    -f "$simple_bootloader_input_tamplate" > "$outputFile"'
], "Preapring recursion step input", cwd="./")

log_and_run([
    "cairo-run \
    --program=simple_bootloader.json \
    --layout=recursive \
    --program_input=simple_bootloader_input.json \
    --air_public_input=simple_bootloader_public_input.json \
    --air_private_input=simple_bootloader_private_input.json \
    --trace_file=simple_bootloader_trace.json \
    --memory_file=simple_bootloader_memory.json \
    --print_output \
    --proof_mode \
    --print_info"
], "Running recursion step", cwd="cairo-lang")

log_and_run([
    "../stone-prover/e2e_test/cpu_air_prover \
    --out_file=simple_bootloader_proof.json \
    --private_input_file=simple_bootloader_private_input.json \
    --public_input_file=simple_bootloader_public_input.json \
    --prover_config_file=cpu_air_prover_config.json \
    --parameter_file=cpu_air_params.json \
    -generate_annotations"
], "Proving recursion step", cwd="cairo-lang")