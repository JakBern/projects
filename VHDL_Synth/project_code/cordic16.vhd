-- ** ===================================== **
--  Circuit: CORDIC Algorithm (Sine Wave from Phase)                            
--  Author: Jake Bernard                               
--  Date Created: 2025-05-07                              
--  Desc:                                                        
--    Most modules here don't have a description, but I thought it would be worthwile to explain the design here.     
--    CORDIC takes an angle as input and starts with a unit vector in the position x=1, y=0 (sine and cosine of 0).
--    It successively rotates this vector based on angles whose tangent is 2^-n (with n increasing each time), subtracting that angle from the input angle
--    and trying to get the value  of the input angle to 0 (this determines which way the rotation will occur, if it does at all).
--    Each rotation (after factoring and applying a constant to the unit vector at the start) only requires an addition and a bit shift.
--    
--    This implementation does that, but scales the input and output spaces accordingly (so -pi/2 is 0 and pi/2 is 2^15).
--    angles > 2^15 are reversed in the same way the triangle wave reverses values past 2^15 so that we get a smooth up and down.
-- 
-- Clock cycles: 8
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity cordic16 is
  port(
    clk, reset : in  std_logic;
    phase      : in  unsigned(15 downto 0);
    amp        : out unsigned(15 downto 0)
  );
end cordic16;

architecture cordic16_behavior of cordic16 is
  -- cordic requires a lookup table of the values of each angle
  type CORDIC_TABLE is array (0 to 14) of unsigned(15 downto 0);
  signal ctable : CORDIC_TABLE := (
    to_unsigned(8192   ,16),
    to_unsigned(4836   ,16),
    to_unsigned(2555   ,16),
    to_unsigned(1297   ,16),
    to_unsigned(651    ,16),
    to_unsigned(326    ,16),
    to_unsigned(163    ,16),
    to_unsigned(81     ,16),
    to_unsigned(41     ,16),
    to_unsigned(20     ,16),
    to_unsigned(10     ,16),
    to_unsigned(5      ,16),
    to_unsigned(3      ,16),
    to_unsigned(1      ,16),
    to_unsigned(1      ,16)
  );
  signal corrected_angle : unsigned(15 downto 0) := (others => '0');
  signal amp_int         : unsigned(16 downto 0) := (others => '0');
  -- starting unit vector, adjusted for multipliers and output space
  signal sine   : unsigned(16 downto 0) := to_unsigned(19897, 17); 
  signal cosine : unsigned(16 downto 0) := (others => '0');
  -- we want to latch:
  --   1. input values
  --   2., 3., 4. values between each cell (cell1 => cell2, cell2 => cell3, cell3 => cell4)
  --   4. the output value
  type REGS is array (7 downto 0) of unsigned(16 downto 0); 
  signal reg_now_sin, reg_next_sin : REGS := (
    others => (others => '0')
  );
  signal reg_now_cos, reg_next_cos : REGS := (
    others => (others => '0')
  );
  type REGS_ANG is array (7 downto 0) of unsigned(15 downto 0); 
  signal reg_now_ang, reg_next_ang : REGS_ANG := (
    others => (others => '0')
  );
  component cordic_cell is
    generic( shamt : natural := 0);
    port(
      angle             : in  unsigned(15 downto 0);
      sine, cosine      : in  unsigned(16 downto 0);
      -- table values
      tv1, tv2                 : in  unsigned(15 downto 0);
      sine_out, cosine_out     : out unsigned(16 downto 0);
      angle_out                : out unsigned(15 downto 0)
    );
  end component;
begin
-- register
  process (clk,reset)
  begin
    if (reset='1') then
      for i in 0 to 7 loop
        reg_now_sin(i) <= (others => '0');
        reg_now_cos(i) <= (others => '0');
        reg_now_ang(i) <= (others => '0');
      end loop;
    elsif (rising_edge(clk)) then
      for i in 0 to 7 loop
        reg_now_sin(i) <= reg_next_sin(i);
        reg_now_cos(i) <= reg_next_cos(i);
        reg_now_ang(i) <= reg_next_ang(i);
      end loop;
    end if;
  end process;
-- next-state logic
  -- use normal phase when < 2^15, otherwise invert it to count down
  corrected_angle <= phase when phase(15)='0' else not phase;
  reg_next_sin(0) <= sine;
  reg_next_cos(0) <= cosine;
  reg_next_ang(0) <= corrected_angle;
  cell1: cordic_cell
    generic map( shamt => 0 )
    port map(
        angle =>      reg_now_ang(0),
        sine =>       reg_now_sin(0),
        cosine =>     reg_now_cos(0),
        tv1 =>        ctable(0),
        tv2 =>        ctable(1),
        sine_out =>   reg_next_sin(1),
        cosine_out => reg_next_cos(1), 
        angle_out =>  reg_next_ang(1) 
    );
  cell2: cordic_cell
    generic map( shamt => 2 )
    port map(
        angle =>      reg_now_ang(1),
        sine =>       reg_now_sin(1),
        cosine =>     reg_now_cos(1),
        tv1 =>        ctable(2),
        tv2 =>        ctable(3),
        sine_out =>   reg_next_sin(2),
        cosine_out => reg_next_cos(2), 
        angle_out =>  reg_next_ang(2) 
    );
  cell3: cordic_cell
    generic map( shamt => 4 )
    port map(
        angle =>      reg_now_ang(2),
        sine =>       reg_now_sin(2),
        cosine =>     reg_now_cos(2),
        tv1 =>        ctable(4),
        tv2 =>        ctable(5),
        sine_out =>   reg_next_sin(3),
        cosine_out => reg_next_cos(3), 
        angle_out =>  reg_next_ang(3) 
    );
  cell4: cordic_cell
    generic map( shamt => 6 )
    port map(
        angle =>      reg_now_ang(3),
        sine =>       reg_now_sin(3),
        cosine =>     reg_now_cos(3),
        tv1 =>        ctable(6),
        tv2 =>        ctable(7),
        sine_out =>   reg_next_sin(4),
        cosine_out => reg_next_cos(4), 
        angle_out =>  reg_next_ang(4) 
    );
  cell5: cordic_cell
    generic map( shamt => 8 )
    port map(
        angle =>      reg_now_ang(4),
        sine =>       reg_now_sin(4),
        cosine =>     reg_now_cos(4),
        tv1 =>        ctable(8),
        tv2 =>        ctable(9),
        sine_out =>   reg_next_sin(5),
        cosine_out => reg_next_cos(5), 
        angle_out =>  reg_next_ang(5) 
    );
  cell6: cordic_cell
    generic map( shamt => 10 )
    port map(
        angle =>      reg_now_ang(5),
        sine =>       reg_now_sin(5),
        cosine =>     reg_now_cos(5),
        tv1 =>        ctable(10),
        tv2 =>        ctable(11),
        sine_out =>   reg_next_sin(6),
        cosine_out => reg_next_cos(6), 
        angle_out =>  reg_next_ang(6) 
    );
  cell7: cordic_cell
    generic map( shamt => 12 )
    port map(
        angle =>      reg_now_ang(6),
        sine =>       reg_now_sin(6),
        cosine =>     reg_now_cos(6),
        tv1 =>        ctable(12),
        tv2 =>        ctable(13),
        sine_out =>   reg_next_sin(7),
        cosine_out => reg_next_cos(7), 
        angle_out =>  reg_next_ang(7) 
    );
-- output logic
  amp_int <= reg_now_cos(7) + to_unsigned((2**15), 17);
  amp <= amp_int(15 downto 0);
end cordic16_behavior;