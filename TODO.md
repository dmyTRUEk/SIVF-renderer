# TODO:

Dont forget to look for [TODO] in code ;)



## Meta:

- write comments in all files (*.py *.md)



## Refactoring:

- rename 'utils' -> 'funcs_utils'

- rename in code 'layer' -> 'canvas', because layer is .sivf property

- rename 'var' -> 'vars'?

- print 'parsing ent...' out of loop?

- use 'layer' instead of 'l' and so on

- use or delete 'shape_number' in one of main functions

- in convert_funcs import only sqrt, sin, ..., for security reason

- rewrite heavy_funcs_cy.pyx from heavy_funcs_py.py



## Optimisations:

- faster rendering
  - [ ] Cython 
  - [ ] use matrix operations by numpy
  - [ ] by render function written on C/C++/Rust (for rust use pyo3)



## New features:

- add 'min', 'max' blending types

- add dx, dy for layers

- add time measurments for every figure

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

- antialiasing (just upscaled render and then downscale?)



## Ideas:

- add entities:
  - Bezier curve
  - recursion (but specify steps amount)

- if "import" found in .sivf, terminate render due to vulnerability risk



