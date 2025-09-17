----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05/04/2025 12:29:16 PM
-- Design Name: 
-- Module Name: toplevel - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
use work.math_real.all;

entity toplevel_sw is
    Port ( CLK100MHZ : in STD_LOGIC;
           sw       : in std_logic_vector(8 downto 0);
           AUD_PWM : out STD_LOGIC;
           AUD_SD  : out STD_LOGIC);
end toplevel_sw;

architecture Behavioral of toplevel_sw is
    -- types
    type gains is array (3 downto 0) of std_logic_vector(3 downto 0);
    -- constants
    constant timer_bits : natural := natural(
        ceil(log2(real(10_000_000)))
    );
    constant note_a4_fcw : unsigned(26 downto 0) := to_unsigned(591, 27);
    -- signals
    signal phase_out        : unsigned(15 downto 0);
    signal amp_out          : unsigned(15 downto 0);
    signal amp_out_gain_adj : unsigned(15 downto 0);
    signal pwm_out          : std_logic;
    -- components
        -- amplitude to PWM converter
        component amp_to_pwm is
            generic(
            amp_bits   : natural := 16
            );
            port(
            clk, reset : in  std_logic;
            amp        : in  unsigned(amp_bits-1 downto 0);
            pwm        : out std_logic
            );
        end component;
        -- phase accumulator
        component phase_accum is
            generic(
            n_bits_count : natural := 24;
            n_bits_out   : natural := 16
            );
            port(
            clk, reset : in  std_logic;
            fcw        : in  unsigned(n_bits_count-1 downto 0);
            phase      : out unsigned(n_bits_out-1 downto 0)
            );
        end component;
        -- PAC (phase to amplitude converter) -- pulse wave
        component pac_pulse is
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
        end component;
        -- barrel right shifter
        component barrel_rlog_shifter is
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
          end component;
begin
-- register
-- next-state logic
-- output logic
    phase_accumulator : phase_accum 
        generic map( n_bits_count => 27, n_bits_out => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            fcw=>note_a4_fcw,
            phase=>phase_out 
        );
    pac_pulse_gen : pac_pulse
        generic map( phase_bits => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            saw_en => sw(0), 
            duty_cycle => unsigned(sw(4 downto 1)),
            phase => phase_out, 
            amp => amp_out
        );
    gain : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  amp_out,
            shamt =>   unsigned(sw(8 downto 5)),
            out_vec => amp_out_gain_adj
        );
    amp2pwm : amp_to_pwm
        generic map( amp_bits => 16 )
        port map(
            clk => CLK100MHZ,
            reset => '0',
            amp => amp_out_gain_adj,
            pwm => pwm_out
        );     
    AUD_SD <= '1';
    AUD_PWM <= pwm_out;
end Behavioral;
