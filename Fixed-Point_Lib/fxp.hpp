#ifndef FIXED_PT_HPP
#define FIXED_PT_HPP

#include <cstddef>
#include <cstdint>
#include <math.h>
#include "stdio.h"


template <size_t t>
struct type_by_size {
  using stype = void;
  using utype = void;
  using uptype = void;
};

template <>
struct type_by_size<8> {
  using stype  = int8_t;
  using utype  = uint8_t;
  using uptype = int16_t;
};

template <>
struct type_by_size<16> {
  using stype  = int16_t;
  using utype  = uint16_t;
  using uptype = int32_t;
};

template <>
struct type_by_size<32> {
  using stype  = int32_t;
  using utype  = uint32_t;
  using uptype = int64_t;
};

template <>
struct type_by_size<64> {
  using stype  = int64_t;
  using utype  = uint64_t;
  using uptype = __int128;
};


template<size_t base_size, size_t frac_size>
struct fxp {
  using stype  = typename type_by_size<base_size>::stype;
  using utype  = typename type_by_size<base_size>::utype;
  using uptype = typename type_by_size<base_size>::uptype;

  static inline constexpr size_t f_bits = frac_size;
  static inline constexpr size_t i_bits = base_size - frac_size;

  static inline constexpr utype i_mask = (((utype)(-1)) << f_bits);
  static inline constexpr utype f_mask = ~i_mask;
  static inline constexpr stype one = ((stype)1) << f_bits;
  static inline constexpr stype neg_one = i_mask;
  static inline constexpr stype max = ~((1) << (base_size-1));
  static inline constexpr stype neg_max = (stype)1 << (base_size-1);
  static inline constexpr stype eps = 1;
  static inline constexpr stype one_half = (stype)1 << (f_bits-1);

  stype value;

  void from_raw(int num) {
     value = num;
  }
  void from_int(int num) {
    value = num << f_bits;
  }
  void from_float(float num) {
    value = (stype)(num * (float)one);
  }
  void from_double(double num) {
    value = (stype)(num * (double)one);
  }

  static constexpr fxp<base_size,frac_size> make_from_raw(int num) {
    fxp<base_size,frac_size> out;
    out.value = num;
    return out;
  }
  static constexpr fxp<base_size,frac_size> make_from_int(int num) {
    fxp<base_size,frac_size> out = num;
    return out;
  }
  static constexpr fxp<base_size,frac_size> make_from_float(float num) {
    fxp<base_size,frac_size> out = num;
    return out;
  }
  static constexpr fxp<base_size,frac_size> make_from_double(double num) {
    fxp<base_size,frac_size> out = num;
    return out;
  }

  constexpr fxp<base_size,frac_size>() = default;
  constexpr fxp<base_size,frac_size>(int n) : value(int_to(n)) {}
  constexpr fxp<base_size,frac_size>(float n) : value(float_to(n)) {}
  constexpr fxp<base_size,frac_size>(double n) : value(double_to(n)) {}

  constexpr stype as_raw() const {
    return value;
  }
  constexpr stype as_int()  const{
    return (value + one_half) >> f_bits;
  }
  constexpr stype as_int_trunc() const {
    return value >> f_bits;
  }
  constexpr float as_float() const {
    return ((float)value) / (float)one;
  }
  constexpr double as_double() const {
    return ((double)value) / (double)one;
  }

  static constexpr stype int_to(int num) {
    return ((stype)num) << f_bits;
  }
  static constexpr stype float_to(float num) {
    return (stype)(num * (float)one);
  }
  static constexpr stype double_to(double num) {
    return (stype)(num * (double)one);
  }

