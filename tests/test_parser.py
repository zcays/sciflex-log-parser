import tempfile
import unittest
from pathlib import Path

from sciflex_log_parser import LogFile


class LogFileTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_rejects_non_log_extension(self):
        filename = self.directory / "example.txt"
        filename.write_text("not a log", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "File must be a .log file"):
            LogFile.from_file(str(filename))

    def test_reads_setup_and_returns_callable_sections(self):
        filename = self.directory / "example.log"
        filename.write_text(
            "sciFLEX_S3Pulse\t87782300166\n"
            "Software Version: 3.19.12.8.sciPULSE\t4:19 PM - 8/14/2024\n"
            "\n"
            "Run ID: example_run\n"
            "Probe: 384_Costar_3656\n"
            "Target: example_target\n",
            encoding="utf-8",
        )

        log_data = LogFile.from_file(str(filename))

        self.assertEqual(log_data.Setup("device_name"), "sciFLEX_S3Pulse")
        self.assertEqual(log_data.Setup("device_number"), "87782300166")
        self.assertEqual(log_data.Setup("run_id"), "example_run")
        self.assertEqual(log_data.Setup("probe_device"), "384_Costar_3656")
        self.assertEqual(log_data.Setup("target"), "example_target")
        self.assertIs(log_data("setup"), log_data.Setup)
        self.assertIs(log_data("tasks"), log_data.Tasks)

    def test_empty_file_has_scalable_sections(self):
        filename = self.directory / "example.log"
        filename.write_text(
            "sciFLEX_S3Pulse\t87782300166\n"
            "Software Version: 3.19.12.8.sciPULSE\t4:19 PM - 8/14/2024\n"
            "\n",
            encoding="utf-8",
        )

        log_data = LogFile.from_file(str(filename))

        self.assertEqual(log_data.Fields(), [])
        self.assertEqual(log_data.RunChecks(), [])


if __name__ == "__main__":
    unittest.main()
