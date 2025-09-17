-- ** ===================================== **
--  Circuit: Phase Accumulator                              
--  Author: Jake Bernard                               
--  Date Created: 2025-04-30                               
--  Desc:                               
--                                 
--     
--
--  References used:
--    https://en.wikipedia.org/wiki/Numerically_controlled_oscillator
--    https://www.fpga4fun.com/DDS3.html
--    https://www.digikey.com/en/articles/the-basics-of-direct-digital-synthesizers-ddss                            
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity phase_accum is
  generic(
    -- allows for fine-grained frequency accumulation -- smallest representable frequency is ~0.745 Hz 
    n_bits_count : natural := 27;
    -- don't need all of those bits for the output
    n_bits_out   : natural := 16
  );
  port(
    clk, reset : in  std_logic;
    -- frequency control word -- determines phase accumulation rate.
    --    smallest possible frequency increment comes from clock_freq/(2^n_bits), which we can call delta_f
    --    the FCW for a desired frequency can be found as: round( freq / delta_f )
    fcw        : in  unsigned(n_bits_count-1 downto 0);
    phase      : out unsigned(n_bits_out-1 downto 0)
  );
end phase_accum;

architecture phase_accum_behavior of phase_accum is
  signal phase_reg, phase_next : unsigned(n_bits_count-1 downto 0) := (others => '0');
begin
-- register
  process (clk,reset)
  begin
    if (reset='1') then
      phase_reg <= (others => '0');
    elsif (rising_edge(clk)) then
      phase_reg <= phase_next;
    end if;
  end process;
-- next-state logic
  phase_next <= phase_reg + fcw;
-- output logic
  -- if output has less width than input, truncate to most significant bits
  phase <= phase_reg(n_bits_count-1 downto (n_bits_count - n_bits_out));
end phase_accum_behavior;