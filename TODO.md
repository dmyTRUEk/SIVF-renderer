# TODO:

- use `process_entity()` instead of `render_from_image_code()`

- support blending type from sivf instead of code

- vars in .sivf

- support nested layers by 'render_entity()' func (entity is layer or object),
  which recursively calls 'render_entity()' if it is layer, 
  or 'prepare_render_object()' if it is object
  - rename 'prepare_render_object()' -> 'render_entity()'

- write comments in all files: *.py *.md

- antialiasing

- add entities:
  - nested layers
  - ellipse
  - rectange
  - line
  - segment (part of line)
  - Bezier curve
  - recursion (but specify steps amount)

- objects rotating

- faster rendering
  - by numpy?
  - by render function written on C/C++/Rust










