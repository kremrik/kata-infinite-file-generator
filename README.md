# Infinite Data Generator
Sample project based off of a real problem somewhere real

### Example

##### example.csv
```csv INJECT_CODE(examples/example.csv)
foo,bar,baz
1,2,3
4,5,6
7,8,9
```

```python INJECT_CODE(examples/example.py)
from generate import inf_csv

with open("example.csv", "r") as c:
    data = inf_csv(c, header=True)
    for _ in range(4):
        print(next(data))

# ['1', '2', '3']
# ['4', '5', '6']
# ['7', '8', '9']
# ['1', '2', '3']
```

### Design choices
(refer to [generate.py](./generate.py))

##### Use of `__all__`
Since there is really no built-in notion of "private" in Python, people are familiar with the convention of prefacing pseudo-private (ie, "please don't touch my stuff") functions/methods with one or two underscores.

I find that the cue of including the user-facing functions in `__all__` serves as a visual aid in the other direction: these are the functions you may touch.

##### Use of generators
Generators are lazy collections/sequences which can be used to create inexhaustible "streams" of data. For the use case of creating an unlimited stream of data, they make the most sense.

##### Exposing three functions rather than just one
> It is better to have 100 functions operate on one data structure than to have 10 functions operate on 10 data structures

(source [SICP](https://mitpress.mit.edu/sites/default/files/sicp/full-text/sicp/book/node1.html))

Also, what happens if we were to make this a single function?
The signature might have to look like this:
```python
inf_file(handler: IO, filetype: str, header: Optional[bool] = None)
```
This is dumb because `header` only makes sense when `filetype='csv'`.
You could also do something like:
```python
inf_file(handler: IO, filetype: str, **kwargs)
```
and pass `header=True` as a keyword arg, but now you lose the ability to use the function signature as "documentation", of sorts.
Neither option is quite as simple as just exposing three obvious, single-purposed functions.

##### Why not use a base class of some sort?
You probably could use one in place of `gen_loop`, and just implement a method like `generate` or something. 
But given that parameters might change (see above), generalizing gets clunky.
Also, when I think about lazy, infinite sequences with single-arity transformations, it just screams "functional programming".

##### Type hints
Type-hinting in Python being totally optional, you should only include them if they are checked with `mypy` and are sure to be 100% correct. 
An incorrect type hint is just as bad as a stale, misleading comment that wasn't updated/deleted.
