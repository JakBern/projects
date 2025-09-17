-- ** ===================================== **
--  Circuit: Phase to Amplitude Converter (Pulse)                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-01                               
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity pac_pulse is
  generic(
    phase_bits   : natural := 16
  );
  port(
    clk, reset : in  std_logic;
    -- turn osc into a pulse-width modulated saw wave
    saw_en     : in std_logic;
    -- configurable duty cycle from 0% to 100% in steps of 6.25% using bit shifts
    duty_cycle : in  unsigned(3 downto 0);
    phase      : in  unsigned(phase_bits-1 downto 0);
    amp        : out unsigned(phase_bits-1 downto 0)
  );
end pac_pulse;

architecture pac_pulse_behavior of pac_pulse is
  signal amp_reg, amp_next : unsigned(phase_bits-1 downto 0) := (others => '0');
  signal phase_msb      : unsigned(3 downto 0);
  signal hi_waveform       : unsigned(phase_bits-1 downto 0);
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
  phase_msb   <= phase(phase_bits-1 downto phase_bits-4);
  hi_waveform <= (others => '1') when saw_en='0' else phase;
  amp_next <=  hi_waveform when phase_msb < duty_cycle else (others => '0');

-- output logic
  amp <= amp_reg;
  
end pac_pulse_behavior;