# Vladislav 19.02.21
# Validate input data

def validate(gamma, small_delta, big_delta, full_spectra, gradients, left_point, right_point):
    valid = True
    msg = 'All right'
    if isinstance(gamma, int) or isinstance(gamma, float):
        pass
    else:
        valid = False
        msg = 'Gamma is not a number!'

    if isinstance(small_delta, int) or isinstance(small_delta, float) and small_delta > 0:
        pass
    else:
        valid = False
        msg = 'Gradient pulse duration is not a number or less or equal than 0!'

    if isinstance(big_delta, int) or isinstance(big_delta, float) and big_delta > small_delta:
        pass
    else:
        valid = False
        msg = 'Diffusion time is not a number or diffusion time is less or equal than Gradient pulse duration!'
    spectra_len = len(full_spectra[1])
    number_of_spectra = len(full_spectra)
    if isinstance(left_point, int) and left_point < int(spectra_len):
        pass
    else:
        valid = False
        msg = 'Left point is not int or bigger than spectrum length!'

    return valid, msg
