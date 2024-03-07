import json
import sys


def run(
    verifier_compiled_program,
    verifier_program_input,
    recursive_compiled_program,
    output_file,
):
    with open(verifier_compiled_program, "r") as f:
        verifier_compiled_program_data = json.load(f)

    with open(verifier_program_input, "r") as f:
        verifier_program_input_data = json.load(f)

    with open(recursive_compiled_program, "r") as f:
        recursive_compiled_program_data = json.load(f)

    verifier_task = {}
    verifier_task["type"] = "RunProgramTask"
    verifier_task["program"] = verifier_compiled_program_data
    verifier_task["program_input"] = {"proof": verifier_program_input_data}
    verifier_task["use_poseidon"] = True

    recursive_task = {}
    recursive_task["type"] = "RunProgramTask"
    recursive_task["program"] = recursive_compiled_program_data
    recursive_task["program_input"] = {}
    recursive_task["use_poseidon"] = True

    data = {"tasks": [verifier_task, recursive_task], "single_page": True}

    # Write output
    with open(output_file, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python bootloader_input.py verifier_compiled_program verifier_program_input recursive_compiled_program output_file"
        )
        sys.exit(1)

    verifier_compiled_program = sys.argv[1]
    verifier_program_input = sys.argv[2]
    recursive_compiled_program = sys.argv[3]
    output_file = sys.argv[4]

    run(
        verifier_compiled_program,
        verifier_program_input,
        recursive_compiled_program,
        output_file,
    )
