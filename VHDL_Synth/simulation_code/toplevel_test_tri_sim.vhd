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

entity toplevel_test_tri_sim is
end toplevel_test_tri_sim;

architecture Behavioral of toplevel_test_tri_sim is
      component toplevel_sw_tri_saw is
          Port ( CLK100MHZ : in STD_LOGIC;
               sw       : in std_logic_vector(11 downto 0);
               AUD_PWM  : out STD_LOGIC;
               AUD_SD   : out STD_LOGIC);
     end component;
     signal clk : std_logic := '0';
     signal aud_pwm_recv, aud_sd_recv : std_logic;
begin
tri : toplevel_sw_tri_saw
    port map(
        clk100mhz => clk,
        sw => (others => '0'),
        aud_pwm => aud_pwm_recv,
        aud_sd => aud_sd_recv
    );
process
begin
    wait for 10 ps;
    clk <= not clk;
end process;
end Behavioral;
