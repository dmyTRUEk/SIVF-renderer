# Documentation



## Entities:
Entity - layer or shape or other special object
- l = layer -> container for any entities
  ```
  "layer": {
      <entities separated by comma>
  }
  ```
  or shorter:
  ```
  "l": {
      <entities separated by comma>
  }
  ```

- o = object -> container for any figures (group of figures)
  ```
  "object": {
      <figures separated by comma>
  }
  ```
  or shorter:
  ```
  "o": {
      <figures separated by comma>
  }
  ```

### Figures:
Figure - any final entity, which means it cant have children
- c = circle ->
  ```
  "circle": {
      "xy": ["<x>", "<y>"],
      "r": "<radius>",
      "color": "<hex color>"
  }
  ```
  or shorter:
  ```
  "c": {
      "xy": ["<x>", "<y>"],
      "r": "<radius>",
      "color": "<hex color>"
  }
  ```

- s = square ->
  ```
  "square": {
      "xy": ["<x>", "<y>"],
      "side": "<side>",
      "color": "<hex color>"
  }
  ```
  or shorter:
  ```
  "square": {
      "xy": ["<x>", "<y>"],
      "side": "<side>",
      "color": "<hex color>"
  }
  ```

### Special Entities:
Special Objects - some very specific and kinda tricky objects with paranormal behavior
- (soon) r = recursion ->
  ```
  "recursion": {
      "layer": {
          <>
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

### Alpha Blending Types:
- default = 0

  default is overlap

- overlap = 0

  `pixel[y, x] = color`

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



