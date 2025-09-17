-- ** ===================================== **
--  Circuit: 8-way 16-bit Channel Mixer                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-01                               
--  Desc: Been making too many components generic when I really don't need to.                                                       
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity channel_mixer is
  port(
    clk, reset                              : in std_logic;
    channel1, channel2, channel3, channel4  : in unsigned(15 downto 0);
    channel5, channel6, channel7, channel8  : in unsigned(15 downto 0);
    mixed                                   : out unsigned(15 downto 0)
  );
end channel_mixer;

architecture channel_mixer_behavior of channel_mixer is
  signal partial_sum1_reg,  partial_sum2_reg,  partial_sum3_reg,  partial_sum4_reg  : unsigned(16 downto 0);
  signal partial_sum1_next, partial_sum2_next, partial_sum3_next, partial_sum4_next : unsigned(16 downto 0);
  signal ppartial_sum1_reg,  ppartial_sum2_reg  : unsigned(17 downto 0);
  signal ppartial_sum1_next, ppartial_sum2_next : unsigned(17 downto 0);
  signal pppartial_sum1_reg  : unsigned(18 downto 0);
  signal pppartial_sum1_next : unsigned(18 downto 0);
begin
-- register
process (clk,reset)
begin
  if (reset='1') then
    partial_sum1_reg   <= (others => '0');
    partial_sum2_reg   <= (others => '0');
    partial_sum3_reg   <= (others => '0');
    partial_sum4_reg   <= (others => '0');
    ppartial_sum1_reg  <= (others => '0');
    ppartial_sum2_reg  <= (others => '0');
    pppartial_sum1_reg <= (others => '0');
  elsif (rising_edge(clk)) then
    partial_sum1_reg   <= partial_sum1_next;
    partial_sum2_reg   <= partial_sum2_next;
    partial_sum3_reg   <= partial_sum3_next;
    partial_sum4_reg   <= partial_sum4_next;
    ppartial_sum1_reg  <= ppartial_sum1_next;
    ppartial_sum2_reg  <= ppartial_sum2_next;
    pppartial_sum1_reg <= pppartial_sum1_next;
  end if;
end process;
-- next-state logic
  partial_sum1_next   <= unsigned( '0' & channel1 )          + unsigned( '0' & channel2 );
  partial_sum2_next   <= unsigned( '0' & channel3 )          + unsigned( '0' & channel4 );
  partial_sum3_next   <= unsigned( '0' & channel5 )          + unsigned( '0' & channel6 );
  partial_sum4_next   <= unsigned( '0' & channel7 )          + unsigned( '0' & channel8 );
  ppartial_sum1_next  <= unsigned( '0' & partial_sum1_reg )  + unsigned( '0' & partial_sum2_reg );
  ppartial_sum2_next  <= unsigned( '0' & partial_sum3_reg )  + unsigned( '0' & partial_sum4_reg );
  pppartial_sum1_next <= unsigned( '0' & ppartial_sum1_reg ) + unsigned( '0' & ppartial_sum2_reg );
-- output logic
  mixed <= pppartial_sum1_reg(18 downto 3);
end channel_mixer_behavior;