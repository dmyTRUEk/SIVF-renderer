# TODO:



## Meta:

- write comments in all files (*.py *.md)



## Refactoring:

- rename 'var' -> 'vars'?

- rewrite main.py using Layer



## Optimisations:

- use array of functions for blend type choosing

- do render throught separate layer

- faster rendering
  - [x] Cython 
  - [ ] ? by numpy
  - [ ] by render function written on C/C++/Rust (for rust use pyo3)



## New features:

- add dx, dy for layers

- shapes intersection (overlap, add, 1minus2, 2minus1 etc)
  for better rendering use separate layer, and only then overlap/add/avg main layer and new

- local vars (scoping) in layer

- entities rotating

- add entities:
  - ellipse
  - rectange
  - line (endless line)
  - segment (part of line)
  - polygon
  - right polygon
  - gradient by n points

- antialiasing



## Ideas:

- add entities:
  - Bezier curve
  - recursion (but specify steps amount)

- if "import" found in .sivf, terminate rendering due to vulnerability risk



