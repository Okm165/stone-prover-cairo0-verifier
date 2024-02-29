%builtins output pedersen range_check ecdsa bitwise ec_op keccak poseidon

from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.cairo_builtins import (KeccakBuiltin, BitwiseBuiltin)
from starkware.cairo.common.builtin_keccak.keccak import keccak_felts

func main(
	   output_ptr: felt*, pedersen_ptr: felt*, range_check_ptr: felt, ecdsa_ptr: felt*, bitwise_ptr: BitwiseBuiltin*, ec_op_ptr: felt*, keccak_ptr: KeccakBuiltin*, poseidon_ptr: felt*
) -> (output_ptr: felt*, pedersen_ptr: felt*, range_check_ptr: felt, ecdsa_ptr: felt*, bitwise_ptr: BitwiseBuiltin*, ec_op_ptr: felt*, keccak_ptr: KeccakBuiltin*, poseidon_ptr: felt*) { 
    alloc_locals;
    // Fetch data from public inputs this is an unconstrained hinted operation that loads all data from *_public_input.json, allocates a new data segment and copies it into it.
    local data_len; // Number of elements to hash
    local data_ptr: felt*;
    %{
         ids.data_len = program_input['data_len']

         data = program_input['data']
         
         ids.data_ptr = data_ptr = segments.add()
         for i, val in enumerate(data):
             memory[data_ptr + i] = val
    %}
    let val = keccak_felts{range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, keccak_ptr=keccak_ptr}(data_len, data_ptr);
 return (
        output_ptr=output_ptr, pedersen_ptr=pedersen_ptr, range_check_ptr=range_check_ptr, ecdsa_ptr=ecdsa_ptr,
        bitwise_ptr=bitwise_ptr, ec_op_ptr=ec_op_ptr, keccak_ptr=keccak_ptr, poseidon_ptr=poseidon_ptr
    );
}
