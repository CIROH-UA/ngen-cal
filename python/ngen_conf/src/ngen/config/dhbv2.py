from __future__ import annotations

from pydantic import PyObject, Field
from typing import Literal, Union
from .bmi_formulation import BMIPython

class dHBV2(BMIPython):
    """A BMIPython implementation for an ngen dhbv2 mdel"""
    #should all be reasonable defaults for dhbv2
    python_type: Union[PyObject, str] = "dhbv2.mts_bmi.MtsDeltaModelBmi"
    main_output_variable: Literal["land_surface_water__runoff_volume_flux"] = "land_surface_water__runoff_volume_flux"
    #NOTE aliases don't propagate to subclasses, so we have to repeat the alias
    model_name: Literal["DeltaModelBmi"] = Field("DeltaModelBmi", alias="model_type_name")

    _variable_names_map =  {
            "atmosphere_water__liquid_equivalent_precipitation_rate": "precip_rate",
            "land_surface_air__temperature": "TMP_2maboveground",
            "atmosphere_air_water~vapor__relative_saturation": "SPFH_2maboveground",
            "land_surface_radiation~incoming~longwave__energy_flux": "DLWRF_surface",
            "land_surface_radiation~incoming~shortwave__energy_flux": "DSWRF_surface",
            "land_surface_air__pressure": "PRES_surface",
            "land_surface_wind__x_component_of_velocity": "UGRD_10maboveground",
            "land_surface_wind__y_component_of_velocity": "VGRD_10maboveground",
            "land_surface_water__runoff_volume_flux": "streamflow_cms"
        }
