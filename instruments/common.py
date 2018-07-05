import numpy as np
from astropy.io import fits

def find_first_index(arr, value):
    """ find the first element equal to value in the array arr """
    try:
        return next(i for i, v in enumerate(arr) if v == value)
    except StopIteration:
        raise Exception("Value %s not found" % value)


class getter:
    """ gets data from a header (dict) """

    def __init__(self, header, info, mode):
        self.header = header
        self.info = info
        self.index = find_first_index(info["modes"], mode)
        self.id = info["id"][self.index]

    def __call__(self, key, alt=None):
        return self.get(key, alt)

    def get(self, key, alt=None):
        value = self.info[key]
        if isinstance(value, list):
            value = value[self.index]
        if isinstance(value, str):
            value = value.format(id=self.id)
            value = self.header.get(value, alt)
        return value


class instrument:
    def load_info(self):
        raise NotImplementedError("Instrument info must be defined for each instrument seperately")

    def add_header_info(self, header, mode, *args, **kwargs):
        """ read data from header and add it as REDUCE keyword back to the header """
        info = self.load_info()
        get = getter(header, info, mode)

        header["e_orient"] = get("orientation")

        naxis_x = get("naxis_x")
        naxis_y = get("naxis_y")

        prescan_x = get("prescan_x")
        overscan_x = get("overscan_x")
        prescan_y = get("prescan_y")
        overscan_y = get("overscan_y")

        header["e_xlo"] = prescan_x
        header["e_xhi"] = naxis_x - overscan_x

        header["e_ylo"] = prescan_y
        header["e_yhi"] = naxis_y - overscan_y

        header["e_gain"] = get("gain")
        header["e_readn"] = get("readnoise")
        header["e_exptim"] = get("exposure_time")

        header["e_sky"] = get("sky", 0)
        header["e_drk"] = get("dark", 0)
        header["e_backg"] = header["e_gain"] * (header["e_drk"] + header["e_sky"])

        header["e_imtype"] = get("image_type")
        header["e_ctg"] = get("category")

        header["e_ra"] = get("ra")
        header["e_dec"] = get("dec")
        header["e_jd"] = get("jd")

        header["e_obslon"] = get("longitude")
        header["e_obslat"] = get("latitude")
        header["e_obsalt"] = get("altitude")

        return header

    def sort_files(self, files, target, mode, *args, **kwargs):
        """
        Sort a set of fits files into different categories
        types are: bias, flat, wavecal, orderdef, spec

        Parameters
        ----------
        files : list(str)
            files to sort
        target : str
            name of the observed target (as present in the header files of the observation)
        mode : str
            mode of the instrument to search for
        Returns
        -------
        biaslist, flatlist, wavelist, orderlist, speclist
            lists of files, one per type
        """
        info = self.load_info()

        # TODO is this also instrument specific? Probably
        # TODO use instrument info instead of settings for labels?
        ob = np.zeros(len(files), dtype="U20")
        ty = np.zeros(len(files), dtype="U20")
        mo = np.zeros(len(files), dtype="U20")

        for i, f in enumerate(files):
            h = fits.open(f)[0].header
            ob[i] = h[info["target"]]
            ty[i] = h[info["observation_type"]]
            mo[i] = h.get(info["instrument_mode"], "")

        # TODO instrument mode check
        biaslist = files[ty == info["id_bias"]]
        flatlist = files[ty == info["id_flat"]]
        wavelist = files[ob == info["id_wave"]]
        orderlist = files[ob == info["id_orders"]]
        speclist = files[ob == target]

        return biaslist, flatlist, wavelist, orderlist, speclist