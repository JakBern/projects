-- ** ===================================== **
--  Circuit: Amplitude to PWM Converter                             
--  Author: Jake Bernard                               
--  Date Created: 2025-04-30                               
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity amp_to_pwm is
  generic(
    -- choices:
    --    19: assuming 8 channels, so summation of 8 signals of 16-bits will at max
    --        take 3 more bits
    --    16: truncate after add
    amp_bits   : natural := 16;
    pwm_gran   : natural := 8
  );
  port(
    clk, reset : in  std_logic;
    amp        : in  unsigned(amp_bits-1 downto 0);
    pwm        : out std_logic
  );
end amp_to_pwm;

architecture amp_to_pwm_behavior of amp_to_pwm is
  -- counting to 2^9 happens at a frequency of 195,312.5 HZ
  --  manual for board says PWM signal should be ~10x faster than
  --  signal you want to represent, and max possible MIDI note freq
  --  is 13289.75.
  signal counter_reg, counter_next : unsigned(pwm_gran-1 downto 0) := (others => '0');
  -- truncate to only 9 most significant bits of amplitude signal
  signal amp_trunc                 : unsigned(pwm_gran-1 downto 0);
  signal pwm_reg, pwm_next         : std_logic;
begin
-- register
  process (clk,reset)
  begin
    if (reset='1') then
      pwm_reg <= '0';
      counter_reg <= (others => '0');
    elsif (rising_edge(clk)) then
      counter_reg <= counter_next;
      pwm_reg <= pwm_next;
    end if;
  end process;
-- next-state logic
  amp_trunc <= amp(amp_bits-1 downto amp_bits-pwm_gran);
  counter_next <= counter_reg + 1;
  pwm_next <= '1' when counter_next < amp_trunc else '0';
-- output logic
  pwm <= pwm_reg;
end amp_to_pwm_behavior;