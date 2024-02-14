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
    'program_file="cairo-lang/cairo_verifier.json"', 
    'proof_file="stone-prover/e2e_test/zerosync_proof.json"',
    'simple_bootloader_input_template="cairo-lang/simple_bootloader_input_template.json"',
    'outputFile="cairo-lang/simple_bootloader_input.json"',
    'jq -n \
    --argfile program "$program_file" \
    --argfile proof "$proof_file" \
    -f "$simple_bootloader_input_template" > "$outputFile"'
], "Preapring bootloader-bridge input", cwd=".")

log_and_run([
    "time cairo-run \
    --program=simple_bootloader.json \
    --layout=recursive \
    --program_input=simple_bootloader_input.json \
    --air_public_input=simple_bootloader_public_input.json \
    --air_private_input=simple_bootloader_private_input.json \
    --trace_file=simple_bootloader_trace.bin \
    --memory_file=simple_bootloader_memory.bin \
    --print_output \
    --proof_mode \
    --print_info"
], "Running bootloader-bridge step", cwd="cairo-lang")

log_and_run([
    "time ./cpu_air_prover \
    --out_file=bootloader_proof.json \
    --public_input_file=../../cairo-lang/simple_bootloader_public_input.json \
    --private_input_file=../../cairo-lang/simple_bootloader_private_input.json \
    --prover_config_file=cpu_air_prover_config.json \
    --parameter_file=cpu_air_params.json \
    -generate_annotations", 
], "Proving verifer program in recursive layout", cwd="stone-prover/bootloader")
