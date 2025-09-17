#pragma once

#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
#include <SDL3/SDL_video.h>
#include <SDL3/SDL_timer.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#include "../fxp/fxp.hpp"
#include "../fxp/fxp_angle.hpp"
#include "../fxp/fxp_util.hpp"

#include "../gfx/gfx_util.hpp"
#include "../gfx/ezrender.hpp"

#include "../mem/allocators.hpp"

#include "../common/decent_types.hpp"
#include "../common/decent_defines.hpp"

Col8 debug_text_color = {6, 1, 2};

template <typename T>
r32 fxp_to_height(T s) {
  r32 out = s.as_float();
  return out * -60.0;
}

template <typename T>
r32 fp_to_height(T s) {
  return s * -60.0;
}

template <typename T>
void fp_print_info(T s, i32 tlx, i32 tly, u8 mode, SDL_Renderer* renderer) {
  const char* typename_f = "float";
  const char* typename_d = "double";
  const char* mode0 = "simple osc";
  const char* mode1 = "fm osc";
  SDL_SetRenderDrawColor(
    renderer, 
    debug_text_color.r(), 
    debug_text_color.g(), 
    debug_text_color.b(), 
    SDL_ALPHA_OPAQUE
  );
  SDL_RenderDebugTextFormat(renderer, tlx + 2, tly + 2, "type: %s", sizeof(T) == 4 ? typename_f : typename_d);
  SDL_RenderDebugTextFormat(renderer, tlx + 2, tly + 12, "mode: %s", mode == 0 ? mode0 : mode1);
  SDL_RenderDebugTextFormat(renderer, tlx + 2, tly + 22, "s=%+.5f", s);
}

template <typename T>
void fxp_print_info(T s, i32 tlx, i32 tly, u8 mode, SDL_Renderer* renderer) {
  const char* mode0 = "simple osc";
  const char* mode1 = "fm osc";
  SDL_SetRenderDrawColor(
    renderer, 
    debug_text_color.r(), 
    debug_text_color.g(), 
    debug_text_color.b(), 
    SDL_ALPHA_OPAQUE
  );
  SDL_RenderDebugTextFormat(renderer, tlx + 2, tly + 2, "type: fixed %d:%d", T::f_bits + T::i_bits, T::f_bits);
  SDL_RenderDebugTextFormat(renderer, tlx + 2, tly + 12, "mode: %s", mode == 0 ? mode0 : mode1);
  SDL_RenderDebugTextFormat(renderer, tlx + 2, tly + 22, "s=%+.5f", s.as_double());
}

template <typename cplex_type>
struct ComplexFun {

  cplex_type s;
  cplex_type c;
  cplex_type r_s;
  cplex_type r_c;
  cplex_type s2;
  cplex_type c2;
  cplex_type r_s2;
  cplex_type r_c2;

  i32 samples = 250;
  i32 topleftx = 120;
  i32 toplefty = 120;
  u8  mode = 0;

  SDL_Renderer* renderer;

  void update_complex_nums() {
    cplex_type new_s, new_c;
    new_s = s*r_s - c*r_c;
    new_c = s*r_c + c*r_s;
    s = new_s;
    c = new_c;
    if (mode) {
      new_s = s2*r_s2 - c2*r_c2;
      new_c = s2*r_c2 + c2*r_s2;
      s2 = new_s;
      c2 = new_c;
      new_s = s*s2 - c*c2;
      new_c = s*c2 + c*s2;
      s = new_s;
      c = new_c;
    }
  }

  void gain_correct() {
    cplex_type g_correct  =  ((cplex_type)0.5)*(((cplex_type)3) - (s*s + c*c));
    cplex_type g_correct2 =  ((cplex_type)0.5)*(((cplex_type)3) - (s2*s2 + c2*c2));
    cplex_type g_correctr  = ((cplex_type)0.5)*(((cplex_type)3) - (r_s*r_s + r_c*r_c));
    cplex_type g_correctr2 = ((cplex_type)0.5)*(((cplex_type)3) - (r_s2*r_s2 + r_c2*r_c2));
    s *= g_correct;
    c *= g_correct;
    s2 *= g_correct2;
    c2 *= g_correct2;
    r_s *= g_correctr;
    r_c *= g_correctr;
    r_s2 *= g_correctr2;
    r_c2 *= g_correctr2;
  }

  SDL_FPoint* sine_points;

  void init_sine_points() {
    s = 1;
    c = 0;
    r_s = cos(0.04);
    r_c = sin(0.04);
    s2 = 1;
    c2 = 0;
    r_s2 = cos(0.001);
    r_c2 = sin(0.001);
    sine_points = (SDL_FPoint*)calloc(samples, sizeof(SDL_FPoint));
    for (i32 i = 0; i < samples; i++) {
      sine_points[i].x = i + topleftx;
      sine_points[i].y = 32 + 60 + toplefty;
    }
  }

  r32 (*cnum_to_height)(cplex_type T);
  
  void (*print_info)(cplex_type T, i32 tlx, i32 tly, u8 mode, SDL_Renderer* renderer);

  void update_sine() {
    update_complex_nums();
    for (i32 i = 0; i < samples-1; i++) {
      sine_points[i].y = sine_points[i+1].y;
    }
    sine_points[samples-1].y = cnum_to_height(s) + 32 + 60 + toplefty;
  }

  void render_sine() {
    SDL_SetRenderDrawColor(
      renderer, 
      255, 
      255, 
      255, 
      SDL_ALPHA_OPAQUE
    );
    SDL_RenderLines(renderer, sine_points, samples);
    SDL_SetRenderDrawColor(
      renderer, 
      0, 
      0, 
      0, 
      SDL_ALPHA_OPAQUE
    );
    SDL_RenderLine(renderer, topleftx,  32+toplefty,      samples + topleftx, 32+toplefty);
    SDL_RenderLine(renderer,  topleftx, 32+toplefty+120,  samples + topleftx, 32+toplefty+120);
    print_info(s, topleftx, toplefty, mode, renderer);
  }
};