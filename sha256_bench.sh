#!/bin/bash

# Show executed shell commands
set -o xtrace
# Exit on error.
set -e

echo "Switching to recursive_layout cairo verifier layout"
git checkout --recurse-submodules recursive_layout

cd stone-prover/e2e_test

echo "Compiling Keccak Benchmark"
cairo-compile ../../sha256/sha256.cairo --output ../../sha256/sha256_compiled.json --proof_mode

echo "Generating Proof"
cairo-run     --program=../../sha256/sha256_compiled.json     --layout=recursive --program_input=../../$1.json --air_public_input=../../sha256/public_input.json     --air_private_input=../../sha256/private_input.json     --trace_file=../../sha256/trace.json     --memory_file=../../sha256/memory.json     --print_output     --proof_mode

echo "Benchmarking Stone Prover constraining Keccak on $1 bytes"
hyperfine './cpu_air_prover     --out_file=../../sha256/sha256_proof.json     --private_input_file=../../sha256/private_input.json --public_input_file=../../sha256/public_input.json     --prover_config_file=../../sha256/cpu_air_prover_config.json --parameter_file=../../sha256/cpu_air_params.json     --generate_annotations' --show-output > air_prover.txt

echo "Benchmarking Stone Air Verifier for Keccak on $1 bytes"
hyperfine './cpu_air_verifier --in_file=../../sha256/sha256_proof.json' --show-output > air_verifier.txt

cd ../../
cd cairo-lang
jq '{ proof: . }' ../sha256/sha256_proof.json > cairo_verifier_input.json

echo "Compiling Cairo Verifier for recursive layout"
cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info

echo "Benchmarking Cairo Verifier for Keccak on $1 bytes"
hyperfine 'cairo-run --program=cairo_verifier.json --layout=recursive --program_input=cairo_verifier_input.json --trace_file=cairo_verifier_trace.json --memory_file=cairo_verifier_memory.json --print_output' --show-output > cairo_verifier.txt
cd ..
