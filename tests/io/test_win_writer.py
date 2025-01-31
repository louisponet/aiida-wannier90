# -*- coding: utf-8 -*-
################################################################################
# Copyright (c), AiiDA team and individual contributors.                       #
#  All rights reserved.                                                        #
# This file is part of the AiiDA-wannier90 code.                               #
#                                                                              #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-wannier90 #
# For further information on the license, see the LICENSE.txt file             #
################################################################################

import pytest
from aiida.common.exceptions import InputValidationError
from aiida.orm import Dict, List


def test_create_win_string(generate_win_params_gaas, file_regression):
    from aiida_wannier90.io._write_win import _create_win_string

    file_regression.check(
        _create_win_string(**generate_win_params_gaas()),
        encoding='utf-8',
        extension='.win'
    )


def test_create_win_string_projections_list_of_str(
    generate_win_params_gaas, file_regression
):
    """Test _write_win for parameter projections using a List of str."""
    from aiida_wannier90.io._write_win import _create_win_string

    gaas_params = generate_win_params_gaas()
    gaas_params['projections'] = List(list=["Ga: p", "As: p"])
    file_regression.check(
        _create_win_string(**gaas_params), encoding='utf-8', extension='.win'
    )


def test_create_win_string_projections_list_of_dict(
    generate_win_params_gaas, file_regression
):
    """Test _write_win for parameter projections using a List of dict."""
    from aiida_wannier90.io._write_win import _create_win_string

    gaas_params = generate_win_params_gaas()
    gaas_params['projections'] = List(
        list=[{
            "kind_name": "Ga",
            "ang_mtm_name": ["p"]
        }, {
            "kind_name": "As",
            "ang_mtm_name": ["p"]
        }]
    )
    file_regression.check(
        _create_win_string(**gaas_params), encoding='utf-8', extension='.win'
    )


def test_create_win_string_projections_dict(
    generate_win_params_gaas, file_regression
):
    """Test _write_win for parameter projections using a List of str."""
    from aiida_wannier90.io._write_win import _create_win_string

    gaas_params = generate_win_params_gaas()
    gaas_params['projections'] = Dict(
        dict={
            "kind_name": "Ga",
            "ang_mtm_name": ["p"]
        }
    )
    file_regression.check(
        _create_win_string(**gaas_params), encoding='utf-8', extension='.win'
    )


def test_exclude_bands(generate_kpoints_mesh, file_regression):
    """Test _write_win for parameter exclude_bands"""
    from aiida_wannier90.io._write_win import _create_win_string

    # check excluding a single band
    # https://github.com/aiidateam/aiida-wannier90/pull/110
    parameters = {'exclude_bands': [1]}
    file_regression.check(
        _create_win_string(parameters, generate_kpoints_mesh(2)),
        encoding='utf-8',
        extension='.win'
    )

    # check values are positive
    # https://github.com/aiidateam/aiida-wannier90/pull/109
    parameters = {'exclude_bands': range(-1, 1)}
    with pytest.raises(InputValidationError):
        _create_win_string(parameters, generate_kpoints_mesh(2))
