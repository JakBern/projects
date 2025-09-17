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

entity toplevel_demo is
    Port ( CLK100MHZ : in STD_LOGIC;
           sw       : in std_logic_vector(15 downto 0);
           BTNU, BTND, BTNL, BTNR, BTNC : in std_logic;
           AUD_PWM  : out STD_LOGIC;
           AUD_SD   : out STD_LOGIC);
end toplevel_demo;

architecture Behavioral of toplevel_demo is
    -- types
    type gains is array (3 downto 0) of std_logic_vector(3 downto 0);
    -- constants
    constant timer_bits : natural := natural(
        ceil(log2(real(10_000_000)))
    );
    constant note_a4_fcw : unsigned(26 downto 0) := to_unsigned(591, 27);
    -- signals
    signal phase_out                : unsigned(15 downto 0);
    signal amp_tri, amp_saw, amp_pulse, amp_sine, amp_noise : unsigned(15 downto 0);
    signal s_amp_tri, s_amp_saw, s_amp_pulse, s_amp_sine, s_amp_noise : unsigned(15 downto 0);
    signal sg_amp_tri, sg_amp_saw, sg_amp_pulse, sg_amp_sine, sg_amp_noise : unsigned(15 downto 0);
    signal mixed_track      : unsigned(15 downto 0);
    signal pwm_out          : std_logic;
    signal fcw              : unsigned(26 downto 0);
    
    -- input splitting
    signal note    : unsigned(6 downto 0);
    signal extra   : unsigned(4 downto 0);
    signal gain_in : unsigned(3 downto 0);
    
    
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
        -- PAC (phase to amplitude converter) -- sine wave
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
        -- PAC (phase to amplitude converter) -- noise
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
        -- PAC (phase to amplitude converter) -- triangle wave
        component pac_tri is
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
        component pac_saw is
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
          -- channel mixer
          component channel_mixer is
          port(
            clk, reset                              : in std_logic;
            channel1, channel2, channel3, channel4  : in unsigned(15 downto 0);
            channel5, channel6, channel7, channel8  : in unsigned(15 downto 0);
            mixed                                   : out unsigned(15 downto 0)
          );
        end component;
begin
-- split input
note  <= unsigned(sw(6 downto 0));
extra <= unsigned(sw(11 downto 7));
gain_in <= unsigned(sw(15 downto 12));
-- register
-- next-state logic
-- output logic
    midi_lookup : midi_note_lut
        port map(
        note_in  => note,
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
            extra => std_logic_vector(extra),
            phase => phase_out, 
            amp => amp_sine
        );
    pac_noise_gen : pac_noise
        generic map( phase_bits => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            extra => std_logic_vector(extra),
            phase => phase_out, 
            amp => amp_noise
        );
     pac_tri_gen : pac_tri
        generic map( phase_bits => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            extra => std_logic_vector(extra),
            phase => phase_out, 
            amp => amp_tri
        );
      pac_saw_gen : pac_saw
        generic map( phase_bits => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            extra => std_logic_vector(extra),
            phase => phase_out, 
            amp => amp_saw
        );
      pac_pulse_gen : pac_pulse
        generic map( phase_bits => 16 )
        port map( 
            clk=>CLK100MHZ, 
            reset=>'0',
            saw_en => std_logic(extra(4)),
            duty_cycle => extra(3 downto 0),
            phase => phase_out, 
            amp => amp_pulse
        );

    s_amp_noise <=  amp_noise  when BTNC='1' else (others => '0');   
    s_amp_sine  <=  amp_sine   when BTNU='1' else (others => '0');  
    s_amp_saw   <=  amp_saw    when BTND='1' else (others => '0'); 
    s_amp_pulse <=  amp_pulse  when BTNR='1' else (others => '0');   
    s_amp_tri   <=  amp_tri    when BTNL='1' else (others => '0'); 

    gain_noi : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  s_amp_noise,
            shamt =>   gain_in,
            out_vec => sg_amp_noise 
        );
    gain_sin : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  s_amp_sine,
            shamt =>   gain_in,
            out_vec => sg_amp_sine
        );
    gain_saw : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  s_amp_saw,
            shamt =>   gain_in,
            out_vec => sg_amp_saw
        );
    gain_pul : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  s_amp_pulse,
            shamt =>   gain_in,
            out_vec => sg_amp_pulse
        );
    gain_tri : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  s_amp_tri,
            shamt =>   gain_in,
            out_vec => sg_amp_tri
        );
    
    chan_mix: channel_mixer
      port map(
        clk => CLK100MHZ, 
        reset => '0',                             
        channel1 => sg_amp_noise,
        channel2 => sg_amp_sine,
        channel3 => sg_amp_sine,
        channel4 => sg_amp_tri, 
        channel5 => sg_amp_tri, 
        channel6 => sg_amp_pulse, 
        channel7 => sg_amp_pulse, 
        channel8 => sg_amp_saw, 
        mixed => mixed_track                              
      );
    

    amp2pwm : amp_to_pwm
        generic map( amp_bits => 16 )
        port map(
            clk => CLK100MHZ,
            reset => '0',
            amp => mixed_track,
            pwm => pwm_out
        );     
    AUD_SD <= '1';
    AUD_PWM <= pwm_out;
end Behavioral;