  static constexpr fxp<base_size, frac_size> pi           = fxp<base_size,frac_size>(3.141592653589793238462643383);
  static constexpr fxp<base_size, frac_size> half_pi      = fxp<base_size,frac_size>(3.141592653589793238462643383 / 2.0);
  static constexpr fxp<base_size, frac_size> quarter_pi   = fxp<base_size,frac_size>(3.141592653589793238462643383 / 4.0);
  static constexpr fxp<base_size, frac_size> sixth_pi     = fxp<base_size,frac_size>(3.141592653589793238462643383 / 6.0);
  static constexpr fxp<base_size, frac_size> tau          = fxp<base_size,frac_size>(6.283185307179586476925286766);
  static constexpr fxp<base_size, frac_size> e            = fxp<base_size,frac_size>(2.718281828459045235360287471);

  static constexpr fxp<base_size, frac_size> fxp_one          = fxp<base_size,frac_size>::make_from_raw(one);
  static constexpr fxp<base_size, frac_size> fxp_one_half     = fxp<base_size,frac_size>::make_from_raw(one_half);
  static constexpr fxp<base_size, frac_size> fxp_eps          = fxp<base_size,frac_size>::make_from_raw(eps);
  static constexpr fxp<base_size, frac_size> fxp_neg_one      = fxp<base_size,frac_size>::make_from_raw(neg_one);
  static constexpr fxp<base_size, frac_size> fxp_max          = fxp<base_size,frac_size>::make_from_raw(max);
  static constexpr fxp<base_size, frac_size> fxp_neg_max      = fxp<base_size,frac_size>::make_from_raw(neg_max);

  // static class fns

  static fxp<base_size,frac_size> lerpf(
                                        fxp<base_size,frac_size> a,
                                        fxp<base_size,frac_size> b,
                                        float alpha
                                      ) {
    fxp<base_size,frac_size> alpha_fxp = float_to(alpha);
    return (1 - alpha_fxp)*a + (alpha_fxp)*b;
  }

  static fxp<base_size,frac_size> lerp(
                                        fxp<base_size,frac_size> a,
                                        fxp<base_size,frac_size> b,
                                        fxp<base_size,frac_size> alpha
                                      ) {
    return (1 - alpha)*a + (alpha)*b;
  }
  
  // class fns

  void lrshift(size_t shamt) {
    value = ((utype)value) >> shamt;
  }


  void print_bits() {
    for (utype index = 1 << base_size-1; index != 0; index >>= 1) {
      printf("%d", (index & value) != 0);
      if (index == one) {
      printf(".");
      }
    }
    printf("\n");
  }

  constexpr fxp<base_size, frac_size> cmult_a(const fxp<base_size, frac_size>& other) {
    value = other.value;
    return *this;
  }

  // assignment operators

