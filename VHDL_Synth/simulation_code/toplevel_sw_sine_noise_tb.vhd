----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05/07/2025 01:41:17 PM
-- Design Name: 
-- Module Name: toplevel_sw_sine_noise_tb - Behavioral
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity toplevel_sw_sine_noise_tb is
--  Port ( );
end toplevel_sw_sine_noise_tb;

architecture Behavioral of toplevel_sw_sine_noise_tb is
signal clk, aud_pwm, aud_sd : std_logic := '0';
signal sw  : std_logic_vector(12 downto 0) := (5 => '1', 6 => '1', 7 => '1', others => '0');
component toplevel_sw_sine_noise is
    Port ( CLK100MHZ : in STD_LOGIC;
           sw       : in std_logic_vector(12 downto 0);
           AUD_PWM  : out STD_LOGIC;
           AUD_SD   : out STD_LOGIC);
end component;
begin
tp : toplevel_sw_sine_noise
    port map(
        clk100mhz => clk,
        sw => sw,
        aud_pwm => aud_pwm,
        aud_sd => aud_sd
    );
    process
    begin
        for i in 0 to 1 loop
            wait for 10ps;
            clk <= not clk;
        end loop;
    end process;
end Behavioral;
