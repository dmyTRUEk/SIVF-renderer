# TODO:

Dont forget to look for [TODO] in code ;)



## Meta:
- rewrite documentation
- polish all project, and make v0.5.0
- `exmaples_tmp/` -> `examples/`
- write comments in all files (\*.py)



## Refactoring:
- solve default parametrs, such as is_fading(default)=false
- add warnings (what and where?)



## Changes:
- 



## Bugs:
- in gradient when `is_fading=False` add `min(255, ...)`
- in `convert_expression_to_units` sort vars by length,
  so firstly it replaces longest vars, and only then shorter
- change Log for rendering progress:
  `rendering <shape>:` -> `rendering <shape> mask` and `rendering <shape> color`
- check if render is pixel perfect



## Optimizations:
- smart bound in parse_and_render_<shape> instead of full canvas
- faster rendering by:
  - [ ] Cython
  - [ ] fast operations for every element in array by numpy
  - [ ] function written on C/C++/Rust (for rust use pyo3)
  - [ ] OpenCL, for example pyopencl
  - [ ] gpu: render by fragment shaders: (qtrender, opengl, vulkan)



## New features:
- layer scale, like delta_xy
- if user doesnt input file in args, open file manager to choose
- log in file
- different backend support:
  - [x] yaml
  - [ ] sivf any (json or yaml)
  - [ ] rust
  - [ ] numpy
  - [ ] gpu
  - [ ] render any
- local vars (scoping) in layer
- entities rotating
- entities:
  - ellipse
  - rectange
  - formula: `formula_for_argb: [255, 255*sin(x), 255*cos(y), 255*sin(x+y)]`
  - line (endless line)
  - segment (part of line)
  - text: xy, color_fg, color_bg, font, ? width between letters
  - mask: layer_bg, layer_mask, ?
  - polygon
  - right polygon
- antialiasing (upscaled render and then downscale?)
- different color scheme support



## Ideas:
- new entities:
  - Bezier curve
  - recursion (but specify steps amount)
- if "import" found in .sivf, terminate render due to vulnerability risk





# CHANGELOG:
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
- 2020.11.19: v0.4.2h: added combine
- 2020.11.25: v0.4.3: delta_xy -> (delta_x, delta_y), Cython support
- 2021.03.25: v0.4.4: added YAML support in heavy_funcs_python.py, fixed some error related to inverse and color starting from #, rewrite main.py
- 2021.04.05: v0.4.4(2): fixed is_fading in gradient for yaml, added datetime to output file name, but not in `funcs_heavy_*.*`
- 2021.04.05: v0.4.5: new output file name format: 'title_date_resolution.png', fixed bug in gradient is_fading=True when rgb becomes > 255
- 2021.04.06: v0.5.0a1: time for every shape, converting expressions to units and colors to ints only in main
- 2021.04.08: v0.5.0a2: fixed inversed delta_y, optimized mask rendering, better comment removment, removed many unuseful comments, many polishment



