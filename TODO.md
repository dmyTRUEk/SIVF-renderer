# TODO:

Dont forget to look for [TODO] in code ;)



## Meta:
- write comments in all files (\*.py)
- rewrite documentation
- check examples, write comments in them



## Refactoring:
- add warnings
- remove gloval vars
- in convert_funcs import only sqrt, sin, etc, for security reason



## Changes:
- ? in .sivf use x, y separetly, so: xy -> x, y



## Bugs:
- check if render is pixel perfect



## Optimizations:
- smart bound in parse_and_render_<shape> instead of full canvas
- faster rendering by:
  - [ ] change `if (...): ...` -> `(...)*(...) + (...)*(...)`
  - [ ] Cython
  - [ ] fast operations for every element in array by numpy
  - [ ] function written on C/C++/Rust (for rust use pyo3)
  - [ ] gpu: render by fragment shaders: (qtrender, opengl, vulkan)



## New features:
- shapes intersection (overlap, add, 1minus2, 2minus1 etc)
- different backend support:
  - yaml
  - sivf any
  - cython
  - rust
  - numpy
  - gpu
  - render any
- time measurments for every figure
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
- 2020.03.22: v0.1: Added figures: Circle, Square, Added properies: canvas sizes, color scheme, Added comment to my json
- 2020.03.23: v0.2: Code refactor, 3 examples with images, blending types support (only in code)
- 2020.03.25: v0.3: Added triangle, Added nested layers, Blendingtype in .sivf, rendering progress output, Mesh
- 2020.03.26: v0.3.2: Faster rendering by Cython, nparray -> carray, build from under `/src` bug fixed, Deleted numpy process func in heavy_funcs.pyx, DOCUMENTATION

- 2020.10.29: v0.3.3: Saving before global changes
- 2020.11.04: v0.4.0a1: done new architucture by layer, but only circles for now.
  Currently, only rgb_logo can be renderer.
- 2020.11.06: v0.4.0a2: Added '.gitignore', Added sivf KeyWords,
  Added and used Error and Warning systems,
  A lot of Refactoring, some new Documentation in code
- 2020.11.07: v0.4.1: Added Gradient, Added Config, Added Log system,
  Added delta_xy support for layers, Added min, max blend types,
  Fixed bug that wrapped figure if part of it was out of canvas,
  Traceback in Warnings, 



