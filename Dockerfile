FROM awiciroh/ciroh-ngen-image AS base
RUN dnf install -y git gcc-c++ make cmake python3-devel python3-pip
WORKDIR /calibration
RUN chmod -R 777 /calibration/
COPY ngen-cal/requirements.txt .
RUN uv venv
RUN uv pip install -r requirements.txt
COPY ngen-cal /calibration/ngen-cal
RUN chmod -R 777 /calibration/ngen-cal
RUN uv pip install -e ngen-cal/python/runCalibValid/ngen_cal
RUN uv pip install -e ngen-cal/python/runCalibValid/ngen_conf
RUN uv pip install numpy==1.26.0 netCDF4 geopandas==1.* xarray
RUN uv pip install colorama rich

COPY mpi-ngen /dmod/bin/mpi-ngen

RUN echo "/calibration/.venv/bin/python /calibration/ngen-cal/python/runCalibValid/calibration.py /ngen/ngen/data/calibration/ngen_cal_conf.yaml && \\" >> run.sh
RUN echo "/calibration/.venv/bin/python /calibration/ngen-cal/python/runCalibValid/validation.py /ngen/ngen/data/calibration/Output/Validation_Run/ngen_cal_conf.yaml" >> run.sh

RUN chmod +x run.sh

ENV VIRTUAL_ENV=/ngen/.venv/

# This is to stop matplotlib complaining
RUN mkdir -p /.config/
RUN mkdir -p /.cache/
RUN chmod -R 777 /.config/
RUN chmod -R 777 /.cache/

ENTRYPOINT [ "/bin/bash" ]
