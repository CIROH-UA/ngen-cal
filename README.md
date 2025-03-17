# What is this?
This ngiab_cal branch represents the first attempt at getting ngen-cal running with nextgen in a box.

# Disclaimer
This is in development, while it does technically work, the link between the ngiab/data_preprocessor and this is fragile. If anything goes wrong the errors will probably be obscured inside the docker image. Understanding docker containers and how to exec into them is highly reccomended if you'd like to debug this. This does not necessarily represent the final calibration tooling that will be paired ngiab, it will likely have features removed and simplified to make it more user friendly. The steps performed by the preprocessor will likely also be moved into the ngiab_cal image/process to make it more flexible.

## How do I use this?

1) follow the dev preprocessor [instructions here](https://github.com/CIROH-UA/NGIAB_data_preprocess/tree/main?tab=readme-ov-file#development-installation) and install the `cal` branch of the preprocessor 
2) run one of the preprocessor commands for your area of interest (it has to be a gage for now). it needs to contain the `-sfr --cal` options. subset, forcings, realization (config) and --cal to generate the files required to run the calibration in this branch. The start and end times should be >3 years apart. e.g. `python -m ngiab_data_cli -i gage-10154200 -sfr --cal --start 2010-01-01 --end 2015-02-28` 
3) If you're feeling lucky, add `--run` to the command and it will attempt to automatically calibrate for the [default settings](https://github.com/CIROH-UA/NGIAB_data_preprocess/blob/cal/modules/data_sources/ngen_cal_conf.yaml) noah-owp-modular + cfe for 100 iterations.
4) All of the files used for and created by calibration will be put in the `calibration` directory.
For example in the command above and default preprocessor output folder, `~/ngiab_preprocess_output/gage-10154200/calibration/` the root folder is named after the input and can be changed by adding `-o folder_name`. THERE IS NO OVERWRITE PROTECTION FOR DIFFERENT TIMES AT THE SAME PLACE.
#### manually running the image
5) To run the calibration manually, copy the command printed in the preprocessor log output or construct it yourself. `docker run -it -v "home/user/ngiab_preprocess_output/gage-10154200/:/ngen/ngen/data" joshcu/ngiab-cal` replace joshcu/ngiab-cal with the name of your image if you built it from this repo
6) The image is functionally identical to ngiab's normal internals, but there's an additional /calibration/ folder with all the stuff in this branch in it and the `dmod/bin/mpi-ngen` script pretending to be a binary. Inside `/calibration/` there is a `run.sh` script that will run ngen cal against the contents of the `/ngen/ngen/data/calibration/` folder. This folder needs to be populated by the cal branch of the preprocessor.

# Notes
* If you want to modify the calibration config, I'd recommend modifying the [template in the preprocessor](https://github.com/CIROH-UA/NGIAB_data_preprocess/blob/cal/modules/data_sources/ngen_cal_conf.yaml) as there's no overwrite protection inside the individual calibration folders.
* __THIS WILL OVERWRITE MANUAL CHANGES TO ngen_cal_conf.yaml__ if using the preprocessor `--run` command OR running the preprocess over an already calibrated folder, it will search for the best parameter set over all the runs and add best_realization.json to your config folder. e.g. `~/ngiab_preprocess_output/gage-10154200/config/best_realization.json` to run the preprocess with JUST this realization generation, remove `-sfr` and just keep `--cal`. e.g. `python -m ngiab_data_cli -i gage-10154200 --cal --start 2010-01-01 --end 2015-02-28` 
* optionally build the container with `docker build -t ngiab_cal .` in the root of this repo.
* mpi-ngen is a script used in the place of the nextgen binary to allow ngen serial commands to be run in parallel. simply replace `ngen-serial` with `mpi-ngen` in the run command and it will automatically try and perform the extra steps needed to run a simulation with mpi. It is a modification of the current [ngiab guide.sh script](https://github.com/CIROH-UA/NGIAB-CloudInfra/blob/main/guide.sh)
