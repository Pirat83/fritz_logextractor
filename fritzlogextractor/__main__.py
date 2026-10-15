from __future__ import annotations

import argparse
import logging
import sys

from fritzlogextractor.config import ConfigError, get_config

from . import __version__

logger = logging.getLogger("fritzlogextractor")


def parse_cmdline(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract the event log of AVM Fritz! devices as structured log lines."
    )
    parser.add_argument(
        "--config", type=str, help="Path to config file (default: read from environment)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Override the log level from the configuration",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser.parse_args(argv)


def setup_logging(level: str) -> None:
    # Diagnostics go to stderr; stdout is reserved for the extracted events.
    logging.basicConfig(
        format="%(asctime)s %(levelname)8s %(name)s | %(message)s", stream=sys.stderr
    )
    logging.getLogger().setLevel(level)


def main(argv: list[str] | None = None) -> None:
    args = parse_cmdline(argv)
    setup_logging(args.log_level or "INFO")

    try:
        config = get_config(args.config)
    except ConfigError, ValueError, TypeError:
        logger.exception("Error while reading config:")
        sys.exit(1)

    logging.getLogger().setLevel(args.log_level or config.log_level)
    logger.info(
        "Configured %d device(s), polling every %ds, state in %s",
        len(config.devices),
        config.poll_interval,
        config.state_dir,
    )
    # The extraction loop is not implemented yet; see AGENTS.md for the design.
    logger.error("Log extraction is not implemented yet.")
    sys.exit(2)


if __name__ == "__main__":
    main()

# Copyright 2026 Patrick Dreker <patrick@dreker.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
