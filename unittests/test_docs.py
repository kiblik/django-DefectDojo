from dataclasses import dataclass
from pydoc import locate

import tree_sitter_markdown
from django.test import TestCase
from tree_sitter import Language, Parser

from dojo.settings.settings import env

from .dojo_test_case import get_unit_tests_path

basedir = get_unit_tests_path().parent


@dataclass
class Setting:
    name: str
    datatype: type
    default: str = ""


class TestDocs(TestCase):

    def test_system_env_var(self):

        # Process settings.dist.py file
        self.setting_file = {}
        for name, setting in env.scheme.items():
            self.setting_file[name] = Setting(
                name,
                setting[0],
                str(setting[1]),
            )

        # Process documentation file
        self.doc_file = {}
        # doc_file = basedir / "docs" / "content" / "en" / "open_source" / "installation" / "configuration" / "envvars.md"

        content = """
        ---
        title: "Configuration (Open Source) - ENV VARS"
        description: "DefectDojo is highly configurable."
        draft: false
        weight: 3
        ---

        ## DD_XXX

        | Name    | Value       |
        | ------- | ----------- |
        | type    | string      |
        | default | `"default"` |

        Description 1

        ## DD_YYY

        | Name    | Value       |
        | ------- | ----------- |
        | type    | int      |
        | default | `10` |

        Description 2

        """

        parser = Parser()
        parser.language = Language(tree_sitter_markdown.language())
        tree = parser.parse(bytes(content, "utf8"))
        for section in tree.root_node.children:
            if section.children[0].type != "atx_heading" or section.children[0].children[0].type != "atx_h2_marker":  # it was are not talking about about H2
                continue

            header = section.children[0]
            header_text = header.children[1].text.decode()

            with self.subTest(header=header_text):
                self.assertTrue(header_text.startswith("DD_"), "All H2 headers have to start with `DD_`")

                table = section.children[1]
                self.assertEqual(table.type, "pipe_table", "First part of EnvVar description has to be table")
                self.assertEqual(table.children[0].children[1].text.decode().strip(), "Name", 'First column of EnvVar table has to be "Name"')
                self.assertEqual(table.children[0].children[3].text.decode().strip(), "Value", 'Second column of EnvVar table has to be "Value"')
                self.assertEqual(table.children[1].children[1].type, "pipe_table_delimiter_cell", "First row after table header has to be delimiter")
                self.assertEqual(table.children[2].children[1].text.decode().strip(), "type", 'First row of EnvVar table has to be "type"')
                self.assertEqual(table.children[3].children[1].text.decode().strip(), "default", 'First row of EnvVar table has to be "type"')

                setting = Setting(
                        header_text,
                        locate(table.children[2].children[3].text.decode().strip()),
                        table.children[3].children[3].text.decode().strip(),
                )

                description = section.children[2]
                self.assertEqual(description.type, "paragraph", "Second part of EnvVar description has to be table")
