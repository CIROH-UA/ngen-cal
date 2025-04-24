"""
This is main script to execute validation control run using the default model
parameter set and validation best run using the best calibrated parameter set.
@author: Xia Feng
"""

import argparse
import logging
from os import chdir
from pathlib import Path

import yaml
from logger_config import get_logger, setup_logging
from ngen.cal.agent import Agent
from ngen.cal.configuration import General
from ngen.cal.validation_run import run_valid_ctrl_best


def main(general: General, model_conf):
    """Main validation function"""
    logger = get_logger(__name__)
    # Seed the random number generators if requested
    if general.random_seed is not None:
        import random

        random.seed(general.random_seed)
        import numpy as np

        np.random.seed(general.random_seed)
        logger.debug(f"Set random seed to {general.random_seed}")

    logger.info("Starting Validation Run")

    # Initialize agent
    logger.debug("Initializing validation agent")
    agent = Agent(model_conf, general.valid_path, general, general.log, general.restart)

    # Execute validation control and best simulation
    logger.info("Executing validation control and best simulation runs")
    run_valid_ctrl_best(agent)

    logger.info("Validation process completed")


if __name__ == "__main__":
    # Create command line parser
    parser = argparse.ArgumentParser(description="Run Validation in NGEN architecture.")
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
