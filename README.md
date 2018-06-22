## Software

All code for this work is in Python with all versions specified in
[`environment.yml`](./environment.yml).

### Create a conda environment with all required libraries

```
$ conda env create -f environment.yml
$ conda activate testing-zd
```

To install specific software for this work:

```
$ python setup.py develop
```

To run tests:

```
$ pytest
```

## Reproducing the results

The raw data containing the specific interactions of all player interactions can
be found here `TODO: Archive data`. Place the un archived `data` in the root
directory of this repository.

```
|--- assets
|--- src
|--- tests
|--- data
```

TODO Add a `wget` and `tar` command to `tasks.py` file

Having created and activated the conda environment

### Pre process the raw data

```
$ invoke process
```

### Create all assets

```
$ invoke assets processdata
```

### Build the pdf

```
$ invoke pdf
```

### Do all of the above

Note that you can simply run:

```
$ invoke build processdata
```

For more information about what you can do:

```
$ invoke -l
```
