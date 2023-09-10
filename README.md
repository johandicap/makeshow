# makeshow

Show definitions of Makefile targets in the terminal before running them.


### Usage

```bash
./makeshow.py
# Will show usage instructions and print a list of all targets found in the Makefile in the current folder.

./makeshow.py target1
# Will print the definition of Makefile target "target1".

./makeshow.py target1 target2 ... targetN
# Will print the definitions of Makefile targets 1 to N.
```

### Examples

##### Example 1: Show definitions of two targets

```bash
./makeshow.py isort_check isort_fix
```

Output:

```
---
isort_check:
	$(call header,"[make isort_check]")
	@isort --settings-path ./pyproject.toml --diff --color --check-only $(PYTHON_FILES_AND_FOLDERS)
---
isort_fix:
	$(call header,"[make isort_fix]")
	@isort --settings-path ./pyproject.toml $(PYTHON_FILES_AND_FOLDERS)
---
```

##### Example 2: Response for an invalid target

```bash
./makeshow.py unknown_target
```

Output:

```
---
Target 'unknown_target' not found in Makefile.
---
```



