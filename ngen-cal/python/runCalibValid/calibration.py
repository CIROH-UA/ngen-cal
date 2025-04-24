"""
This is the main script to read calibration configuration file and execute calibration run.
@author: Nels Frazer and Xia Feng
"""

import argparse
import logging
from os import chdir
from pathlib import Path

import yaml
from logger_config import get_logger, setup_logging
from ngen.cal.agent import Agent
from ngen.cal.configuration import General
from ngen.cal.search import dds, dds_set, gwo_search, pso_search
from ngen.cal.strategy import Algorithm


def main(general: General, model_conf):
    """Main calibration function"""
    logger = get_logger(__name__)
    # Seed the random number generators if requested
    if general.random_seed is not None:
        import random

        random.seed(general.random_seed)
        import numpy as np

        np.random.seed(general.random_seed)
        logger.debug(f"Set random seed to {general.random_seed}")

    logger.info("Starting calibration process")

    """
    TODO calibrate each "catcment" independely, but there may be something interesting in grouping various formulation params
    into a single variable vector and calibrating a set of heterogenous formultions...
    """
    start_iteration = 0
    # Initialize the starting agent
    logger.debug("Initializing calibration agent")
    agent = Agent(model_conf, general.calib_path, general, general.log, general.restart)

    if general.strategy.algorithm == Algorithm.dds:
        start_iteration = general.start_iteration
        if general.restart:
            logger.info("Restarting from previous calibration run")
            start_iteration = agent.restart()
        func = dds_set  # FIXME what about explicit/dds
        logger.info(f"Using DDS algorithm, starting at iteration {start_iteration}")

    elif general.strategy.algorithm == Algorithm.pso:  # TODO how to restart PSO?
        if agent.model.strategy != "uniform":
            logger.error("Can only use PSO with the uniform model strategy")
            return
        if general.restart:
            logger.warning("Restart not supported for PSO search, starting at 0")
        func = pso_search
        logger.info("Using PSO algorithm")

    elif general.strategy.algorithm == Algorithm.gwo:
        if agent.model.strategy != "uniform":
            logger.error("Can only use GWO with the uniform model strategy")
            return
        if general.restart:
            start_iteration = agent.restart()
            logger.info(f"Restarting GWO from iteration {start_iteration}")
        func = gwo_search
        logger.info("Using GWO algorithm")

    logger.info(f"Starting calibration loop with strategy: {agent.model.strategy}")

    # NOTE this assumes we calibrate each catchment independently, it may be possible to design an "aggregate" calibration
    # that works in a more sophisticated manner.
    if (
        agent.model.strategy == "explicit"
    ):  # FIXME this needs a refactor...should be able to use a calibration_set with explicit loading
        logger.debug("Using explicit strategy for calibration")
        for catchment in agent.model.adjustables:
            logger.info(
                f"Starting calibration for catchment {catchment.id if hasattr(catchment, 'id') else 'unknown'}"
            )
            dds(start_iteration, general.iterations, catchment, agent)

    elif agent.model.strategy == "independent":
        logger.debug("Using independent strategy for calibration")
        func(start_iteration, general.iterations, agent)

    elif agent.model.strategy == "uniform":
        logger.debug("Using uniform strategy for calibration")
        func(start_iteration, general.iterations, agent)

    logger.info("Calibration process completed")


if __name__ == "__main__":
    # Create the command line parser
    parser = argparse.ArgumentParser(description="Calibrate catchments in NGEN architecture.")
    parser.add_argument(
        "config_file",
        type=Path,
        help="The configuration yaml file for catchments to be operated on",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level",
    )
    parser.add_argument("--log-dir", type=str, help="Directory to store log files (optional)")
    args = parser.parse_args()

    # Setup logging
    log_level = getattr(logging, args.log_level)
    setup_logging(log_level, args.log_dir)

    logger = get_logger(__name__)
    logger.info(f"Reading configuration from {args.config_file}")

    try:
        with open(args.config_file) as file:
            conf = yaml.safe_load(file)

        general = General(**conf["general"])

        # Change directory to workdir
        logger.debug(f"Changing working directory to {general.workdir}")
        chdir(general.workdir)

        main(general, conf["model"])

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise
