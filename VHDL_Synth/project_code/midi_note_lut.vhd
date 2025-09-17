-- ** ===================================== **
--  Circuit: MIDI Note Frequency Lookup Table                             
--  Author: Jake Bernard                               
--  Date Created: 2025-05-06                             
--  Desc:                                                        
--                                 
-- ** ===================================== **

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.math_real.all;

entity midi_note_lut is
  port(
    -- 128 different midi notes
    note_in    : in unsigned(6 downto 0);
    freq_out   : out unsigned(26 downto 0)
  );
end midi_note_lut;

architecture midi_note_lut_behavior of midi_note_lut is
  -- highest frequency's control word only needs 15 bits -- ceil(log2(16836))
  --  we're only storing the highest frequency version of each note since that has the most bits of precision.
  --  lower frequency notes are just bit-shifted.
  type ROM_TOP is array (11 downto 0) of unsigned(14 downto 0);
  -- each frequency has 2 important bits of information to extract:
  --    1. the amount to shift the top frequency by (index 1)
  --    2. its value mod 12 (index 0) 
  type LOOKUP_TUPLE is array (1 downto 0) of unsigned(3 downto 0);
  -- doing this instead of storing every single note saves 716 bits
  type TUPLE_ROM is array (127 downto 0) of LOOKUP_TUPLE;

  -- numbers found using formula described in phase accumulator file:
  --   freq / (clock freq / 2^(counter bits))
  constant NOTE_ROM_TOP : ROM_TOP := (
  -- G9  
    to_unsigned(16836, 15),
  -- Gb9
    to_unsigned(15891, 15),
  -- F9
    to_unsigned(14999, 15),
  -- E9
    to_unsigned(14157, 15),
  -- Eb9
    to_unsigned(13363, 15),
  -- D9
    to_unsigned(12613, 15),
  -- Db9
    to_unsigned(11905, 15),
  -- C9
    to_unsigned(11237, 15),
  -- B8
    to_unsigned(10606, 15),
  -- Bb8
    to_unsigned(10011, 15),
  -- A8
    to_unsigned(9449, 15),
  -- Ab8
    to_unsigned(8919, 15)
  );
  -- create lookup table for each note number
  -- used this thread as a reference for writing functions: https://www.eevblog.com/forum/microcontrollers/vhdl-initializing-large-arrays-and-using-lookup-tables/
  function create_lut return TUPLE_ROM is
  variable rom : TUPLE_ROM;
  begin
    for i in 127 downto 0 loop
      -- we start at C, but the ROM lookup starts at Ab, so we have to correct for this by adding 4
      rom(i)(0) := to_unsigned((i + 4) mod 12, 4);
      rom(i)(1) := to_unsigned(10 - ((i + 4) / 12), 4);
    end loop;
    return rom;
  end function;
  constant NOTE_TO_SHIFT_AND_MOD : TUPLE_ROM := create_lut;

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
  signal note_tuple : LOOKUP_TUPLE;
  signal freq_int     : unsigned(14 downto 0);
  signal freq_out_int : unsigned(14 downto 0);

  constant ZERO_PADDING : std_logic_vector(11 downto 0) := (others => '0');
begin
  note_tuple <= NOTE_TO_SHIFT_AND_MOD(to_integer(note_in));
  freq_int <= NOTE_ROM_TOP(to_integer(note_tuple(0)));
  freq_shift : barrel_rlog_shifter
    generic map( 15 )
    port map(
      in_vec => freq_int ,
      shamt => note_tuple(1),
      out_vec => freq_out_int
    );
  freq_out <= unsigned(ZERO_PADDING & std_logic_vector(freq_out_int));
end midi_note_lut_behavior;