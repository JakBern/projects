-- ** ===================================== **
--  Circuit: Phase to Amplitude Converter (Sawtooth)                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-02                               
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity pac_saw is
  generic(
    phase_bits   : natural := 16
  );
  port(
    clk, reset : in  std_logic;
    extra      : in  std_logic_vector(4 downto 0);
    phase      : in  unsigned(phase_bits-1 downto 0);
    amp        : out unsigned(phase_bits-1 downto 0)
  );
end pac_saw;

architecture pac_saw_behavior of pac_saw is
  signal amp_reg, amp_next : unsigned(phase_bits-1 downto 0);
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
  amp_next <= phase;

-- output logic
  amp <= amp_reg;
  
end pac_saw_behavior;