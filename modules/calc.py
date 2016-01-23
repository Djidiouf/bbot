__author__ = 'Djidiouf'

# Project modules
import modules.textalteration
import modules.connection

import math


def main(i_string):
    math_functions = { # 9.2.1. Number-theoretic and representation functions
                       "ceil": math.ceil,              # math.ceil(x)
                       "copysign": math.copysign,      # math.copysign(x, y)
                       "fabs": math.fabs,              # math.fabs(x)
                       "factorial": math.factorial,    # math.factorial(x)
                       "floor": math.floor,            # math.floor(x)
                       "fmod": math.fmod,              # math.fmod(x, y)
                       "frexp": math.frexp,            # math.frexp(x)
                       "fsum": math.fsum,              # math.fsum(iterable)
                       "gcd": math.gcd,                # math.gcd(a, b)
                       "isclose": math.isclose,        # math.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)
                       "isfinite": math.isfinite,      # math.isfinite(x)
                       "isinf": math.isinf,            # math.isinf(x)
                       "isnan": math.isnan,            # math.isnan(x)
                       "ldexp": math.ldexp,            # math.ldexp(x, i)
                       "modf": math.modf,              # math.modf(x)
                       "trunc": math.trunc,            # math.trunc(x)
                       # 9.2.2. Power and logarithmic functions
                       "exp": math.exp,                # math.exp(x)
                       "expm1": math.expm1,            # math.expm1(x)
                       "log": math.log,                # math.log(x[, base])
                       "log1p": math.log1p,            # math.log1p(x)
                       "log2": math.log2,              # math.log2(x)
                       "log10": math.log10,            # math.log10(x)
                       "pow": math.pow,                # math.pow(x, y)
                       "sqrt": math.sqrt,              # math.sqrt(x)
                       # 9.2.3. Trigonometric functions
                       "acos": math.acos,              # math.acos(x)
                       "asin": math.asin,              # math.asin(x)
                       "atan": math.atan,              # math.atan(x)
                       "atan2": math.atan2,            # math.atan2(y, x)
                       "cos": math.cos,                # math.cos(x)
                       "hypot": math.hypot,            # math.hypot(x, y)
                       "sin": math.sin,                # math.sin(x)
                       "tan": math.tan,                # math.tan(x)
                       # 9.2.4. Angular conversion
                       "degrees": math.degrees,        # math.degrees(x)
                       "radians": math.radians,        # math.radians(x)
                       # .2.5. Hyperbolic functions
                       "acosh": math.acosh,            # math.acosh(x)
                       "asinh": math.asinh,            # math.asinh(x)
                       "atanh": math.atanh,            # math.atanh(x)
                       "cosh": math.cosh,              # math.cosh(x)
                       "sinh": math.sinh,              # math.sinh(x)
                       "tanh": math.tanh,              # math.tanh(x)
                       # 9.2.6. Special functions
                       "erf": math.erf,                # math.erf(x)
                       "erfc": math.erfc,              # math.erfc(x)
                       "gamma": math.gamma,            # math.gamma(x)
                       "lgamma": math.lgamma,          # math.lgamma(x)
                       # 9.2.7. Constants
                       "pi": math.pi,                  # math.pi
                       "e": math.e,                    # math.e
                       "inf": math.inf,                # math.inf
                       "nan": math.nan}                # math.nan

    compute_requested = eval(i_string, {"__builtins__": None}, math_functions)
    modules.connection.send_message("%s = %f" % (i_string, compute_requested))
