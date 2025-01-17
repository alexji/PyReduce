import os.path
import numpy as np
import matplotlib.pyplot as plt
import pyreduce
from pyreduce import datasets, instruments, util, configuration
from pyreduce.wavelength_calibration import (
    WavelengthCalibration as WavelengthCalibrationModule,
)


def func_wavecal(
    deg, thar, instrument, mode, **kwargs
):
    reference = instruments.instrument_info.get_wavecal_filename(None, instrument, mode)
    reference = np.load(reference, allow_pickle=True)
    linelist = reference["cs_lines"]
    kwargs["degree"] = deg

    module = WavelengthCalibrationModule(**kwargs)
    wave, coef = module.execute(thar, linelist)

    return module.aic


def func_freq_comb(deg, comb, wave, **kwargs):
    kwargs["degree"] = deg
    module = WavelengthCalibrationModule(**kwargs)
    wave = module.frequency_comb(comb, wave)
    return module.aic


# define parameters
instrument = "HARPS"
target = "HD109200"
night = "2015-04-09"
mode = "red"

# some basic settings
# Expected Folder Structure: base_dir/datasets/HD132205/*.fits.gz
# Feel free to change this to your own preference, values in curly brackets will be replaced with the actual values {}

# load dataset (and save the location)
base_dir = datasets.HARPS("/DATA/PyReduce")
input_dir = "raw"
output_dir = f"reduced_{mode}"

config = configuration.get_configuration_for_instrument(instrument, plot=False)

f = os.path.join(base_dir, output_dir, "harps_red.thar.npz")
data = np.load(f, allow_pickle=True)
thar = data["thar"]
wave = data["wave"]

f = os.path.join(base_dir, output_dir, "harps_red.comb.npz")
data = np.load(f, allow_pickle=True)
comb = data["comb"]

ndim = 2
kwargs = config["wavecal"]
kwargs_comb = config["freq_comb"]
kwargs["dimensionality"] = f"{ndim}D"
kwargs_comb["dimensionality"] = f"{ndim}D"

for key in ["extraction_method", "extraction_width", "extraction_cutoff"]:
    del kwargs_comb[key]
    del kwargs[key]

shape = tuple([20] * ndim)
grid = np.zeros((*shape, ndim), int)
for i in np.ndindex(shape):
    grid[i] = i
    grid[i] += 1

matrix = util.gridsearch(func_wavecal, grid, args=(thar, instrument, mode), kwargs=kwargs)
np.save(f"matrix_{ndim}D.npy", matrix)

# matrix = util.gridsearch(func_freq_comb, grid, args=(comb, wave), kwargs=kwargs_comb)
# np.save(f"matrix_comb_{ndim}D.npy", matrix)

# matrix = np.load(f"matrix_comb_{ndim}D.npy")

if ndim == 1:
    plt.plot(grid[:, 0], matrix)
elif ndim == 2:
    idx = np.unravel_index(np.argmin(np.nan_to_num(matrix)), matrix.shape)
    # matrix = np.log(np.abs(matrix)) * np.sign(matrix)
    plt.imshow(matrix, origin="lower", cmap="viridis_r", vmax=-100000)
    cb = plt.colorbar()
    plt.plot(idx[1], idx[0], "rD")
    plt.xticks(range(shape[0]), labels=grid[:, 0, 0])
    plt.yticks(range(shape[1]), labels=grid[0, :, 1])
    plt.xlabel("degree in dispersion direction")
    plt.ylabel("degree in cross-dispersion direction")
    cb.ax.set_ylabel("AIC", rotation=-90, va="bottom")
    plt.tight_layout()
plt.show()
