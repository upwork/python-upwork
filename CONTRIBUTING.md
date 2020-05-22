Install project automation tool [`nox`](https://nox.thea.codes/en/stable/):

```
python -m pip install --user nox
```

### Unit Tests

```
nox -s tests
```

### Lint

```
nox -s lint
```

### Publish to PyPI

```
nox -s publish
```