# Vladislav 19.02.21
# Validate input data

def validate(gamma, small_delta, big_delta, p1, d16, full_spectra, gradients, left_point, right_point):
    valid = True
    msg = 'All right'
    spectra_len = len(full_spectra[1])
    spectra_numbers = len(full_spectra[:, 1])

    if isinstance(gamma, int) or isinstance(gamma, float):
        pass
    else:
        valid = False
        msg = 'Gamma is not a number!'

    if isinstance(small_delta, int) or isinstance(small_delta, float) and small_delta > 0:
        pass
    else:
        valid = False
        msg = 'Gradient pulse duration is not a number or Gradient pulse duration is less than 0!'

    if isinstance(big_delta, int) or isinstance(big_delta, float) and big_delta > 0:
        pass
    else:
        valid = False
        msg = 'Diffusion time is not a number or Diffusion time is less than 0!'

    # if isinstance(gradient_strength, int) or isinstance(gradient_strength, float) and gradient_strength > 0:
    #     pass
    # else:
    #     valid = False
    #     msg = 'Gradient strength is not a number or is less than 0 or equal!'

    if isinstance(left_point, int) and 0 < left_point < int(spectra_len):
        pass
    else:
        valid = False
        msg = 'Left point is not a number. Or Left point is out of the spectrum length!'

    if isinstance(right_point, int) and int(spectra_len) > right_point > left_point:
        pass
    else:
        valid = False
        msg = 'Right point is not int or bigger than spectrum length or smaller than left point!'

    if spectra_numbers >= len(gradients):
        pass
    else:
        valid = False
        msg = 'Spectrum number is smaller than gradients number in difflist!'

    if isinstance(d16, int) or isinstance(d16, float) and d16 > 0:
        pass
    else:
        valid = False
        msg = 'Delay d16 is not a number or Delay d16 is smaller than 0!'

    if isinstance(p1, int) or isinstance(p1, float) and p1 > 0:
        pass
    else:
        valid = False
        msg = '90 degree pulse is not a number or 90 degree pulse is smaller than 0!'

    return valid, msg
