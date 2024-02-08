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
    "jq '{ proof: . }' ../stone-prover/e2e_test/proof.json > cairo_verifier_input.json", 
], "Preparing input", cwd="cairo-lang")

log_and_run([
    "cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info --proof_mode", 
], "Compiling verifier program", cwd="cairo-lang")

log_and_run([
    "cairo-run \
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
], "Running verifier program", cwd="cairo-lang")

# log_and_run([
#     "./cpu_air_prover \
#     --out_file=proof.json \
#     --private_input_file=../../cairo-lang/cairo_verifier_private_input.json \
#     --public_input_file=../../cairo-lang/cairo_verifier_public_input.json \
#     --prover_config_file=cpu_air_prover_config.json \
#     --parameter_file=cpu_air_params.json \
#     -generate_annotations", 
# ], "Proving verifer program in recursive layout", cwd="stone-prover/bridge")
