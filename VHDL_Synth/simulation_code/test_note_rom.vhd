----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05/08/2025 01:25:19 AM
-- Design Name: 
-- Module Name: test_note_rom - Behavioral
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity test_note_rom is
--  Port ( );
end test_note_rom;

architecture Behavioral of test_note_rom is
component midi_note_lut is
  port(
    -- 128 different midi notes
    note_in    : in unsigned(6 downto 0);
    freq_out   : out unsigned(26 downto 0)
  );
end component;
signal inp  : unsigned(6 downto 0) := (others => '0');
signal outp : unsigned(26 downto 0) := (others => '0');
begin
process
begin
    for i in 0 to 127 loop
        wait for 100ps;
        inp <= to_unsigned(i, 7);
    end loop;
end process;
lookup : midi_note_lut
    port map(
        inp,
        outp
    );
end Behavioral;
