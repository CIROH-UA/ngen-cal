from __future__ import annotations

from pydantic import Field
from typing import Literal
from .bmi_formulation import BMIC


class LSTM_Rust(BMIC):
    """A BMI Rust implementation of the BMI Python LSTM model"""

    # should all be reasonable defaults for LSTM
    main_output_variable: Literal["land_surface_water__runoff_depth"] = (
        "land_surface_water__runoff_depth"
    )
    # NOTE aliases don't propagate to subclasses, so we have to repeat the alias
    model_name: Literal["bmi_rust"] = Field("bmi_rust", alias="model_type_name")
    registration_function: str = "register_bmi_lstm"

    _variable_names_map = {
        "atmosphere_water__time_integral_of_precipitation_mass_flux": "RAINRATE"
    }
