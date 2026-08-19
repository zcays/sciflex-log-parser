# sciflex-log-parser

`sciflex-log-parser` reads a sciFLEX `.log` file and exposes its setup,
field layout, numbered fields, run checks, and chronological tasks as callable
Python objects. It has no runtime dependencies.

## Install

```bash
pip install git+https://github.com/zcays/sciflex-log-parser.git
```

## Use

```python
from sciflex_log_parser import LogFile

filename = "/path/to/example_Logfile.log"
log_data = LogFile.from_file(filename)

log_data.print_attributes()

print(log_data.Setup)
print(log_data.Setup("run_id"))
print(log_data.FieldSetup)
print(log_data.Fields)
print(log_data.RunChecks)
print(log_data.Tasks)
print(log_data.ExtraAttributes)

print(log_data.Field1)
print(log_data.Run1Check)

print(log_data())
print(log_data("tasks"))
print(log_data.Fields())
print(log_data.RunChecks())
print(log_data.Tasks())
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
