-- ** ===================================== **
--  Circuit: CORDIC Iteration                           
--  Author: Jake Bernard                               
--  Date Created: 2025-05-07                              
--  Desc:                                                        
--
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity cordic_op is
  port(
    angle                    : in  unsigned(15 downto 0);
    sine, cosine             : in  unsigned(16 downto 0);
    sh_sine, sh_cosine       : in  unsigned(16 downto 0);
    table_value              : in  unsigned(15 downto 0);
    sine_out, cosine_out     : out unsigned(16 downto 0);
    angle_out                : out unsigned(15 downto 0)
  );
end cordic_op;

architecture cordic_op_behavior of cordic_op is
  signal cat_sin, cat_cos, cat_sh_sin, cat_sh_cos : unsigned(17 downto 0) := (others => '0');
  signal sum_cos, sum_sin : unsigned(17 downto 0) := (others => '0');
  signal cat_angle, cat_table_val, sum_ang : unsigned(16 downto 0) := (others => '0');
  signal sigma : std_logic;
  signal skip  : std_logic := '0';
  constant halfway : natural := 16384;
begin
  sigma <= '1' when angle > halfway else '0';
  skip <= '1' when angle = 0 else '0';
  cat_sh_sin <= sh_sine(16) & sh_sine;
  cat_sh_cos <= sh_cosine(16) & sh_cosine;
  cat_sin <= sine(16) & sine;
  cat_cos <= cosine(16) & cosine;
  cat_angle <= '0' & angle;
  cat_table_val <= '0' & table_value;
  process (cat_cos,cat_sh_sin,cat_sin,cat_sh_cos,cat_angle,cat_table_val,sigma)
  begin
      -- bad and unoptimized but im running out of time
      case sigma is
        when '1' =>
          sum_cos <= cat_cos - cat_sh_sin;
          sum_sin <= cat_sin + cat_sh_cos;
          sum_ang <= cat_angle - cat_table_val;
      when others=>
        sum_cos <= cat_cos + cat_sh_sin;
        sum_sin <= cat_sin - cat_sh_cos;
        sum_ang <= cat_angle + cat_table_val;
      end case;
  end process;
  process (skip, sum_cos, sum_sin, sum_ang, angle, sine, cosine)
  begin
    if skip='1' then
      cosine_out <= cosine;
      sine_out   <= sine;
      angle_out  <= angle;
    else
      cosine_out <= sum_cos(16 downto 0);
      sine_out   <= sum_sin(16 downto 0);
      angle_out  <= sum_ang(15 downto 0);
    end if;
  end process;
end cordic_op_behavior;