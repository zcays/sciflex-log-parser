# sciflex-log-parser

`sciflex-log-parser` reads a sciFLEX `.log` file and exposes its setup,
field layout, numbered fields, run checks, and chronological tasks as callable
Python objects. It has no runtime dependencies.

## Install

```bash
python3 -m pip install git+https://github.com/zcays/sciflex-log-parser.git
```

## Use

```python
from sciflex_log_parser import LogFile

filename = "/path/to/example_Logfile.log"
log_data = LogFile.from_file(filename)

# Print the full report
log_data.print_attributes()
```

### Inspect specific sections

You can print or inspect individual sections using the built-in objects:

```python
# Formatted individual sections
print(log_data.Setup)
print(log_data.FieldSetup)
print(log_data.Fields)
print(log_data.RunChecks)
print(log_data.Tasks)
print(log_data.ExtraAttributes)

# Numbered fields and run checks
print(log_data.Field1)
print(log_data.Run1Check)

# Access raw Python data
run_id = log_data.Setup("run_id")
spots = log_data.Field1()      # List of populated spot coordinates
tasks = log_data.Tasks()       # List of task dictionaries
```

The available main object names are:

- `Setup`
- `FieldSetup`
- `Field1`, `Field2`, ...
- `Run1Check`, `Run2Check`, ...
- `Fields`
- `RunChecks`
- `Tasks`
- `ExtraAttributes`
