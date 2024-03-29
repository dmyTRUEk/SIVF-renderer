# Documentation



## Entities:
Entity - layer or shape or other special object
- layer -> container for any entities (even layer)
  ```
  "layer": {
      "blending": ["<alpha channel blending type>", "<color channel blending type>"], 
      <entities separated by comma>
  }
  ```

- (soon) object -> container for any shapes (group of shapes)
  ```
  "object": {
      <shapes separated by comma>
  }
  ```

### Shape:
Shape - any final entity, which means it cant have children
- circle ->
  ```
  "circle": {
      "xy": ["<x>", "<y>"],
      "r": "<radius>",
      "color": "<hex color>"
  }
  ```

- square ->
  ```
  "square": {
      "xy": ["<x>", "<y>"],
      "side": "<side>",
      "color": "<hex color>"
  }
  ```

- triangle ->
  ```
  "triangle": {
      "xy": ["<x1>", "<y1>",
          "<x2>", "<y2>",
          "<x3>", "<y3>"],
      "color": "<hex color>"
  }
  ```

### Special Entities:
Special Objects - some very specific and kinda tricky objects with paranormal behavior
- mesh (grid) ->
  ```
  "mesh": {
      "layer": {<entities to be repeated>},
      "n_xleft_ydown_xright_yup": ["5", "5", "5", "5"],
      "dist_xy": ["10%", "10%"]
  }
  ```

- (soon) gradient ->
  ```
  "gradient": {
      <smt?>
  }
  ```

- (not soon) recursion ->
  ```
  "recursion": {
      "layer": {
          <objects to be recursed>
      },
      "depth": "<times it be repeated>",
      "delta_scale": "<delta scale on every step>",
      "changing_vars": {
          <here is vars, that will be changed, for example color, x, y>
      }
  }
  ```



## Value types:
- pixels -> `42`

  (yes, nothing to specify, so just a number already pixels)

- percentage -> `42%`

  (just add % at end of the value)

  50% = (50/100) * plane_height

- metrics -> `42m` or `42dm` or `42cm` or `42mm`

  m - meters

  dm - decimeters

  cm - cantimeters
  
  mm - milimeters



## Blending Types:

### Alpha Blending Types:
- default = 0

  default is overlap

- overlap = 0
  ```
  pixel[y, x] = (
      <r>,
      <g>,
      <b>,
      a
  )
  ```

- add = 1
  ```
  pixels[y, x] = (
      <r>,
      <g>,
      <b>,
      pixels[y, x][3] + a,
  )
  ```

- avg = 2
  ```
  pixels[y, x] = (
      <r>,
      <g>,
      <b>,
      (pixels[y, x][3]*obj_n+a)//(obj_n+1)
  )
  ```

  where obj_n is number of object adding to image

### Color Blending Types:
- default = 0

  default is overlap

- overlap = 0
  ```
  pixels[y, x] = (
      r,
      g,
      b,
      <alpha>
  )
  ```

- add = 1
  ```
  pixels[y, x] = (
      pixels[y, x][0] + r,
      pixels[y, x][1] + g,
      pixels[y, x][2] + b,
      <alpha>
  )
  ```

- avg = 2
  ```
  pixels[y, x] = (
      (pixels[y, x][0]*obj_n+r)//(obj_n+1),
      (pixels[y, x][1]*obj_n+g)//(obj_n+1),
      (pixels[y, x][2]*obj_n+b)//(obj_n+1),
      <alpha>
  )
  ```

  where obj_n is number of object adding to image




