-- ** ===================================== **
--  Circuit: Phase to Amplitude Converter (Sine)                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-07                             
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity pac_sine is
  generic(
    phase_bits   : natural := 16
  );
  port(
    clk, reset : in  std_logic;
    extra      : in  std_logic_vector(4 downto 0);
    phase      : in  unsigned(phase_bits-1 downto 0);
    amp        : out unsigned(phase_bits-1 downto 0)
  );
end pac_sine;

architecture pac_sine_behavior of pac_sine is
  signal amp_reg, amp_next : unsigned(phase_bits-1 downto 0) := (others => '0');
  component cordic16 is
    port(
      clk, reset : in  std_logic;
      phase      : in  unsigned(15 downto 0);
      amp        : out unsigned(15 downto 0)
    );
  end component;
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
  -- all the complexity is hidden here
  sine_gen : cordic16
    port map(
        clk => clk,
        reset => reset,
        phase => phase,
        amp => amp_next
    );
-- output logic
  amp <= amp_reg;
end pac_sine_behavior;