  constexpr fxp<base_size, frac_size>& operator=(const fxp<base_size, frac_size>& other) {
    value = other.value;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator=(const int& other) {
    value = int_to(other);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator=(const float& other) {
    value = float_to(other);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator=(const double& other) {
    value = double_to(other);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator+=(fxp<base_size, frac_size> rhs) {
    value = value + rhs.value;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator+=(int rhs) {
    value = value + int_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator+=(float rhs) {
    value = value + float_to(rhs);
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator+=(double rhs) {
    value = value + double_to(rhs);
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator-=(fxp<base_size, frac_size> rhs) {
    value = value - rhs.value;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator-=(int rhs) {
    value = value - int_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator-=(float rhs) {
    value = value - float_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator-=(double rhs) {
    value = value - double_to(rhs);
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator*=(fxp<base_size, frac_size> rhs) {
    value = (stype)((((uptype)value * (uptype)(rhs.value)) + fxp<base_size,frac_size>::one_half) >> f_bits);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator*=(int rhs) {
    value = value * rhs;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator*=(float rhs) {
    value = (stype)(((uptype)value * (uptype)float_to(rhs)));
    value = value + fxp<base_size,frac_size>::one_half;
    value = value >> f_bits;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator*=(double rhs) {
    value = (stype)(((uptype)value * (uptype)double_to(rhs)));
    value = value + fxp<base_size,frac_size>::one_half;
    value = value >> f_bits;
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator/=(fxp<base_size, frac_size> rhs) {
    value = (stype)((((uptype)value << f_bits) / (uptype)(rhs.value)));
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator/=(int rhs) {
    value = value / rhs;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator/=(float rhs) {
    value = (stype)((((uptype)value << f_bits) / (uptype)float_to(rhs)));
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator/=(double rhs) {
    value = (stype)((((uptype)value << f_bits) / (uptype)double_to(rhs)));
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator%=(fxp<base_size, frac_size> rhs) {
    value = (stype)(((value) % (rhs.value)));
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator%=(int rhs) {
    value = (stype)(((value)  % int_to(rhs)));
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator%=(float rhs) {
    value = (stype)(((value) % float_to(rhs)));
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator%=(double rhs) {
    value = (stype)(((value) % double_to(rhs)));
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator&=(fxp<base_size, frac_size> rhs) {
    value = value & rhs.value;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator&=(int rhs) {
    value = value & int_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator&=(float rhs) {
    value = value & float_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator&=(double rhs) {
    value = value & double_to(rhs);
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator|=(fxp<base_size, frac_size> rhs) {
    value = value | rhs.value;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator|=(int rhs) {
    value = value | int_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator|=(float rhs) {
    value = value | float_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator|=(double rhs) {
    value = value | double_to(rhs);
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator^=(fxp<base_size, frac_size> rhs) {
    value = value ^ rhs.value;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator^=(int rhs) {
    value = value ^ int_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator^=(float rhs) {
    value = value ^ float_to(rhs);
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator^=(double rhs) {
    value = value ^ double_to(rhs);
    return *this;
  }


  constexpr fxp<base_size, frac_size>& operator<<=(int rhs) {
    value = value << rhs;
    return *this;
  }

  constexpr fxp<base_size, frac_size>& operator>>=(int rhs) {
    value = value >> rhs;
    return *this;
  }

  // unary operators

  constexpr fxp<base_size, frac_size>& operator++() {
    value = value + one;
    return *this;
  }

  constexpr stype operator++(int) {
    stype old = value;
    value = value + one;
    return old;
  }

  constexpr fxp<base_size, frac_size>& operator--() {
    value = value - one;
    return *this;
  }

  constexpr stype operator--(int) {
    stype old = value;
    value = value - one;
    return old;
  }

  constexpr bool operator!() {
    return !value;
  }

  constexpr fxp<base_size, frac_size> operator~() {
    fxp<base_size, frac_size> out;
    out.from_raw(~value);
    return out;
  }

  constexpr fxp<base_size, frac_size> operator-() const {
    fxp<base_size, frac_size> out;
    out.from_raw(-value);
    return out;
  }

  constexpr fxp<base_size, frac_size> operator+() const {
    fxp<base_size, frac_size> out;
    out.from_raw(+value);
    return out;
  }

};

// binary arithmetic operators

// ADD

// left

template<size_t t, size_t f>
constexpr fxp<t,f> operator+(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result;
  result.value = a.value;
  result.value += b.value;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator+(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result += b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator+(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result += b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator+(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result += b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f> operator+(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result += b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator+(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result += b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator+(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result += b;
  return result;
}

// SUB

// left

template<size_t t, size_t f>
constexpr fxp<t,f> operator-(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result;
  result.value = a.value;
  result.value -= b.value;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator-(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result -= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator-(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result -= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator-(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result -= b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f> operator-(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result -= a;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator-(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result -= a;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator-(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result -= a;
  return result;
}


// MULT

// left

template<size_t t, size_t f>
constexpr fxp<t,f> operator*(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result = a;
  result *= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator*(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result *= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator*(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result *= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator*(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result *= b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f> operator*(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result *= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator*(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result *= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator*(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result *= b;
  return result;
}


// DIV
// (TODO) could be made better by shifting fully on conversions instead of multiple shifts

// left

template<size_t t, size_t f>
constexpr fxp<t,f> operator/(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result = a;
  result /= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator/(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result /= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator/(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result /= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator/(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result /= b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f> operator/(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result /= a;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator/(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result /= a;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator/(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result /= a;
  return result;
}

// MOD
// (TODO) could be made better by shifting fully on conversions instead of multiple shifts

// left

template<size_t t, size_t f>
constexpr fxp<t,f> operator%(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result = a;
  result %= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator%(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result %= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator%(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result %= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator%(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result %= b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f> operator%(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result %= a;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator%(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result %= a;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f> operator%(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = b;
  result %= a;
  return result;
}

// BITWISE AND

// left

template<size_t t, size_t f>
constexpr fxp<t,f>operator&(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result = a;
  result &= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator&(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result &= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator&(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result &= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator&(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result &= b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f>operator&(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result &= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator&(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result &= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator&(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result &= b;
  return result;
}

// BITWISE OR

// left

template<size_t t, size_t f>
constexpr fxp<t,f>operator|(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result = a;
  result |= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator|(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result |= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator|(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result |= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator|(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result |= b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f>operator|(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result |= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator|(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result |= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator|(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result |= b;
  return result;
}

// BITWISE XOR

// left

template<size_t t, size_t f>
constexpr fxp<t,f>operator^(const fxp<t,f>& a, const fxp<t,f>& b) {
  fxp<t,f> result = a;
  result ^= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator^(const fxp<t,f>& a, const int& b) {
  fxp<t,f> result = a;
  result ^= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator^(const fxp<t,f>& a, const float& b) {
  fxp<t,f> result = a;
  result ^= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator^(const fxp<t,f>& a, const double& b) {
  fxp<t,f> result = a;
  result ^= b;
  return result;
}

// right

template<size_t t, size_t f>
constexpr fxp<t,f>operator^(const int& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result ^= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator^(const float& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result ^= b;
  return result;
}

template<size_t t, size_t f>
constexpr fxp<t,f>operator^(const double& b, const fxp<t,f>& a) {
  fxp<t,f> result = a;
  result ^= b;
  return result;
}

// LEFT SHIFT

template<size_t t, size_t f>
constexpr fxp<t,f>operator<<(const fxp<t,f>& a, const size_t& shamt) {
  fxp<t,f> result = a;
  result <<= shamt;
  return result;
}

// RIGHT (ARITHMETIC) SHIFT

template<size_t t, size_t f>
constexpr fxp<t,f>operator>>(const fxp<t,f>& a, const size_t& shamt) {
  fxp<t,f> result = a;
  result >>= shamt;
  return result;
}

// COMPARISON

// EQUALITY

// left

template<size_t t, size_t f>
constexpr bool operator==(fxp<t,f> a, const fxp<t,f>& b) {
  return a.value == b.value;
}

template<size_t t, size_t f>
constexpr bool operator==(fxp<t,f> a, const int& b) {
  return a.value == fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator==(fxp<t,f> a, const float& b) {
  return a.value == fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator==(fxp<t,f> a, const double& b) {
  return a.value == fxp<t,f>::double_to(b);
}

// right

template<size_t t, size_t f>
constexpr bool operator==(const int& b, fxp<t,f> a) {
  return a.value == fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator==(const float& b, fxp<t,f> a) {
  return a.value == fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator==(const double& b, fxp<t,f> a) {
  return a.value == fxp<t,f>::double_to(b);
}

// INEQUALITY

// left

template<size_t t, size_t f>
constexpr bool operator!=(fxp<t,f> a, const fxp<t,f>& b) {
  return a.value != b.value;
}

template<size_t t, size_t f>
constexpr bool operator!=(fxp<t,f> a, const int& b) {
  return a.value != fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator!=(fxp<t,f> a, const float& b) {
  return a.value != fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator!=(fxp<t,f> a, const double& b) {
  return a.value != fxp<t,f>::double_to(b);
}

// right

template<size_t t, size_t f>
constexpr bool operator!=(const int& b, fxp<t,f> a) {
  return a.value != fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator!=(const float& b, fxp<t,f> a) {
  return a.value != fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator!=(const double& b, fxp<t,f> a) {
  return a.value != fxp<t,f>::double_to(b);
}

// LESS THAN

// left

template<size_t t, size_t f>
constexpr bool operator<(fxp<t,f> a, const fxp<t,f>& b) {
  return a.value < b.value;
}

template<size_t t, size_t f>
constexpr bool operator<(fxp<t,f> a, const int& b) {
  return a.value < fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<(fxp<t,f> a, const float& b) {
  return a.value < fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<(fxp<t,f> a, const double& b) {
  return a.value < fxp<t,f>::double_to(b);
}

// right

template<size_t t, size_t f>
constexpr bool operator<(const int& b, fxp<t,f> a) {
  return a.value > fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<(const float& b, fxp<t,f> a) {
  return a.value > fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<(const double& b, fxp<t,f> a) {
  return a.value > fxp<t,f>::double_to(b);
}

// LESS THAN OR EQUAL TO

// left

template<size_t t, size_t f>
constexpr bool operator<=(fxp<t,f> a, const fxp<t,f>& b) {
  return a.value <= b.value;
}

template<size_t t, size_t f>
constexpr bool operator<=(fxp<t,f> a, const int& b) {
  return a.value <= fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<=(fxp<t,f> a, const float& b) {
  return a.value <= fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<=(fxp<t,f> a, const double& b) {
  return a.value <= fxp<t,f>::double_to(b);
}

// right

template<size_t t, size_t f>
constexpr bool operator<=(const int& b, fxp<t,f> a) {
  return a.value >= fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<=(const float& b, fxp<t,f> a) {
  return a.value >= fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator<=(const double& b, fxp<t,f> a) {
  return a.value >= fxp<t,f>::double_to(b);
}

// GREATER THAN

// left

template<size_t t, size_t f>
constexpr bool operator>(fxp<t,f> a, const fxp<t,f>& b) {
  return a.value > b.value;
}

template<size_t t, size_t f>
constexpr bool operator>(fxp<t,f> a, const int& b) {
  return a.value > fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>(fxp<t,f> a, const float& b) {
  return a.value > fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>(fxp<t,f> a, const double& b) {
  return a.value > fxp<t,f>::double_to(b);
}

// right

template<size_t t, size_t f>
constexpr bool operator>(const int& b, fxp<t,f> a) {
  return a.value < fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>(const float& b, fxp<t,f> a) {
  return a.value < fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>(const double& b, fxp<t,f> a) {
  return a.value < fxp<t,f>::double_to(b);
}

// GREATER THAN OR EQUAL TO

// left

template<size_t t, size_t f>
constexpr bool operator>=(fxp<t,f> a, const fxp<t,f>& b) {
  return a.value >= b.value;
}

template<size_t t, size_t f>
constexpr bool operator>=(fxp<t,f> a, const int& b) {
  return a.value >= fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>=(fxp<t,f> a, const float& b) {
  return a.value >= fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>=(fxp<t,f> a, const double& b) {
  return a.value >= fxp<t,f>::double_to(b);
}

// right

template<size_t t, size_t f>
constexpr bool operator>=(const int& b, fxp<t,f> a) {
  return a.value <= fxp<t,f>::int_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>=(const float& b, fxp<t,f> a) {
  return a.value <= fxp<t,f>::float_to(b);
}

template<size_t t, size_t f>
constexpr bool operator>=(const double& b, fxp<t,f> a) {
  return a.value <= fxp<t,f>::double_to(b);
}

typedef fxp<64, 16>  fxp64;
typedef fxp<32, 8>   fxp32;
typedef fxp<16, 4>   fxp16;
typedef fxp<8,  2>   fxp8;
typedef fxp<64, 32>  bfxp64;
typedef fxp<32, 16>  bfxp32;
typedef fxp<16, 8>   bfxp16;
typedef fxp<8,  4>   bfxp8;
typedef fxp<64, 48>  pfxp64;
typedef fxp<32, 24>  pfxp32;
typedef fxp<16, 12>  pfxp16;
typedef fxp<8,  6>   pfxp8;


#endif

