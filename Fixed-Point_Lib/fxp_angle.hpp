#ifndef FIXED_PT_ANGLE_HPP
#define FIXED_PT_ANGLE_HPP

#include "fxp.hpp"
#include "../util/gen_util.hpp"
#include <cmath>

using namespace GenUtil;

struct fxp_angle;

struct fxp_angle : bfxp32 {
  
  fxp_angle() = default;
  constexpr fxp_angle(bfxp32 n) : bfxp32(n) {}
  constexpr fxp_angle(int n) :  bfxp32(n) {}
  constexpr fxp_angle(float n) :  bfxp32(n) {}
  constexpr fxp_angle(double n) :  bfxp32(n) {}

  static constexpr int32_t pi = (3 << f_bits) + 9280;

  // member functions

  constexpr fxp32 cos() {
    fxp32 out = std::cos(this->as_double()); 
    return out;
  }

  constexpr fxp32 sin() {
    fxp32 out = std::sin(this->as_double()); 
    return out;
  }

  constexpr fxp32 tan() {
    fxp32 out = std::tan(this->as_double()); 
    return out;
  }


  // overloading

  constexpr fxp_angle& operator=(const bfxp32& other) {
    value = other.value;
    return *this;
  }

  constexpr fxp_angle& operator+=(const fxp_angle& rhs) {
    value = value + rhs.value;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator+=(const bfxp32& rhs) {
    value = value + rhs.value;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator+=(const int& rhs) {
    value = value + int_to(rhs);
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator+=(const float& rhs) {
    value = value + float_to(rhs);
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }


  constexpr fxp_angle& operator+=(const double& rhs) {
    value = value + double_to(rhs);
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }


  constexpr fxp_angle& operator-=(const fxp_angle& rhs) {
    value = value - rhs.value;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator-=(const bfxp32& rhs) {
    value = value - rhs.value;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator-=(const int& rhs) {
    value = value - int_to(rhs);
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator-=(float rhs) {
    value = value - float_to(rhs);
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator-=(double rhs) {
    value = value - double_to(rhs);
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }


  constexpr fxp_angle& operator*=(fxp_angle rhs) {
    value = (stype)(((uptype)value * (uptype)(rhs.value)));
    value = value + fxp_angle::one_half;
    value = value >> f_bits;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator*=(bfxp32 rhs) {
    value = (stype)(((uptype)value * (uptype)(rhs.value)));
    value = value + fxp_angle::one_half;
    value = value >> f_bits;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator*=(int rhs) {
    value = value * rhs;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator*=(float rhs) {
    value = (stype)(((uptype)value * (uptype)float_to(rhs)));
    value = value + fxp_angle::one_half;
    value = value >> f_bits;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }

  constexpr fxp_angle& operator*=(double rhs) {
    value = (stype)(((uptype)value * (uptype)double_to(rhs)));
    value = value + fxp_angle::one_half;
    value = value >> f_bits;
    int32_t tmp = value % fxp_angle::pi;
    int32_t half_turn = (value / fxp_angle::pi) % 2;
    if (half_turn) {
      int32_t a_sign = sgn_i32(value);
      value = -a_sign * fxp_angle::pi + tmp;
    }
    else {
      value = tmp;
    }
    return *this;
  }



};

constexpr fxp_angle operator+(const fxp_angle& a, const fxp_angle& b) {
  fxp_angle result = a;
  result += b;
  return result;
}

constexpr fxp_angle operator+(const fxp_angle& a, const bfxp32& b) {
  fxp_angle result = a;
  result += b;
  return result;
}

constexpr fxp_angle operator+(const fxp_angle& a, const int& b) {
  fxp_angle result = a;
  result += b;
  return result;
}

constexpr fxp_angle operator+(const fxp_angle& a, const float& b) {
  fxp_angle result = a;
  result += b;
  return result;
}

constexpr fxp_angle operator+(const fxp_angle& a, const double& b) {
  fxp_angle result = a;
  result += b;
  return result;
}

// right

constexpr fxp_angle operator+(const bfxp32& a, const fxp_angle& b) {
  fxp_angle result = a;
  result += b;
  return result;
}


constexpr fxp_angle operator+(const int& b, const fxp_angle& a) {
  fxp_angle result = a;
  result += b;
  return result;
}

constexpr fxp_angle operator+(const float& b, const fxp_angle& a) {
  fxp_angle result = a;
  result += b;
  return result;
}

constexpr fxp_angle operator+(const double& b, const fxp_angle& a) {
  fxp_angle result = a;
  result += b;
  return result;
}

// SUB

// left

constexpr fxp_angle operator-(const fxp_angle& a, const fxp_angle& b) {
  fxp_angle result = a;
  result -= b;
  return result;
}

constexpr fxp_angle operator-(const fxp_angle& a, const bfxp32& b) {
  fxp_angle result = a;
  result -= b;
  return result;
}

constexpr fxp_angle operator-(const fxp_angle& a, const int& b) {
  fxp_angle result = a;
  result -= b;
  return result;
}

constexpr fxp_angle operator-(const fxp_angle& a, const float& b) {
  fxp_angle result = a;
  result -= b;
  return result;
}

constexpr fxp_angle operator-(const fxp_angle& a, const double& b) {
  fxp_angle result = a;
  result -= b;
  return result;
}

// right

constexpr fxp_angle operator-(const bfxp32& a, const fxp_angle& b) {
  fxp_angle result = a;
  result -= b;
  return result;
}

constexpr fxp_angle operator-(const int& b, const fxp_angle& a) {
  fxp_angle result = b;
  result -= a;
  return result;
}

constexpr fxp_angle operator-(const float& b, const fxp_angle& a) {
  fxp_angle result = b;
  result -= a;
  return result;
}

constexpr fxp_angle operator-(const double& b, const fxp_angle& a) {
  fxp_angle result = b;
  result -= a;
  return result;
}


// MULT

// left

constexpr fxp_angle operator*(const fxp_angle& a, const fxp_angle& b) {
  fxp_angle result = a;
  result *= b;
  return result;
}

constexpr fxp_angle operator*(const fxp_angle& a, const bfxp32& b) {
  fxp_angle result = a;
  result *= b;
  return result;
}

constexpr fxp_angle operator*(const fxp_angle& a, const int& b) {
  fxp_angle result = a;
  result *= b;
  return result;
}

constexpr fxp_angle operator*(const fxp_angle& a, const float& b) {
  fxp_angle result = a;
  result *= b;
  return result;
}

constexpr fxp_angle operator*(const fxp_angle& a, const double& b) {
  fxp_angle result = a;
  result *= b;
  return result;
}

// right

constexpr fxp_angle operator*(const bfxp32& a, const fxp_angle& b) {
  fxp_angle result = a;
  result *= b;
  return result;
}

constexpr fxp_angle operator*(const int& b, const fxp_angle& a) {
  fxp_angle result = a;
  result *= b;
  return result;
}

constexpr fxp_angle operator*(const float& b, const fxp_angle& a) {
  fxp_angle result = a;
  result *= b;
  return result;
}

constexpr fxp_angle operator*(const double& b, const fxp_angle& a) {
  fxp_angle result = a;
  result *= b;
  return result;
}



#endif