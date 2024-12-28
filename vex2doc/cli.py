# Copyright (C) 2024Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import argparse
import sys
import textwrap
from collections import ChainMap

from lib4vex.parser import VEXParser

import vex2doc.generator as generator
from vex2doc.version import VERSION

# CLI processing


def main(argv=None):
    argv = argv or sys.argv
    app_name = "vex2doc"
    parser = argparse.ArgumentParser(
        prog=app_name,
        description=textwrap.dedent(
            """
            VEX2doc generates documentation for a VEX artefact.
            """
        ),
    )
    input_group = parser.add_argument_group("Input")
    input_group.add_argument(
        "-i",
        "--input-file",
        action="store",
        default="",
        help="Name of VEX file",
    )

    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="add debug information",
    )

    # Add format option
    output_group.add_argument(
        "-f",
        "--format",
        action="store",
        help="Output format (default: output to console)",
        choices=["console", "excel", "html", "json", "markdown", "pdf"],
        default="console",
    )

    output_group.add_argument(
        "-o",
        "--output-file",
        action="store",
        default="",
        help="output filename (default: output to stdout)",
    )

    parser.add_argument("-V", "--version", action="version", version=VERSION)

    defaults = {
        "input_file": "",
        "output_file": "",
        "debug": False,
        "format": "console",
    }

    raw_args = parser.parse_args(argv[1:])
    args = {key: value for key, value in vars(raw_args).items() if value}
    args = ChainMap(args, defaults)

    # Validate CLI parameters

    input_file = args["input_file"]

    if input_file == "":
        print("[ERROR] VEX name must be specified.")
        return -1

    if args["format"] != "console" and args["output_file"] == "":
        print("[ERROR] Output filename must be specified.")
        return -1

    if args["debug"]:
        print("Input file", args["input_file"])
        print("Output file", args["output_file"])

    vex_parser = VEXParser()
    # Load SBOM - will autodetect SBOM type
    try:
        vex_parser.parse(input_file)

        generator.generate_document(
            args["format"],
            vex_parser,
            input_file,
            args["output_file"],
        )

    except FileNotFoundError:
        print(f"{input_file} not found")

    return 0


if __name__ == "__main__":
    sys.exit(main())
