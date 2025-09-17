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

#include "cplex_osc.hpp"

#define PTYPE(a,b) printf(#a " = %" #b "\n",a)

#define MAX(a,b) \
  ({ __typeof__ (a) _a = (a); \
      __typeof__ (b) _b = (b); \
    _a > _b ? _a : _b; })

#define MIN(a,b) \
  ({ __typeof__ (a) _a = (a); \
      __typeof__ (b) _b = (b); \
    _a < _b ? _a : _b; })

static SDL_Window *window = NULL;
static SDL_Renderer *renderer = NULL;
static SDL_Texture *texture = NULL;

using namespace DecentGfxUtil;
using namespace DecentMemory;
using namespace DecentGfxEZRender;

i32 window_width = 515;
i32 window_height = 475;

r32 fps = 0.f;
r32 perf_freq  = 0.f;
r32 perf_delta = 0;

ComplexFun<float>      float_oscs;
ComplexFun<double>     double_oscs;
ComplexFun<fxp<32,24>> bfxp32_oscs;
ComplexFun<fxp<32,28>> pfxp32_oscs;
ComplexFun<fxp<32,29>> hpfxp32_oscs;
ComplexFun<fxp<32,30>> pfxp64_oscs;

void init_oscs_again() {
  float_oscs.topleftx = 0;
  float_oscs.toplefty = 12;
  double_oscs.topleftx = 260;
  double_oscs.toplefty = 12;
  
  bfxp32_oscs.topleftx  = 0;
  bfxp32_oscs.toplefty  = 152+12;
  pfxp32_oscs.topleftx = 260;
  pfxp32_oscs.toplefty = 152+12;
  
  hpfxp32_oscs.topleftx  = 0;
  hpfxp32_oscs.toplefty  = 2*152+12;
  pfxp64_oscs.topleftx = 260;
  pfxp64_oscs.toplefty = 2*152+12;
  
  float_oscs.cnum_to_height   = fp_to_height<float>;
  double_oscs.cnum_to_height  = fp_to_height<double>;
  bfxp32_oscs.cnum_to_height  = fxp_to_height<fxp<32,24>>;
  pfxp32_oscs.cnum_to_height  = fxp_to_height<fxp<32,28>>;
  hpfxp32_oscs.cnum_to_height = fxp_to_height<fxp<32,29>>;
  pfxp64_oscs.cnum_to_height  = fxp_to_height<fxp<32,30>>;
  
  float_oscs.print_info   = fp_print_info<float>; 
  double_oscs.print_info  = fp_print_info<double>;  
  bfxp32_oscs.print_info  = fxp_print_info<fxp<32,24>>;  
  pfxp32_oscs.print_info  = fxp_print_info<fxp<32,28>>;
  hpfxp32_oscs.print_info = fxp_print_info<fxp<32,29>>;   
  pfxp64_oscs.print_info  = fxp_print_info<fxp<32,30>>;  
  
  float_oscs.renderer   = renderer;   
  double_oscs.renderer  = renderer;   
  bfxp32_oscs.renderer  = renderer;   
  pfxp32_oscs.renderer  = renderer;   
  hpfxp32_oscs.renderer = renderer;   
  pfxp64_oscs.renderer  = renderer; 
  
  

  float_oscs.init_sine_points();   
  double_oscs.init_sine_points();  
  bfxp32_oscs.init_sine_points();  
  pfxp32_oscs.init_sine_points();  
  hpfxp32_oscs.init_sine_points(); 
  pfxp64_oscs.init_sine_points();  
}


bool init_game() {

  SDL_SetAppMetadata("Engine Test", "1.0", NULL);

  if (!SDL_Init( SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_EVENTS )) {
    SDL_Log("Couldn't initialize SDL: %s", SDL_GetError());
    return false;
  }

  if (!SDL_CreateWindowAndRenderer("test", window_width, window_height, SDL_WINDOW_RESIZABLE, &window, &renderer)) {
    SDL_Log("Couldn't create window/renderer: %s", SDL_GetError());
    return false;
  }

  if(!SDL_SetRenderVSync( renderer, 1 )) {
    SDL_Log( "Could not enable VSync! SDL error: %s\n", SDL_GetError() );
    return false;
  }

  init_oscs_again();

  return true;
}



void debug_hud() {

  SDL_SetRenderDrawColor(
    renderer, 
    debug_text_color.r(), 
    debug_text_color.g(), 
    debug_text_color.b(), 
    SDL_ALPHA_OPAQUE
  );

  // font is 8x8 pixels
  SDL_RenderDebugTextFormat(renderer, 2, 2, "%04.2f FPS", round(fps));

}


void update_game() {
  float_oscs.update_sine();   
  double_oscs.update_sine();  
  bfxp32_oscs.update_sine();  
  pfxp32_oscs.update_sine();  
  hpfxp32_oscs.update_sine(); 
  pfxp64_oscs.update_sine(); 
  return;
}


void render_frame() {

  SDL_SetRenderDrawColor(renderer, 100, 100, 100, SDL_ALPHA_OPAQUE);
  SDL_RenderClear(renderer);

  float_oscs.render_sine();   
  double_oscs.render_sine();  
  bfxp32_oscs.render_sine();  
  pfxp32_oscs.render_sine();  
  hpfxp32_oscs.render_sine(); 
  pfxp64_oscs.render_sine(); 
  debug_hud();

  SDL_RenderPresent(renderer); 
}

int main(int argc, char **argv) {

  if (!init_game()) {
    SDL_Quit();
    return -1;
  }

  perf_freq = SDL_GetPerformanceFrequency();

  SDL_Event event;
  u32 current_time, last_time = 0;
  u64 perf_current_time, perf_last_time = 0;
  u32 framecount = 1;

  while (true) {
    
    perf_current_time = SDL_GetPerformanceCounter();
    current_time = SDL_GetTicks();

    perf_delta = (r32)(perf_current_time - perf_last_time);
    fps = perf_freq / perf_delta;
    if (current_time-last_time >= 16) {
      framecount = (framecount + 1) % (60 * 10);
      last_time = current_time;
      perf_last_time = perf_current_time;
      update_game();
      render_frame();
      if (framecount == 0) {
        float_oscs.mode   = !(float_oscs.mode  ); 
        double_oscs.mode  = !(double_oscs.mode );
        bfxp32_oscs.mode  = !(bfxp32_oscs.mode );
        pfxp32_oscs.mode  = !(pfxp32_oscs.mode );
        hpfxp32_oscs.mode = !(hpfxp32_oscs.mode);
        pfxp64_oscs.mode  = !(pfxp64_oscs.mode );
        float_oscs.gain_correct(); 
        double_oscs.gain_correct();
        bfxp32_oscs.gain_correct();
        pfxp32_oscs.gain_correct();
        hpfxp32_oscs.gain_correct();
        pfxp64_oscs.gain_correct();
      }
    }

    if (!SDL_PollEvent(&event)) {
      continue;
    }

    switch (event.type) {

      case SDL_EVENT_QUIT:
        SDL_Quit();
        return 0;
      
      case SDL_EVENT_WINDOW_RESIZED:
        window_width = event.window.data1;
        window_height = event.window.data2;
        break;

    }

  } 
}

