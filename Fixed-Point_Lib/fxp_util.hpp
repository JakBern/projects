#ifndef FIXED_PT_UTILS_HPP
#define FIXED_PT_UTILS_HPP

#include "fxp.hpp"
#include "fxp_angle.hpp"
#include "gen_util.hpp"
#include "math.h"

namespace FxpUtil {

  // template <size_t size>
  // constexpr fxp<size, size - (size/4)> fxp_to_pfxp(fxp<size, size/4> a) {
  //   fxp<size, size - (size/4)> b;
  //   b.from_raw(a.as_raw() << (size/2));
  //   return b;
  // }

  // template <size_t size>
  // constexpr fxp<size, size/4> pfxp_to_fxp(fxp<size, size - (size/4)>  a) {
  //   fxp<size, size/4> b;
  //   b.from_raw(a.as_raw() >> (size/2));
  //   return b;
  // }

  template<size_t in_t, size_t in_f, size_t out_t, size_t out_f>
  constexpr fxp32 fxp_exp(fxp32 n) {
    fxp32 out = exp(n.as_double()); 
    return out;
  }

  constexpr fxp32 fxp_pow(fxp32 base, fxp32 expo) {
    fxp32 out = pow(base.as_double(), expo.as_double()); 
    return out;
  }

  constexpr fxp32 fxp_sqrt(fxp32 n) {
    fxp32 out = sqrt(n.as_double()); 
    return out;
  }

  constexpr fxp_angle fxp_atan2(fxp32 y, fxp32 x) {
    fxp_angle out = atan2(y.as_double(), x.as_double()); 
    return out;
  }

  constexpr fxp_angle deg2angle(double deg) {
    deg = deg * (3.14159265358979323846 / 180.0);
    fxp_angle out = deg;
    int32_t tmp = out.value % fxp_angle::pi;
    int32_t half_turn = (out.value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(out.value);
      out.value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      out.value = tmp;
    }
    return out;
  }
    
    



}

#endif
