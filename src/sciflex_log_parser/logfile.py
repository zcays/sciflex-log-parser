class Setup:
    """Header/setup information from a sciFLEX log file."""

    ATTRIBUTE_NAMES = [
        "device_name",
        "device_number",
        "software_version",
        "software_time_date",
        "run_id",
        "probe_device",
        "target",
        "pattern_layout_file",
        "humidity",
        "run_name",
        "task_names",
    ]

    LABELS = {
        "device_name": "Device Name",
        "device_number": "Device Number",
        "software_version": "Software Version",
        "software_time_date": "Software Time / Date",
        "run_id": "Run ID",
        "probe_device": "Probe Device",
        "target": "Target",
        "pattern_layout_file": "Pattern Layout File",
        "humidity": "Humidity",
        "run_name": "Run Name",
        "task_names": "Task Names",
    }

    def __init__(self):
        self.device_name = None
        self.device_number = None
        self.software_version = None
        self.software_time_date = None
        self.run_id = None
        self.probe_device = None
        self.target = None
        self.pattern_layout_file = None
        self.humidity = None
        self.run_name = None
        self.task_names = []

    def __call__(self, attribute_name=None):
        """
        setup() returns every setup value as a dictionary.
        setup("run_id") returns one setup value.
        """
        if attribute_name is None:
            return self.to_dict()

        if attribute_name not in self.ATTRIBUTE_NAMES:
            raise KeyError("Unknown Setup attribute: " + str(attribute_name))

        return getattr(self, attribute_name)

    def to_dict(self):
        result = {}

        for name in self.ATTRIBUTE_NAMES:
            value = getattr(self, name)

            if isinstance(value, list):
                result[name] = value[:]
            else:
                result[name] = value

        return result

    def __str__(self):
        lines = ["SETUP", "=" * 72]

        for name in self.ATTRIBUTE_NAMES:
            value = getattr(self, name)

            if name == "task_names":
                lines.append("Task Names:")

                if value:
                    for number, task_name in enumerate(value, start=1):
                        lines.append("  " + str(number) + ". " + task_name)
                else:
                    lines.append("  Not found")
            else:
                label = self.LABELS[name]
                display_value = "Not found" if value is None else str(value)
                lines.append(label.ljust(24) + ": " + display_value)

        return "\n".join(lines)

    def print_attributes(self):
        print(self)


class FieldSetup:
    """The physical field-layout settings from the log file."""

    ATTRIBUTE_NAMES = [
        "nozzle",
        "x_fields",
        "y_fields",
        "start_point_left",
        "start_point_up",
        "x_field_gap",
        "y_field_gap",
        "pattern_size_x",
        "pattern_size_y",
        "dot_pitch_x",
        "dot_pitch_y",
    ]

    LABELS = {
        "nozzle": "Nozzle",
        "x_fields": "X Fields",
        "y_fields": "Y Fields",
        "start_point_left": "Start Point Left",
        "start_point_up": "Start Point Up",
        "x_field_gap": "X Field Gap",
        "y_field_gap": "Y Field Gap",
        "pattern_size_x": "Pattern Size X",
        "pattern_size_y": "Pattern Size Y",
        "dot_pitch_x": "Dot Pitch X",
        "dot_pitch_y": "Dot Pitch Y",
    }

    def __init__(self):
        for name in self.ATTRIBUTE_NAMES:
            setattr(self, name, None)

    def __call__(self, attribute_name=None):
        if attribute_name is None:
            return self.to_dict()

        if attribute_name not in self.ATTRIBUTE_NAMES:
            raise KeyError("Unknown FieldSetup attribute: " + str(attribute_name))

        return getattr(self, attribute_name)

    def to_dict(self):
        return {
            name: getattr(self, name)
            for name in self.ATTRIBUTE_NAMES
        }

    def __str__(self):
        lines = ["FIELD SETUP", "=" * 72]

        for name in self.ATTRIBUTE_NAMES:
            value = getattr(self, name)
            display_value = "Not found" if value is None else str(value)
            lines.append(self.LABELS[name].ljust(24) + ": " + display_value)

        return "\n".join(lines)

    def print_attributes(self):
        print(self)


