-- ** ===================================== **
--  Circuit: N-Bit Barrel Left Shifter                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-01                               
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity barrel_lshifter is
  generic(
    n_bits : natural := 8
  );
  port(
    in_vec  : in  unsigned(n_bits-1 downto 0);
    shamt   : in  unsigned(
                    natural(ceil(log2(real(n_bits))))-1 
                    downto 0);
    out_vec : out unsigned(n_bits-1 downto 0)
  );
end barrel_lshifter;

architecture barrel_lshifter_behavior of barrel_lshifter is
  constant shamt_bits : natural := natural(ceil(log2(real(n_bits))));
  type shift_array is array (shamt_bits downto 0) of unsigned(n_bits-1 downto 0);
  signal intermediate_vec : shift_array;
begin
  intermediate_vec(0) <= in_vec;
  gen_muxfield: for i in 0 to shamt_bits-1 generate
    intermediate_vec(i+1) <= 
      shift_left(intermediate_vec(i), integer(2**i))
      when shamt(i)='1' else 
      intermediate_vec(i);
  end generate;
  out_vec <= intermediate_vec(shamt_bits);
end barrel_lshifter_behavior;