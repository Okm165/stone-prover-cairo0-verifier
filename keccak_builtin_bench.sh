#!/bin/bash

# Show executed shell commands
set -o xtrace
# Exit on error.
set -e

echo "Switching to starknet_with_keccak cairo verifier layout"
git checkout --recurse-submodules master

cd stone-prover/e2e_test

echo "Compiling Keccak Builtin Benchmark"
cairo-compile ../../keccak_builtin/keccak_builtin.cairo --output ../../keccak_builtin/keccak_builtin_compiled.json --proof_mode

echo "Generating Proof"
cairo-run --program=../../keccak_builtin/keccak_builtin_compiled.json --layout=starknet_with_keccak --program_input=../../$1.json --air_public_input=../../keccak_builtin/public_input.json --air_private_input=../../keccak_builtin/private_input.json --trace_file=../../keccak_builtin/trace.json --memory_file=../../keccak_builtin/memory.json --print_output --proof_mode

echo "Benchmarking Stone Prover constraining Keccak (Builtin) on $1 bytes"
hyperfine './cpu_air_prover     --out_file=../../keccak_builtin/keccak_builtin_proof.json     --private_input_file=../../keccak_builtin/private_input.json     --public_input_file=../../keccak_builtin/public_input.json     --prover_config_file=../../keccak_builtin/cpu_air_prover_config.json     --parameter_file=../../keccak_builtin/cpu_air_params.json --generate_annotations' --show-output > air_prover.txt

echo "Benchmarking Stone Air Verifier for Keccak (Builtin) on $1 bytes"
hyperfine './cpu_air_verifier --in_file=../../keccak_builtin/keccak_builtin_proof.json' --show-output > air_verifier.txt

cd ../../
cd cairo-lang
jq '{ proof: . }' ../keccak_builtin/keccak_builtin_proof.json > cairo_verifier_input.json

echo "Compiling Cairo Verifier for starknet_with_keccak layout"
cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info

echo "Benchmarking Cairo Verifier for Keccak (Builtin) on $1 bytes"
hyperfine 'cairo-run --program=cairo_verifier.json --layout=starknet_with_keccak --program_input=cairo_verifier_input.json --trace_file=cairo_verifier_trace.json --memory_file=cairo_verifier_memory.json --print_output' --show-output > cairo_verifier.txt
cd ..