class Field:
    """One numbered field and all of its populated row/column points."""

    def __init__(self, field_number, raw_rows=None):
        self.field_number = field_number
        self.raw_rows = [] if raw_rows is None else raw_rows

    def get_spots(self):
        spots = []

        for row_index, row in enumerate(self.raw_rows):
            cells = row if isinstance(row, list) else row.split("\t")

            for column_index, value in enumerate(cells):
                clean_value = value.strip()

                if clean_value and clean_value != "[0, 0, 0]":
                    spots.append({
                        "row": row_index,
                        "column": column_index,
                        "value": clean_value,
                    })

        return spots

    def __call__(self):
        return self.get_spots()

    def __str__(self):
        spots = self.get_spots()
        lines = [
            "FIELD " + str(self.field_number),
            "=" * 72,
            "Row".ljust(10) + "Column".ljust(10) + "Value",
            "-" * 32,
        ]

        if not spots:
            lines.append("No populated points found.")
        else:
            for spot in spots:
                lines.append(
                    str(spot["row"]).ljust(10)
                    + str(spot["column"]).ljust(10)
                    + str(spot["value"])
                )

        return "\n".join(lines)

    def print_attributes(self):
        print(self)


class RunCheck:
    """Settings and status checks associated with one log-file run."""

    ATTRIBUTE_NAMES = [
        "parallel_spotting",
        "ignore_nozzle_offset",
        "sort_by_field_position",
        "repeat_found",
        "repeat_parameter_1",
        "repeat_parameter_2",
        "start_time",
        "finish_time",
        "status",
        "not_spotted_probes_pre_autodrop",
    ]

    LABELS = {
        "parallel_spotting": "Parallel Spotting",
        "ignore_nozzle_offset": "Ignore Nozzle Offset",
        "sort_by_field_position": "Sort by Field Position",
        "repeat_found": "Repeat Found",
        "repeat_parameter_1": "Repeat Parameter 1",
        "repeat_parameter_2": "Repeat Parameter 2",
        "start_time": "Start Time",
        "finish_time": "Finish Time",
        "status": "Status",
        "not_spotted_probes_pre_autodrop": "Not Spotted Probes",
    }

    def __init__(self, run_number):
        self.run_number = run_number

        for name in self.ATTRIBUTE_NAMES:
            setattr(self, name, None)

    def __call__(self, attribute_name=None):
        if attribute_name is None:
            return self.to_dict()

        if attribute_name not in self.ATTRIBUTE_NAMES:
            raise KeyError("Unknown RunCheck attribute: " + str(attribute_name))

        return getattr(self, attribute_name)

    def to_dict(self):
        return {
            name: getattr(self, name)
            for name in self.ATTRIBUTE_NAMES
        }

    @staticmethod
    def _display_value(value):
        if value is True:
            return "True"

        if value is False:
            return "False"

        if value is None or value == "":
            return "None"

        return str(value)

    def __str__(self):
        lines = [
            "RUN " + str(self.run_number) + " CHECK",
            "=" * 72,
        ]

        for name in self.ATTRIBUTE_NAMES:
            lines.append(
                self.LABELS[name].ljust(30)
                + ": "
                + self._display_value(getattr(self, name))
            )

        return "\n".join(lines)

    def print_attributes(self):
        print(self)


class CallableSection:
    """A printable and callable view of one complete log section."""

    def __init__(self, name, data_function, format_function):
        self.name = name
        self._data_function = data_function
        self._format_function = format_function

    def __call__(self):
        return self._data_function()

    def __str__(self):
        return self._format_function()

    def print_attributes(self):
        print(self)


