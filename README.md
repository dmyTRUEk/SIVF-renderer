# SIVF-renderer
SIVF - SImple Vector Format

SIVF-renderer - open source program for rendering new open source file format: SIVF



## Pros and Cons: 

### Pros:

- Created to be **simple** and **open source**.

- SIVF uses JSON, while all raster and vector formats uses XML.
  Why? Because it is much more readable.
  Look ![here](https://json.org/example.html) for more.

- Every coordinates (x and y) are **measuring from centre** of the plane,
  and this is very pleasurably for many scenarios,
  so, to place circle in centre of the plane all you need is:
  ```
  "circle": {
      "xy": ["0", "0"],
      "r": "50%",
      "color": "#ff00aaff"
  }
  ```

- Support for three main units:
  - Pixels
  - Percentage (%)
  - (soon) Metrics (m, cm, mm)

- Forcely transparent object, so you can **easely crop** a circle (example 2, last circle)

- Vars: declare vars, and the use it for shape's coords, sizes - etc (example 4)

- **Formulas** and numbers: 
  Instead of 
  `"xy": ["70.711%", "2.535cm"]`
  Here you can use
  `"xy": ["sqrt(2)*50%", "log10(7)*3cm"]`
  Which have benefits of calculating as many digits, as you need.

- (soon) Custom **antialiasing** (msaa, fxaa, taa - etc.)

### Cons:

- As I develop the ptoject by myself, so it grows slow

- it is hard to became popular, so big graphic editors may not support it soon...



## Example 1: Not a smiley face
![Image example 1](https://raw.githubusercontent.com/dmytruek/sivf-renderer/master/examples/image_example_1.png)

SIVF file content:
```
{
    "sizes_wh": ["500", "500"],
    "color_scheme": "rgb",

    "image": {
        "layer1": {
            "circle": {
                "xy": ["0%", "0%"],
                "r": "50%",
                "color": "#ff00aaff"
            },
            "square1": {
                "xy": ["25%", "0"],
                "side": "25%",
                "color": "#ff000000"
            },
            "square2": {
                "xy": ["-25%", "0"],
                "side": "25%",
                "color": "#ff000000"
            },
            "square3": {
                "xy": ["0", "-25%"],
                "side": "10%",
                "color": "#ff000000"
            }
        }
    }
} 
```



## Example 2: RGB logo
![Image example 2](https://raw.githubusercontent.com/dmytruek/sivf-renderer/master/examples/image_example_2.png)

SIVF file content:
```
{
    "sizes_wh": ["512", "512"],
    "color_scheme": "rgb",

    "image": {
        "layer1": {
            "blending": ["add", "overlap"],
            "circle1": {
                "xy": ["-25.981%", "-15%"],
                "r": "43.589%",
                "color": "#ffff0000"
            },
            "circle2": {
                "xy": ["0%", "30%"],
                "r": "43.589%",
                "color": "#ff00ff00"
            },
            "circle3": {
                "xy": ["25.981%", "-15%"],
                "r": "43.589%",
                "color": "#ff0000ff"
            },
            "circle4": {
                "inverse": "true",
                "xy": ["0", "0"],
                "r": "50%",
                "color": "#00000000"
            }
        }
    }
} 
```



## Example 3: Handmade recursion of circles and squares
![Image example 3](https://raw.githubusercontent.com/dmytruek/sivf-renderer/master/examples/image_example_3.png)

SIVF file content:
```
{
    "sizes_wh": ["1152", "1152"],
    "color_scheme": "rgb",

    "image": {
        "layer1": {
            "square1": {
                "xy": ["0", "0"],
                "side": "1152",
                "color": "#ff000000"
            },
            "circle1": {
                "xy": ["0", "0"],
                "r": "576",
                "color": "#ffffffff"
            }
        },



        "layer2": {
            "square1": {
                "xy": ["384", "0"],
                "side": "384",
                "color": "#ff202020"
            },
            "circle1": {
                "xy": ["384", "0"],
                "r": "192",
                "color": "#ffe0e0e0"
            },

            "square2": {
                "xy": ["0", "384"],
                "side": "384",
                "color": "#ff202020"
            },
            "circle2": {
                "xy": ["0", "384"],
                "r": "192",
                "color": "#ffe0e0e0"
            },

            "square3": {
                "xy": ["-384", "0"],
                "side": "384",
                "color": "#ff202020"
            },
            "circle3": {
                "xy": ["-384", "0"],
                "r": "192",
                "color": "#ffe0e0e0"
            },
            
            "square4": {
                "xy": ["0", "-384"],
                "side": "384",
                "color": "#ff202020"
            },
            "circle4": {
                "xy": ["0", "-384"],
                "r": "192",
                "color": "#ffe0e0e0"
            }
        },



        "layer3": {
            ...
        }
```



## Example 4: Vars in Action
![Image example 4](https://raw.githubusercontent.com/dmytruek/sivf-renderer/master/examples/image_example_4.png)

So: 
- changing `shape_pos` affects on all shapes' distances from centre,
- and changing `shape_size` affects on all shapes' size (square->side, circle->radius)
- and changing `circle_zoom` affects on how much every circle bigger then square

SIVF file content:
```
{
    "sizes_wh": ["600", "600"],
    "color_scheme": "rgb",

    "vars": {
        "shape_pos": "18",
        "shape_size": "30",

        "circle_zoom": "0.8"
    },

    "image": {
        "layer1": {
            "blending": ["overlap", "overlap"],

            "square1": {
                "xy": ["shape_pos %", "shape_pos %"],
                "side": "shape_size %",
                "color": "#ff000000"
            },
            "circle1": {
                "xy": ["shape_pos %", "shape_pos %"],
                "r": "circle_zoom*shape_size/2 %",
                "color": "#ffffffff"
            },

            "square2": {
                "xy": ["-shape_pos %", "shape_pos %"],
                "side": "shape_size %",
                "color": "#ff000000"
            },
            "circle2": {
                "xy": ["-shape_pos %", "shape_pos %"],
                "r": "circle_zoom*shape_size/2 %",
                "color": "#ffffffff"
            },

            "square3": {
                "xy": ["-shape_pos %", "-shape_pos %"],
                "side": "shape_size %",
                "color": "#ff000000"
            },
            "circle3": {
                "xy": ["-shape_pos %", "-shape_pos %"],
                "r": "circle_zoom*shape_size/2 %",
                "color": "#ffffffff"
            },

            "square4": {
                "xy": ["shape_pos %", "-shape_pos %"],
                "side": "shape_size %",
                "color": "#ff000000"
            },
            "circle4": {
                "xy": ["shape_pos %", "-shape_pos %"],
                "r": "circle_zoom*shape_size/2 %",
                "color": "#ffffffff"
            }
        }
    }
}
```



More examples ![here](https://raw.githubusercontent.com/dmytruek/sivf-renderer/dev/EXAMPLES.md)
