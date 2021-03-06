# Climlab Preconfigured Energy Balance Models¶

This model is based on the Climlab [example available here](https://climlab.readthedocs.io/en/latest/courseware/Preconfigured_EBM.html).

## Usage

This model can be run with:

```
python3 main.py --t0=11.1 --water_depth=12  
```

Additionally, the `timestep` can be set in `parameters.json`.

## Parameters:

* `t0`: base value for initial temperature
    * default is `12`
    * units are `°C`
* `water_depth`: depth of zonal_mean_surface domain, which the heat capacity is dependent on
    * default is `10`
    * units are `m`
* `timestep`: specifies the EBM’s timestep
    * default is `(365.2422 * 24 * 60 * 60 ) / 90`
    * units are `s`

## Outputs:

This model produces 2 outputs:

1. `ebm_model_results.nc`: netCDF file containing the model output
2. `ebm_results.png`: plot of the model output

 ![Example output](plots/ebm_results.png)