class LogFile:
    SETUP_ATTRIBUTES = Setup.ATTRIBUTE_NAMES
    FIELD_SETUP_ATTRIBUTES = FieldSetup.ATTRIBUTE_NAMES

    def __init__(self):
        self.setup = Setup()
        self.field_setup = FieldSetup()
        self.Setup = self.setup
        self.FieldSetup = self.field_setup
        self.fields = {}
        self.run_checks = {}
        self.configured_tasks = []
        self.executed_tasks = []
        self._task_count_by_run = {}
        self._active_run_check_number = None
        self.not_spotted_probes_pre_autodrop = None

        self.task_runs = {}
        self._current_task_run_id = 0

        self.field_points = {}

        self.parallel_spotting = None
        self.ignore_nozzle_offset = None
        self.sort_by_field_position = None

        self.repeat_found = False
        self.repeat_parameter_1 = None
        self.repeat_parameter_2 = None

        self.start_time = None
        self.finish_time = None
        self.run_status = None
        self.recorded_humidity = []
        self.recorded_temperature = []
        self.extra_attributes = {}

        self.Fields = CallableSection(
            "Fields",
            self.get_all_fields,
            self.format_all_fields,
        )
        self.RunChecks = CallableSection(
            "RunChecks",
            self.get_all_run_checks,
            self.format_all_run_checks,
        )
        self.Tasks = CallableSection(
            "Tasks",
            self.get_all_tasks,
            self.format_tasks,
        )
        self.ExtraAttributes = CallableSection(
            "ExtraAttributes",
            self.get_extra_attributes,
            self.format_extra_attributes,
        )

    def __getattr__(self, attribute_name):
        """Keep old access such as log_data.run_id working."""
        if attribute_name in self.SETUP_ATTRIBUTES:
            return getattr(self.setup, attribute_name)

        if attribute_name in self.FIELD_SETUP_ATTRIBUTES:
            return getattr(self.field_setup, attribute_name)

        if attribute_name == "FieldSetup":
            return self.field_setup

        if attribute_name.startswith("Field"):
            field_number = attribute_name[5:]

            if field_number.isdigit():
                return self.get_field(int(field_number))

        if attribute_name.startswith("Run") and attribute_name.endswith("Check"):
            run_number = attribute_name[3:-5]

            if run_number.isdigit():
                return self.get_run_check(int(run_number))

        raise AttributeError(attribute_name)

    def __call__(self, object_name=None):
        """log_data() returns its main parsed objects."""
        objects = {
            "setup": self.Setup,
            "field_setup": self.FieldSetup,
            "fields": self.Fields,
            "run_checks": self.RunChecks,
            "tasks": self.Tasks,
            "extra_attributes": self.ExtraAttributes,
            "configured_tasks": self.configured_tasks,
            "executed_tasks": self.executed_tasks,
            "run": self.get_run_summary(),
        }

        if object_name is None:
            return objects

        object_name = str(object_name).lower()

        if object_name not in objects:
            raise KeyError("Unknown LogFile object: " + object_name)

        return objects[object_name]

    @classmethod
    def from_file(cls, filename):
        if not filename.lower().endswith(".log"):
            raise ValueError("File must be a .log file")

        result = cls()

        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            lines = file.readlines()

        if not lines:
            return result

        result._read_device_line(lines[0])

        if len(lines) > 1:
            result._read_software_line(lines[1])

        current_field = None
        current_configured_task = None
        configured_step_counts = {}
        in_tasks = False
        in_field_points = False
        field_section = None
        in_event_log = False

        for original_line in lines[2:]:
            line = original_line.strip()

            if line.startswith("§"):
                continue

            if not line:
                if in_field_points and current_field is not None:
                    result.field_points[current_field].append(
                        original_line.rstrip("\n")
                    )
                elif in_tasks or in_event_log:
                    result.task_runs[result._current_task_run_id].append(
                        original_line.rstrip("\n")
                    )
                continue

            if line.startswith("Run ID:"):
                result.setup.run_id = result._after_colon(line)

            elif line.startswith("Probe:"):
                result.setup.probe_device = result._after_colon(line)

            elif line.startswith("Target:"):
                result.setup.target = result._after_colon(line)

            elif line.startswith("Pattern File"):
                result.setup.pattern_layout_file = result._after_colon(line)

            elif line.startswith("Humidity:"):
                result.setup.humidity = result._after_colon(line)

            elif line.startswith("Run Name:"):
                result.setup.run_name = result._after_colon(line)

            elif line.startswith("Task Names:"):
                task_text = result._after_colon(line)
                result.setup.task_names = [
                    name.strip()
                    for name in task_text.split("/")
                    if name.strip()
                ]

            elif line == "Tasks:":
                in_tasks = True
                current_configured_task = None
                result._start_task_run()

            elif line.startswith("Nozzle(s):"):
                in_tasks = False
                result.field_setup.nozzle = result._to_number(
                    result._after_colon(line)
                )

            elif in_tasks:
                result.task_runs[result._current_task_run_id].append(
                    original_line.rstrip("\n")
                )

                if line.endswith("=") and "\t" not in line:
                    current_configured_task = line[:-1].strip()

                    if current_configured_task not in configured_step_counts:
                        configured_step_counts[current_configured_task] = 0
                elif current_configured_task is not None:
                    step_number = configured_step_counts[current_configured_task]
                    result._read_configured_task(
                        current_configured_task,
                        step_number,
                        original_line.rstrip("\n"),
                    )
                    configured_step_counts[current_configured_task] = (
                        step_number + 1
                    )

                result._read_repeat_line(line)

            elif line == "Field(s):":
                field_section = "fields"

            elif line == "Start Point":
                field_section = "start_point"

            elif line == "Pattern Size:":
                field_section = "pattern_size"

            elif line == "Dot Pitch:":
                field_section = "dot_pitch"

            elif line.startswith("Left:"):
                result.field_setup.start_point_left = result._to_number(
                    result._after_colon(line)
                )

            elif line.startswith("Up:"):
                result.field_setup.start_point_up = result._to_number(
                    result._after_colon(line)
                )

            elif line.startswith("X Field Gap:"):
                result.field_setup.x_field_gap = result._to_number(
                    result._after_colon(line).rstrip("/")
                )

            elif line.startswith("Y Field Gap:"):
                result.field_setup.y_field_gap = result._to_number(
                    result._after_colon(line).rstrip("/")
                )

            elif line.startswith("X ="):
                value = result._to_number(line.split("=", 1)[1].strip())

                if field_section == "fields":
                    result.field_setup.x_fields = value
                elif field_section == "pattern_size":
                    result.field_setup.pattern_size_x = value
                elif field_section == "dot_pitch":
                    result.field_setup.dot_pitch_x = value

            elif line.startswith("Y ="):
                value = result._to_number(line.split("=", 1)[1].strip())

                if field_section == "fields":
                    result.field_setup.y_fields = value
                elif field_section == "pattern_size":
                    result.field_setup.pattern_size_y = value
                elif field_section == "dot_pitch":
                    result.field_setup.dot_pitch_y = value

            elif line.startswith("Field ") and line[6:].isdigit():
                current_field = int(line[6:])
                result.field_points[current_field] = []
                result.fields[current_field] = Field(
                    current_field,
                    result.field_points[current_field],
                )
                in_field_points = True
                field_section = None

            elif line == "[0, 0, 0]":
                continue

            elif line.startswith("Drops/Field"):
                in_field_points = False
                current_field = None

            elif in_field_points and current_field is not None:
                result.field_points[current_field].append(
                    original_line.rstrip("\n")
                )

            elif line.startswith("Parallel Spotting:"):
                result.parallel_spotting = result._on_or_off(
                    result._after_colon(line)
                )

            elif line.startswith("Ignore Nozzle Offset:"):
                result.ignore_nozzle_offset = result._on_or_off(
                    result._after_colon(line)
                )

            elif line.startswith("Sort by Field Position:"):
                result.sort_by_field_position = result._on_or_off(
                    result._after_colon(line)
                )

            elif line.startswith("Start Time:"):
                result.start_time = result._after_colon(line)
                result.run_status = "Started"
                result._start_run_check()
                in_event_log = True
                result._start_task_run()

            elif line.startswith("Run has finished:"):
                result.finish_time = result._after_colon(line)
                result.run_status = "Finished"
                result._finish_active_run_check("Finished", result.finish_time)
                in_event_log = False

            elif line.startswith("Run has been aborted!"):
                result.run_status = "Aborted"
                result._finish_active_run_check("Aborted", None)
                in_event_log = False

            elif "Not spotted probes (pre-autodrop)" in line:
                marker = "Not spotted probes (pre-autodrop)"
                value = line.split(marker, 1)[1].strip()

                if value.startswith(":") or value.startswith("="):
                    value = value[1:].strip()

                result.not_spotted_probes_pre_autodrop = value
                result._update_active_not_spotted(value)

            elif in_event_log:
                if not line.startswith("Plate\tPlate Pos"):
                    result.task_runs[result._current_task_run_id].append(
                        original_line.rstrip("\n")
                    )
                    result._read_executed_task(original_line.rstrip("\n"))

                if "Humidity=" in line:
                    result._read_recorded_environment(line)

            elif "Humidity=" in line:
                result._read_recorded_environment(line)

            elif ":" in line:
                label, value = line.split(":", 1)
                result._store_extra(label.strip(), value.strip())

        return result

    def _start_task_run(self):
        self._current_task_run_id += 1
        self.task_runs[self._current_task_run_id] = []

    def _start_run_check(self):
        run_number = len(self.run_checks) + 1
        run_check = RunCheck(run_number)
        run_check.parallel_spotting = self.parallel_spotting
        run_check.ignore_nozzle_offset = self.ignore_nozzle_offset
        run_check.sort_by_field_position = self.sort_by_field_position
        run_check.repeat_found = self.repeat_found
        run_check.repeat_parameter_1 = self.repeat_parameter_1
        run_check.repeat_parameter_2 = self.repeat_parameter_2
        run_check.start_time = self.start_time
        run_check.status = self.run_status
        run_check.not_spotted_probes_pre_autodrop = (
            self.not_spotted_probes_pre_autodrop
        )
        self.run_checks[run_number] = run_check
        self._active_run_check_number = run_number

    def _finish_active_run_check(self, status, finish_time):
        if self._active_run_check_number is None:
            return

        run_check = self.run_checks[self._active_run_check_number]
        run_check.status = status
        run_check.finish_time = finish_time

    def _update_active_not_spotted(self, value):
        if self._active_run_check_number is not None:
            self.run_checks[
                self._active_run_check_number
            ].not_spotted_probes_pre_autodrop = value

    def _read_device_line(self, line):
        columns = [column.strip() for column in line.split("\t")]

        if columns:
            self.setup.device_name = columns[0] or None

        if len(columns) > 1:
            self.setup.device_number = columns[1] or None

    def _read_software_line(self, line):
        columns = [column.strip() for column in line.split("\t")]

        if columns and columns[0].startswith("Software Version:"):
            self.setup.software_version = self._after_colon(columns[0])

        if len(columns) > 1:
            self.setup.software_time_date = columns[1] or None

    def _read_repeat_line(self, line):
        columns = [value.strip() for value in line.split("\t") if value.strip()]

        if "Begin Loop" in columns:
            self.repeat_found = True
            self.repeat_parameter_1 = self._to_number(columns[-1])

        if "End Loop" in columns:
            self.repeat_found = True
            self.repeat_parameter_2 = self._to_number(columns[-1])

    def _read_recorded_environment(self, line):
        humidity_text = line.split("Humidity=", 1)[1]
        humidity_part = humidity_text.split("Temperature=", 1)[0]
        humidity_value = humidity_part.strip().split()[0]
        self.recorded_humidity.append(self._to_number(humidity_value))

        if "Temperature=" in line:
            temperature_text = line.split("Temperature=", 1)[1].strip()
            temperature_value = temperature_text.split()[0]
            self.recorded_temperature.append(
                self._to_number(temperature_value)
            )

    def _read_configured_task(self, task_name, step_number, raw_line):
        values = [value.strip() for value in raw_line.split("\t")]

        while values and not values[-1]:
            values.pop()

        if not values:
            return

        labels = [
            "plate",
            "plate_pos",
            "nozzle",
            "well",
            "target",
            "level",
            "field",
            "drops",
            "x_pos",
            "y_pos",
        ]

        configured_task = {
            "configured_task": task_name,
            "step": step_number,
            "raw_line": raw_line.rstrip(),
            "fits_table": len(values) >= len(labels),
        }

        for index, label in enumerate(labels):
            configured_task[label] = (
                values[index] if index < len(values) else ""
            )

        configured_task["extra"] = values[len(labels):]

        self.configured_tasks.append(configured_task)

    def _read_executed_task(self, raw_line):
        columns = raw_line.split("\t")

        if len(columns) < 2:
            return

        timestamp = columns[0].strip()

        if not self._looks_like_timestamp(timestamp):
            return

        values = [value.strip() for value in columns[1:]]

        while values and not values[-1]:
            values.pop()

        labels = [
            "plate",
            "plate_pos",
            "nozzle",
            "well",
            "target",
            "level",
            "field",
            "drops",
            "x_pos",
            "y_pos",
        ]

        task = {
            "task": len(self.executed_tasks),
            "timestamp": timestamp,
            "raw_line": raw_line.rstrip(),
            "fits_table": len(values) >= len(labels),
        }

        run_number = self._active_run_check_number

        if run_number is None:
            run_number = 0

        task_number_in_run = self._task_count_by_run.get(run_number, 0)
        self._task_count_by_run[run_number] = task_number_in_run + 1
        task["run"] = run_number
        task["task_in_run"] = task_number_in_run

        for index, label in enumerate(labels):
            task[label] = values[index] if index < len(values) else ""

        task["extra"] = values[len(labels):]
        self.executed_tasks.append(task)

    @staticmethod
    def _looks_like_timestamp(value):
        return (
            bool(value)
            and value[0].isdigit()
            and "." in value
            and "-" in value
            and ":" in value
        )

    def _store_extra(self, label, value):
        converted_value = self._to_number(value)

        if label not in self.extra_attributes:
            self.extra_attributes[label] = converted_value
        else:
            existing_value = self.extra_attributes[label]

            if not isinstance(existing_value, list):
                existing_value = [existing_value]
                self.extra_attributes[label] = existing_value

            existing_value.append(converted_value)

    @staticmethod
    def _after_colon(line):
        return line.split(":", 1)[1].strip()

    @staticmethod
    def _to_number(value):
        value = value.strip()

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            return value

    @staticmethod
    def _on_or_off(value):
        value = value.strip().lower()

        if value == "on":
            return True

        if value == "off":
            return False

        return value

    @staticmethod
    def _display_switch(value):
        if value is True:
            return "On"

        if value is False:
            return "Off"

        return "Not found" if value is None else str(value)

    def get_field_spots(self, field_id=1):
        if field_id not in self.fields:
            return []

        return self.fields[field_id].get_spots()

    def get_field(self, field_number):
        if field_number not in self.fields:
            raise KeyError("Field " + str(field_number) + " was not found")

        return self.fields[field_number]

    def get_run_check(self, run_number):
        if run_number not in self.run_checks:
            raise KeyError("Run " + str(run_number) + " Check was not found")

        return self.run_checks[run_number]

    def get_all_fields(self):
        return [
            self.fields[field_number]
            for field_number in sorted(self.fields)
        ]

    def get_all_run_checks(self):
        return [
            self.run_checks[run_number]
            for run_number in sorted(self.run_checks)
        ]

    def get_executed_tasks(self, run_number=None):
        if run_number is None:
            return self.executed_tasks[:]

        return [
            task
            for task in self.executed_tasks
            if task["run"] == run_number
        ]

    def get_configured_tasks(self, task_name=None):
        if task_name is None:
            return self.configured_tasks[:]

        return [
            task
            for task in self.configured_tasks
            if task["configured_task"] == task_name
        ]

    def get_all_tasks(self):
        tasks = []

        for configured_task in self.configured_tasks:
            task = {
                "source": "Configured",
                "task_name": configured_task["configured_task"],
                "step": configured_task["step"],
                "timestamp": "Before run",
                "fits_table": configured_task["fits_table"],
                "raw_line": (
                    "[Before run] "
                    + configured_task["configured_task"]
                    + " [step "
                    + str(configured_task["step"])
                    + "]: "
                    + configured_task["raw_line"]
                ),
            }

            for key in [
                "plate",
                "plate_pos",
                "nozzle",
                "well",
                "target",
                "level",
                "field",
                "drops",
                "x_pos",
                "y_pos",
                "extra",
            ]:
                task[key] = configured_task.get(key, "")

            tasks.append(task)

        for executed_index, executed_task in enumerate(self.executed_tasks):
            task = {
                "source": "Run " + str(executed_task["run"]),
                "task_name": executed_task["task_in_run"],
                "step": "",
                "timestamp": executed_task["timestamp"],
                "timestamp_section_start": executed_index == 0,
                "fits_table": executed_task["fits_table"],
                "raw_line": executed_task["raw_line"],
            }

            for key in [
                "plate",
                "plate_pos",
                "nozzle",
                "well",
                "target",
                "level",
                "field",
                "drops",
                "x_pos",
                "y_pos",
                "extra",
            ]:
                task[key] = executed_task.get(key, "")

            tasks.append(task)

        return tasks

    def print_all_fields(self):
        print(self.format_all_fields())

    def format_all_fields(self):
        fields = self.get_all_fields()

        if not fields:
            return "FIELDS\n" + "=" * 72 + "\nNo fields found."

        return "\n\n".join(str(field) for field in fields)

    def print_all_run_checks(self):
        print(self.format_all_run_checks())

    def format_all_run_checks(self):
        run_checks = self.get_all_run_checks()

        if not run_checks:
            return "RUN CHECKS\n" + "=" * 72 + "\nNo runs found."

        return "\n\n".join(
            str(run_check)
            for run_check in run_checks
        )

    def get_extra_attributes(self):
        return self.extra_attributes.copy()

    def format_extra_attributes(self):
        lines = ["EXTRA ATTRIBUTES", "=" * 72]

        if not self.extra_attributes:
            lines.append("No extra attributes found.")
        else:
            for name, value in self.extra_attributes.items():
                lines.append(str(name).ljust(24) + ": " + str(value))

        return "\n".join(lines)

    def get_layout(self):
        return {
            "nozzle": self.nozzle,
            "x_fields": self.x_fields,
            "y_fields": self.y_fields,
            "start_point_left": self.start_point_left,
            "start_point_up": self.start_point_up,
            "x_field_gap": self.x_field_gap,
            "y_field_gap": self.y_field_gap,
            "pattern_size_x": self.pattern_size_x,
            "pattern_size_y": self.pattern_size_y,
            "dot_pitch_x": self.dot_pitch_x,
            "dot_pitch_y": self.dot_pitch_y,
            "parallel_spotting": self.parallel_spotting,
            "ignore_nozzle_offset": self.ignore_nozzle_offset,
            "sort_by_field_position": self.sort_by_field_position,
        }

    def get_run_summary(self):
        return {
            "status": self.run_status,
            "start_time": self.start_time,
            "finish_time": self.finish_time,
            "repeat_found": self.repeat_found,
            "repeat_parameter_1": self.repeat_parameter_1,
            "repeat_parameter_2": self.repeat_parameter_2,
            "recorded_humidity": self.recorded_humidity[:],
            "recorded_temperature": self.recorded_temperature[:],
        }

    def format_tasks(self):
        columns = [
            ("source", "Source"),
            ("task_name", "Task"),
            ("step", "Step"),
            ("timestamp", "Timestamp"),
            ("plate", "Plate"),
            ("plate_pos", "Plate Pos"),
            ("nozzle", "Nozzle"),
            ("well", "Well"),
            ("target", "Target"),
            ("level", "Level"),
            ("field", "Field"),
            ("drops", "Drops"),
            ("x_pos", "X Pos"),
            ("y_pos", "Y Pos"),
            ("extra", "Extra"),
        ]

        return self._format_tasks_with_fallback(
            "TASKS",
            self.get_all_tasks(),
            columns,
            False,
        )

    def print_tasks(self):
        print(self.format_tasks())

    def format_configured_tasks(self, task_name=None):
        tasks = self.get_configured_tasks(task_name)
        columns = [
            ("configured_task", "Configured Task"),
            ("step", "Step"),
            ("plate", "Plate"),
            ("plate_pos", "Plate Pos"),
            ("nozzle", "Nozzle"),
            ("well", "Well"),
            ("target", "Target"),
            ("level", "Level"),
            ("field", "Field"),
            ("drops", "Drops"),
            ("x_pos", "X Pos"),
            ("y_pos", "Y Pos"),
            ("extra", "Extra"),
        ]

        return self._format_tasks_with_fallback(
            "CONFIGURED TASKS",
            tasks,
            columns,
            True,
        )

    def print_configured_tasks(self, task_name=None):
        print(self.format_configured_tasks(task_name))

    def format_executed_tasks(self, run_number=None):
        columns = [
            ("run", "Run"),
            ("task_in_run", "Task"),
            ("timestamp", "Timestamp"),
            ("plate", "Plate"),
            ("plate_pos", "Plate Pos"),
            ("nozzle", "Nozzle"),
            ("well", "Well"),
            ("target", "Target"),
            ("level", "Level"),
            ("field", "Field"),
            ("drops", "Drops"),
            ("x_pos", "X Pos"),
            ("y_pos", "Y Pos"),
            ("extra", "Extra"),
        ]

        tasks = self.get_executed_tasks(run_number)

        return self._format_tasks_with_fallback(
            "EXECUTED TASKS",
            tasks,
            columns,
            False,
        )

    @staticmethod
    def _format_tasks_with_fallback(
        title,
        tasks,
        columns,
        configured,
    ):
        if not tasks:
            return title + "\n" + "=" * 72 + "\nNo tasks found."

        formatted_rows = {}

        for position, task in enumerate(tasks):
            if not task.get("fits_table", False):
                continue

            row = {}

            for key, label in columns:
                value = task.get(key, "")

                if isinstance(value, list):
                    value = ", ".join(str(item) for item in value)

                row[key] = str(value)

            formatted_rows[position] = row

        widths = {}

        for key, label in columns:
            width = len(label)

            for row in formatted_rows.values():
                width = max(width, len(row[key]))

            widths[key] = width

        header = " | ".join(
            label.ljust(widths[key])
            for key, label in columns
        )
        separator = "-+-".join(
            "-" * widths[key]
            for key, label in columns
        )
        lines = [title, "=" * len(header), header, separator]

        for position, task in enumerate(tasks):
            if task.get("timestamp_section_start", False):
                lines.extend([
                    "",
                    "TIMESTAMPED RUN TASKS",
                    "=" * len(header),
                    header,
                    separator,
                    "",
                ])

            if position in formatted_rows:
                row = formatted_rows[position]
                lines.append(
                    " | ".join(
                        row[key].ljust(widths[key])
                        for key, label in columns
                    )
                )
                lines.append("")
            else:
                raw_line = task.get("raw_line", "")

                if configured:
                    raw_line = (
                        str(task.get("configured_task", "Task"))
                        + " [step "
                        + str(task.get("step", ""))
                        + "]: "
                        + raw_line
                    )

                lines.append(raw_line)
                lines.append("")

        return "\n".join(lines).rstrip()

    def print_executed_tasks(self, run_number=None):
        print(self.format_executed_tasks(run_number))

    def print_attributes(
        self,
        include_field_spots=True,
        include_tasks=True,
        include_raw_tasks=False,
    ):
        sections = [str(self.Setup), str(self.FieldSetup)]

        if include_field_spots:
            sections.append(str(self.Fields))

        sections.append(str(self.RunChecks))

        if include_tasks:
            sections.append(str(self.Tasks))

        if self.extra_attributes:
            sections.append(str(self.ExtraAttributes))

        if include_raw_tasks:
            task_lines = ["RAW TASK RUNS", "=" * 72]

            for run_id, lines in self.task_runs.items():
                task_lines.append("Task Run " + str(run_id))
                task_lines.extend(lines)
                task_lines.append("")

            sections.append("\n".join(task_lines).rstrip())

        print("\n\n".join(sections))

