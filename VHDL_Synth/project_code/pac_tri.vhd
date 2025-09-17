-- ** ===================================== **
--  Circuit: Phase to Amplitude Converter (Triangle)                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-01                               
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity pac_tri is
  generic(
    phase_bits   : natural := 16
  );
  port(
    clk, reset : in  std_logic;
    extra      : in  std_logic_vector(4 downto 0);
    phase      : in  unsigned(phase_bits-1 downto 0);
    amp        : out unsigned(phase_bits-1 downto 0)
  );
end pac_tri;

architecture pac_tri_behavior of pac_tri is
  signal amp_reg, amp_next : unsigned(phase_bits-1 downto 0);
  signal inverter          : unsigned(phase_bits-2 downto 0);
begin

-- register
  process (clk,reset)
  begin
    if (reset='1') then
      amp_reg <= (others => '0');
    elsif (rising_edge(clk)) then
      amp_reg <= amp_next;
    end if;
  end process;

-- next-state logic
  -- take 1s complement inverse when past threshold via XORing all bits below MSB then shifting left one
  inverter <= (others => phase(phase_bits-1));
  amp_next <= (phase(phase_bits-2 downto 0) & '0') xor (inverter & phase(phase_bits-1));

-- output logic
  amp <= amp_reg;
  
end pac_tri_behavior;