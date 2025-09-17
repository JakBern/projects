-- ** ===================================== **
--  Circuit: Phase to Amplitude Converter (White Noise)                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-07                              
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity pac_noise is
  generic(
    phase_bits   : natural := 16;
    seed         : natural := 413
  );
  port(
    clk, reset : in  std_logic;
    extra      : in  std_logic_vector(4 downto 0);
    phase      : in  unsigned(phase_bits-1 downto 0);
    amp        : out unsigned(phase_bits-1 downto 0)
  );
end pac_noise;

architecture pac_noise_behavior of pac_noise is
  signal phase_last_reg, phase_next : unsigned(phase_bits-1 downto 0);
  signal amp_reg, amp_next   : unsigned(phase_bits-1 downto 0) := (others => '0');
  signal noise               : unsigned(phase_bits-1 downto 0) := (others => '0');
  signal sampled_noise       : unsigned(phase_bits-1 downto 0) := (others => '0');
  signal phase_pulse         : std_logic;

  component lfsr32 is
    generic(
     seed : natural := 1
    );
    port(
      clk, reset, en : in  std_logic;
      vec_out : out unsigned(15 downto 0)
    );
  end component;
begin

-- register
  process (clk,reset)
  begin
    if (reset='1') then
      amp_reg <= (others => '0');
      phase_last_reg <= (others => '0');
    elsif (rising_edge(clk)) then
      amp_reg <= amp_next;
      phase_last_reg <= phase_next;
    end if;
  end process;
  
  lfsr : lfsr32
    generic map( seed )
    port map(
      clk, 
      reset,
      phase_pulse,
      noise
    );
-- next-state logic
  phase_next <= phase;
  phase_pulse <= '1' when phase_next < phase_last_reg else '0';
  sampled_noise <= noise when extra(4)='0' else (others => noise(0));
  amp_next <=  sampled_noise when phase_pulse='1' else amp_reg;
-- output logic
  amp <= amp_reg;
  
end pac_noise_behavior;