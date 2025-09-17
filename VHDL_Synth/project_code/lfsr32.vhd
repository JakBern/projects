-- ** ===================================== **
--  Circuit: 16-bit Linear Feedback Shift Register                              
--  Author: Jake Bernard                               
--  Date Created: 2025-05-07                              
--  Desc:                                                      
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity lfsr32 is
  generic(
   seed : natural := 1
  );
  port(
    clk, reset, en : in  std_logic;
    vec_out : out unsigned(15 downto 0)
  );
end lfsr32;

architecture lfsr32_behavior of lfsr32 is
  signal vec_reg, vec_next : unsigned(31 downto 0) := to_unsigned(seed, 32);
  signal int_xor1, int_xor2, int_xor3, int_xor4 : std_logic;
begin
-- register
  process (clk,reset,en)
  begin
    if (reset='1') then
      vec_reg <= to_unsigned(seed, 32);
    elsif (rising_edge(clk) and en='1') then
      vec_reg <= vec_next;
    end if;
  end process;
-- next-state logic
  int_xor1 <= vec_reg(31) xor vec_reg(21);
  int_xor2 <= vec_reg(1)  xor vec_reg(0);
  int_xor3 <= int_xor1    xor int_xor2;
  vec_next <= vec_reg(30 downto 0) & int_xor3;
-- output logic
  -- if output has less width than input, truncate to most significant bits
  vec_out <= vec_reg(31 downto 16);
end lfsr32_behavior;