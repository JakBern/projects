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

entity toplevel is
    Port ( CLK100MHZ : in STD_LOGIC;
           AUD_PWM : out STD_LOGIC;
           AUD_SD  : out STD_LOGIC);
end toplevel;

architecture Behavioral of toplevel is
    -- types
    type gains is array (3 downto 0) of std_logic_vector(3 downto 0);
    -- constants
    constant timer_bits : natural := natural(
        ceil(log2(real(10_000_000)))
    );
    constant note_a4_fcw : unsigned(26 downto 0) := to_unsigned(591, 27);
    -- signals
    signal timer_reg, timer_next               : unsigned(timer_bits-1 downto 0) := (others => '0');
    signal gain_reg, gain_next                 : unsigned(3 downto 0) := "0000";
    signal duty_reg, duty_next                 : unsigned(3 downto 0) := "0100";
    signal saw_en_reg, saw_en_next             : std_logic := '1';
    signal timer_pulse, gain_pulse, duty_pulse : std_logic;

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
    process (CLK100MHZ)
    begin
        if (rising_edge(CLK100MHZ)) then
            timer_reg <= timer_next;
            gain_reg <= gain_next;
            duty_reg <= duty_next;
            saw_en_reg <= saw_en_next;
        end if;
    end process;
-- next-state logic
    timer_next <= timer_reg + 1;
    timer_pulse <= '1' when signed(timer_reg)=to_signed(-1,timer_reg'length) else '0'; -- trick learned from https://vhdlwhiz.com/how-to-check-if-a-vector-is-all-zeros-or-ones/
    
    gain_next <= gain_reg - 1 when timer_pulse='1' else gain_reg;
    gain_pulse <= '1' when timer_pulse='1' and gain_reg=0 else '0';
    
    duty_next <= duty_reg + 1 when gain_pulse='1' else duty_reg;
    duty_pulse <= '1' when timer_pulse='1' and signed(duty_reg)=to_signed(-1,duty_reg'length) else '0';

    saw_en_next <= not saw_en_reg when duty_pulse='1' else saw_en_reg;
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
            saw_en => saw_en_reg, 
            duty_cycle => duty_reg,
            phase => phase_out, 
            amp => amp_out
        );
    gain : barrel_rlog_shifter
        generic map( n_bits => 16 )
        port map(
            in_vec =>  amp_out,
            shamt =>   gain_reg,
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
