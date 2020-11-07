# TODO:

Dont forget to look for [TODO] in code ;)



## Meta:
- write comments in all files (*.py *.md)
- rewrite documentation



## Refactoring:
- rewrite blend_canvases error using own errors
- add warnings
- remove gloval vars
- in convert_funcs import only sqrt, sin, ..., for security reason



## Changes:
- in .sivf use x, y separetly, so: xy -> x, y
- dont pass delta_xy to parse_and_render_<shape>



## Bugs:
- if delta_x/y > 25% -> wrapping shoudnt be done
  (caused by blend_canvases?)
- check if render is pixel perfect



## Optimisations:
- smart bound in parse_and_render_<shape> instead of full canvas
- faster rendering by:
  - [ ] change 'if (...): ...' -> '(...)\*(...) + (...)\*(...)'
  - [ ] Cython
  - [ ] matrix operations by numpy
  - [ ] function written on C/C++/Rust (for rust use pyo3)
  - [ ] gpu: render by fragment shaders



## New features:
- different backend support
- 'min', 'max' blending types
- 'dx', 'dy' for layers
- time measurments for every figure
- shapes intersection (overlap, add, 1minus2, 2minus1 etc)
  for better rendering use separate layer, and only then overlap/add/avg main layer and new
- local vars (scoping) in layer
- entities rotating
- entities:
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
- new entities:
  - Bezier curve
  - recursion (but specify steps amount)
- if "import" found in .sivf, terminate render due to vulnerability risk



