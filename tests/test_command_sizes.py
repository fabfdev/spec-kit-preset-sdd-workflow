import unittest
from pathlib import Path

# invariant: every command is loaded whole on each invocation; this caps its token cost.
LIMIT_BYTES = 3072
COMMANDS = Path(__file__).resolve().parents[1] / "commands"


class CommandSizeTest(unittest.TestCase):
    def test_commands_stay_small(self):
        files = sorted(COMMANDS.glob("*.md"))
        self.assertTrue(files)
        too_big = {f.name: f.stat().st_size for f in files if f.stat().st_size > LIMIT_BYTES}
        self.assertEqual(too_big, {}, "commands over {} bytes".format(LIMIT_BYTES))


if __name__ == "__main__":
    unittest.main()
