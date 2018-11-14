## Software

All code for this work is in Python with all versions specified in
[`environment.yml`](./environment.yml).

### Create a conda environment with all required libraries

```
$ conda env create -f environment.yml
$ source activate testing-zd
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

The raw data containing the specific interactions of all player interactions is
achieved at https://doi.org/10.5281/zenodo.1297075

**Having created and activated the conda environment**

### Download and unpack the archived data

```
$ invoke data
```

### Pre process the raw data

```
$ invoke process
```

### Create all assets

```
$ invoke assets --processdata
```

### Build the main pdf

```
$ invoke main
```

### Do all of the above

Note that you can simply run:

```
$ invoke data
$ invoke build
```

For more information about what you can do:

```
$ invoke -l
```
