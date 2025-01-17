import pytest

import numpy as np

from pyreduce import util
from pyreduce.trace_orders import mark_orders


def test_orders(instr, instrument, mode, files, settings, mask):
    if len(files["orders"]) == 0:
        pytest.skip(f"No order definition files found for instrument {instrument}")

    files = files["orders"][0]
    order_img, _ = instr.load_fits(files, mode, mask=mask)
    settings = settings["orders"]

    orders, column_range = mark_orders(
        order_img,
        min_cluster=settings["min_cluster"],
        filter_size=settings["filter_size"],
        noise=settings["noise"],
        opower=settings["degree"],
        border_width=settings["border_width"],
        manual=False,
        plot=False,
    )

    assert isinstance(orders, np.ndarray)
    assert np.issubdtype(orders.dtype, np.floating)
    assert orders.shape[1] == settings["degree"] + 1

    assert isinstance(column_range, np.ndarray)
    assert np.issubdtype(column_range.dtype, np.integer)
    assert column_range.shape[1] == 2
    assert np.all(column_range >= 0)
    assert np.all(column_range <= order_img.shape[1])

    assert orders.shape[0] == column_range.shape[0]


def test_simple():
    img = np.full((100, 100), 1)
    img[45:56, :] = 100

    orders, column_range = mark_orders(
        img, manual=False, opower=1, plot=False, border_width=0
    )

    assert orders.shape[0] == 1
    assert np.allclose(orders[0], [0, 50])

    assert column_range.shape[0] == 1
    assert column_range[0, 0] == 0
    assert column_range[0, 1] == 100


def test_parameters():
    img = np.full((100, 100), 1)
    img[45:56, :] = 100

    with pytest.raises(TypeError):
        mark_orders(None)
    with pytest.raises(TypeError):
        mark_orders(img, min_cluster="bla")
    with pytest.raises(TypeError):
        mark_orders(img, filter_size="bla")
    with pytest.raises(ValueError):
        mark_orders(img, filter_size=0)
    with pytest.raises(TypeError):
        mark_orders(img, noise="bla")
    with pytest.raises(TypeError):
        mark_orders(img, border_width="bla")
    with pytest.raises(ValueError):
        mark_orders(img, border_width=-1)
    with pytest.raises(TypeError):
        mark_orders(img, opower="bla")
    with pytest.raises(ValueError):
        mark_orders(img, opower=-1)
