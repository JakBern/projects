-- ** ===================================== **
--  Circuit: CORDIC Cell (Do 3 Cordic Iterations in a Row)                          
--  Author: Jake Bernard                               
--  Date Created: 2025-05-07                              
--  Desc:                                                        
--
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity cordic_cell is
  generic( shamt : natural := 0 );
  port(
    angle                    : in  unsigned(15 downto 0);
    sine, cosine             : in  unsigned(16 downto 0);
    -- table values
    tv1, tv2                 : in  unsigned(15 downto 0);
    sine_out, cosine_out     : out unsigned(16 downto 0);
    angle_out                : out unsigned(15 downto 0)
  );
end cordic_cell;

architecture cordic_cell_behavior of cordic_cell is
  signal angle_int  : unsigned(15 downto 0) := (others => '0');
  signal cosine_int : unsigned(16 downto 0) := (others => '0');
  signal sine_int   : unsigned(16 downto 0) := (others => '0'); 
  type SHIFTED_INTERMEDIATE is array (1 downto 0) of unsigned(16 downto 0);
  signal sh_sin_int : SHIFTED_INTERMEDIATE := (
    (others => '0'),
    (others => '0')
  );
  signal sh_cos_int : SHIFTED_INTERMEDIATE := (
    (others => '0'),
    (others => '0')
  );
  component cordic_op is
    port(
      angle                    : in  unsigned(15 downto 0);
      sine, cosine             : in  unsigned(16 downto 0);
      sh_sine, sh_cosine       : in  unsigned(16 downto 0);
      table_value              : in  unsigned(15 downto 0);
      sine_out, cosine_out     : out unsigned(16 downto 0);
      angle_out                : out unsigned(15 downto 0)
    );
  end component;
begin
  sh_sin_int(0) <= unsigned(shift_right(signed(sine), shamt));
  sh_cos_int(0) <= unsigned(shift_right(signed(cosine), shamt));
  op1 : cordic_op
  port map(
    angle  => angle,
    sine   => sine,
    cosine => cosine,
    sh_sine     => sh_sin_int(0),
    sh_cosine   => sh_cos_int(0),
    table_value => tv1,
    sine_out   => sine_int,
    cosine_out => cosine_int,
    angle_out  => angle_int
  );
  
  sh_sin_int(1) <= unsigned(shift_right(signed(sine_int), shamt+1));
  sh_cos_int(1) <= unsigned(shift_right(signed(cosine_int), shamt+1));
  op2 : cordic_op
  port map(
    angle  => angle_int,
    sine   => sine_int,
    cosine => cosine_int,
    sh_sine     => sh_sin_int(1),
    sh_cosine   => sh_cos_int(1),
    table_value => tv2,
    sine_out   => sine_out,
    cosine_out => cosine_out,
    angle_out  => angle_out
  );
end cordic_cell_behavior;