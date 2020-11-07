# TODO:

Dont forget to look for [TODO] in code ;)



## Meta:
- write comments in all files (*.py *.md)
- rewrite documentation



## Refactoring:
- add warnings
- use sivf KW everywhere
- print 'parsing ent...' out of loop?
- remove gloval vars
- use or delete 'shape_number' in one of main functions
- in convert_funcs import only sqrt, sin, ..., for security reason
- rewrite heavy_funcs_cy.pyx from heavy_funcs_py.py



## Changes:
- in .sivf use x, y separetly, so: xy -> x, y



## Optimisations:
- smart bound in parse_and_render_<shape> instead of full canvas
- faster rendering by:
  - [ ] change 'if (...): ...' -> '(...)\*(...) + (...)\*(...)'
  - [ ] Cython 
  - [ ] matrix operations by numpy
  - [ ] function written on C/C++/Rust (for rust use pyo3)
  - [ ] gpu: render by fragment shaders



## New features:
- add different backend support:
  - different rendering types
  - different sivf types:
    - json
    - yaml
- add 'min', 'max' blending types
- add dx, dy for layers
- add yaml support
- add time measurments for every figure
- shapes intersection (overlap, add, 1minus2, 2minus1 etc)
  for better rendering use separate layer, and only then overlap/add/avg main layer and new
- local vars (scoping) in layer
- entities rotating
- add entities:
  - gradient by n points
  - ellipse
  - rectange
  - line (endless line)
  - segment (part of line)
  - text: xy, color_fg, color_bg, font, ? width between letters
  - polygon
  - right polygon
- antialiasing (just upscaled render and then downscale?)



## Ideas:
- add entities:
  - Bezier curve
  - recursion (but specify steps amount)
- if "import" found in .sivf, terminate render due to vulnerability risk



