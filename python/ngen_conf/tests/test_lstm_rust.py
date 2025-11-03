import pytest
from ngen.config.formulation import Formulation
from ngen.config.lstm_rust import LSTM_Rust


def test_init(lstm_rust_params):
    lstm_rust = LSTM_Rust(**lstm_rust_params)


def test_name_map(lstm_rust_params):
    lstm_rust = LSTM_Rust(**lstm_rust_params)
    _t = lstm_rust.name_map[
        "atmosphere_water__time_integral_of_precipitation_mass_flux"
    ]
    assert _t == "RAINRATE"


def test_lib(lstm_rust_params):
    # Unlike the BMI Python version, the Rust version should always have a library
    lstm_rust = LSTM_Rust(**lstm_rust_params)
    assert "library" in lstm_rust.dict().keys()


@pytest.mark.parametrize("forcing", ["csv", "netcdf"], indirect=True)
def test_lstm_rust_formulation(lstm_rust_params, forcing):
    lstm_rust = LSTM_Rust(**lstm_rust_params)
    f = {"params": lstm_rust, "name": "bmi_c"}
    lstm_rust_formulation = Formulation(**f)
    _lstm_rust = lstm_rust_formulation.params
    assert _lstm_rust.name == "bmi_c"
    assert _lstm_rust.model_name == "bmi_rust"
    serialized = _lstm_rust.dict(by_alias=True)
    assert serialized["model_type_name"] == "bmi_rust"
