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

entity toplevel_sw_sine_noise is
    Port ( CLK100MHZ : in STD_LOGIC;
           sw       : in std_logic_vector(12 downto 0);
           AUD_PWM  : out STD_LOGIC;
           AUD_SD   : out STD_LOGIC);
end toplevel_sw_sine_noise;

architecture Behavioral of toplevel_sw_sine_noise is
    -- types
    type gains is array (3 downto 0) of std_logic_vector(3 downto 0);
    -- constants
    constant timer_bits : natural := natural(
        ceil(log2(real(10_000_000)))
    );
    constant note_a4_fcw : unsigned(26 downto 0) := to_unsigned(591, 27);
    -- signals
    signal phase_out        : unsigned(15 downto 0);
    signal amp_out_tri, amp_out_saw : unsigned(15 downto 0);
    signal amp_out_muxed    : unsigned(15 downto 0);
    signal amp_out_gain_adj : unsigned(15 downto 0);
    signal pwm_out          : std_logic;
    signal fcw              : unsigned(26 downto 0);
    signal noise_ports      : unsigned(4 downto  0);
    -- components
        -- MIDI Note Lookup Table
        component midi_note_lut is
            port(
            note_in    : in  unsigned(6 downto 0);
            freq_out   : out unsigned(26 downto 0)
            );
        end component;
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
        -- PAC (phase to amplitude converter) -- triangle wave
        component pac_sine is
          generic(
            phase_bits   : natural := 16
          );
          port(
            clk, reset : in  std_logic;
            extra      : in  std_logic_vector(4 downto 0);
            phase      : in  unsigned(phase_bits-1 downto 0);
            amp        : out unsigned(phase_bits-1 downto 0)
          );
        end component;
        -- PAC (phase to amplitude converter) -- sawtooth wave
        component pac_noise is
          generic(
            phase_bits   : natural := 16;
            seed : natural := 413
          );
          port(
            clk, reset : in  std_logic;
            extra      : in  std_logic_vector(4 downto 0);
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
    midi_lookup : midi_note_lut
        port map(
        note_in  => unsigned(sw(7 downto 1)),
        freq_out => fcw
    );
    phase_accumulator : phase_accum 
        generic map( n_bits_count => 27, n_bits_out => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            fcw=> fcw,
            phase=>phase_out 
        );
    pac_sine_gen : pac_sine
        generic map( phase_bits => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            extra => (others => '0'),
            phase => phase_out, 
            amp => amp_out_tri
        );
    noise_ports <= (4 => sw(12), others => '0');
    pac_noise_gen : pac_noise
        generic map( phase_bits => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            extra => std_logic_vector(noise_ports),
            phase => phase_out, 
            amp => amp_out_saw
        );
    amp_out_muxed <= amp_out_tri when sw(0)='0' else amp_out_saw;
    gain : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  amp_out_muxed,
            shamt =>   unsigned(sw(11 downto 8)),
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
