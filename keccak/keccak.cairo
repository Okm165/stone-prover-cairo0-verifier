%builtins output pedersen range_check bitwise

from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.cairo_builtins import BitwiseBuiltin
from starkware.cairo.common.cairo_keccak.keccak import (finalize_keccak, cairo_keccak_felts)

func main {
	   output_ptr: felt, pedersen_ptr: felt, range_check_ptr: felt, bitwise_ptr: BitwiseBuiltin*, 
} () {
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
    let (keccak_ptr: felt*) = alloc();
    local keccak_ptr_start: felt* = keccak_ptr;
    
    let val = cairo_keccak_felts{range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, keccak_ptr=keccak_ptr}(data_len, data_ptr);

    finalize_keccak(keccak_ptr_start=keccak_ptr_start, keccak_ptr_end=keccak_ptr);

    return ();
}
