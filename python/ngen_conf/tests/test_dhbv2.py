import pytest
from ngen.config.formulation import Formulation
from ngen.config.dhbv2 import dHBV2


def test_init(dhbv2_params):
    dhbv2 = dHBV2(**dhbv2_params)


def test_name_map(dhbv2_params):
    dhbv2 = dHBV2(**dhbv2_params)
    _t = dhbv2.name_map[
        "atmosphere_water__liquid_equivalent_precipitation_rate"
    ]
    assert _t == "precip_rate"


def test_no_lib(dhbv2_params):
    # Unlike the BMI Python version, the Rust version should always have a library
    dhbv2 = dHBV2(**dhbv2_params)
    assert "library" not in dhbv2.dict().keys()


@pytest.mark.parametrize("forcing", ["csv", "netcdf"], indirect=True)
def test_dhbv2_formulation(dhbv2_params, forcing):
    dhbv2 = dHBV2(**dhbv2_params)
    f = {"params": dhbv2, "name": "bmi_python"}
    dhbv2_formulation = Formulation(**f)
    _dhbv2 = dhbv2_formulation.params
    assert _dhbv2.name == "bmi_python"
    assert _dhbv2.model_name == "DeltaModelBmi"
    serialized = _dhbv2.dict(by_alias=True)
    assert serialized["model_type_name"] == "DeltaModelBmi"
