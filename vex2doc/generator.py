# Copyright (C) 2025 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

from sbom2doc.docbuilder.consolebuilder import ConsoleBuilder
from sbom2doc.docbuilder.htmlbuilder import HTMLBuilder
from sbom2doc.docbuilder.jsonbuilder import JSONBuilder
from sbom2doc.docbuilder.markdownbuilder import MarkdownBuilder
from sbom2doc.docbuilder.pdfbuilder import PDFBuilder
from sbom2doc.docbuilder.spreadsheetbuilder import SpreadsheetBuilder


def generate_document(format, vex_parser, filename, outfile):
    # Get constituent components of the VEX
    vex_type = vex_parser.get_type()
    metadata = vex_parser.get_metadata()
    product = vex_parser.get_product()
    vulnerabilities = vex_parser.get_vulnerabilities()

    # Select document builder based on format
    if format == "markdown":
        vex_document = MarkdownBuilder()
    elif format == "json":
        vex_document = JSONBuilder()
    elif format == "pdf":
        vex_document = PDFBuilder()
    elif format == "excel":
        vex_document = SpreadsheetBuilder()
    elif format == "html":
        vex_document = HTMLBuilder()
    else:
        vex_document = ConsoleBuilder()

    vex_document.heading(1, "VEX Summary")
    vex_document.createtable(["Item", "Details"], [20, 35])
    vex_document.addrow(["VEX File", filename])
    vex_document.addrow(["VEX Type", vex_type])
    for key, value in metadata.items():
        vex_document.addrow([key.capitalize(), str(value)])
    vex_document.showtable(widths=[5, 9])

    vex_document.heading(1, "Product Summary")
    # TODO Fix lib4vex
    if vex_type == "cyclonedx":
        product = product[0]
    vex_document.createtable(["Item", "Details"], [20, 35])
    for key, value in product.items():
        vex_document.addrow([key.capitalize(), str(value)])
    vex_document.showtable(widths=[5, 9])

    if len(vulnerabilities) > 0:
        vex_document.heading(1, "Vulnerabilities Summary")
        heading = False
        vuln_heading = []
        rows = []
        # Build up headings from all entries. Can't assume the first entry contains all of the attributes
        for vulnerability in vulnerabilities:
            vuln_dict = {} if not heading else {key: "" for key in vuln_heading}
            for key, value in vulnerability.items():
                if not heading or key not in vuln_heading:
                    vuln_heading.append(key)
                vuln_dict[key] = value
            if not heading:
                heading = True
            rows.append(list(vuln_dict.values()))

        vex_document.createtable([item.capitalize() for item in vuln_heading])
        for row in rows:
            vex_document.addrow(row)
        vex_document.showtable(widths=[15, 15, 15, 30])
    vex_document.publish(outfile)
