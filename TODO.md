# TODO:

Dont forget to look for [TODO] in code ;)



## Meta:
- write comments in all files (\*.py)
- rewrite documentation



## Refactoring:
- rewrite blend_canvases error using own errors
- add warnings
- remove gloval vars
- in convert_funcs import only sqrt, sin, ..., for security reason



## Changes:
- ? in .sivf use x, y separetly, so: xy -> x, y



## Bugs:
- check if render is pixel perfect



## Optimizations:
- smart bound in parse_and_render_<shape> instead of full canvas
- faster rendering by:
  - [ ] change `if (...): ...` -> `(...)\*(...) + (...)\*(...)`
  - [ ] Cython
  - [ ] matrix operations by numpy
  - [ ] function written on C/C++/Rust (for rust use pyo3)
  - [ ] gpu: render by fragment shaders



## New features:
- different backend support
- 'min', 'max' blending types
- time measurments for every figure
- shapes intersection (overlap, add, 1minus2, 2minus1 etc)
  for better rendering use separate layer, and only then overlap/add/avg main layer and new
- local vars (scoping) in layer
- entities rotating
- entities:
  - ellipse
  - rectange
  - line (endless line)
  - segment (part of line)
  - text: xy, color_fg, color_bg, font, ? width between letters
  - polygon
  - right polygon
- antialiasing (upscaled render and then downscale?)



## Ideas:
- new entities:
  - Bezier curve
  - recursion (but specify steps amount)
- if "import" found in .sivf, terminate render due to vulnerability risk





# DONE:
- 2020.03.22: Added figures: Circle, Square, Added properies: canvas sizes, color scheme, Added comment to my json
- 2020.03.23: Code refactor, 3 examples with images, blending types support (only in code)
- 2020.03.25: Added triangle, Added nested layers, Blendingtype in .sivf, rendering progress output, Mesh
- 2020.03.26: Faster rendering by Cython
- 2020.04.02: nparray -> carray, build from under `/src` bug fixed
- 2020.04.18: Deleted numpy process func in heavy_funcs.pyx, DOCUMENTATION

- 2020.10.29: v0.3.3: Saving before global changes
- 2020.11.04: v0.4.0a1: done new architucture by layer, but only circles for now. Currently, only rgb_logo can be renderer.
- 2020.11.06: v0.4.0a2: Added '.gitignore', Added sivf KeyWords, Added and used Error and Warning systems, A lot of Refactoring, some new Documentation in code
- 2020.11.07: Traceback in Warnings, Added Config, Added delta_xy support for layers, Fixed bug that wrapped figure if part of it was out of canvas



