# Examples:



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



## Example 5: Overlaping Circles
![Image example 5](https://raw.githubusercontent.com/dmytruek/sivf-renderer/dev/examples/image_example_5.png)

This strange effect creates because circles are overlaping many times, and color and alpha is adding.

SIVF file content:
```
{
    "sizes_wh": ["1000", "1000"],
    "color_scheme": "rgb",

    "vars": {
        "size": "30%",
        "n": "3",
        "offset": "10%"
    },

    "image": {
        "layer1": {

            "mesh": {
                "layer": {
                    "blending": ["add", "add"],
                    "circle1": {
                        "xy": ["0", "0"],
                        "r": "0.5*size",
                        "color": "#5040ff00"
                    }
                    //"triangle": {
                    //    "inverse": "true",
                    //    "xy": ["-0.5*_size", "-0.5*_size",
                    //        "0", "0.5*_size",
                    //        "0.5*_size", "-0.5*_size"],
                    //    "color": "#20ff3000"
                    //}
                },
                "n_xleft_ydown_xright_yup": ["n", "n", "n", "n"],
                "delta_xy": ["offset", "offset"]
            }

        }
    }
}
```



## Example 6: Overlaping Triangles
![Image example 6](https://raw.githubusercontent.com/dmytruek/sivf-renderer/dev/examples/image_example_6.png)

This strange effect creates because circles are overlaping many times, and color and alpha is adding.

SIVF file content:
```
{
    "sizes_wh": ["1000", "1000"],
    "color_scheme": "rgb",

    "vars": {
        "size": "60%",
        "n": "3",
        "offset": "5%"
    },

    "image": {
        "layer1": {

            "mesh": {
                "layer": {
                    "blending": ["add", "add"],
                    "triangle": {
                        "inverse": "true",
                        "xy": ["-0.5*size", "-0.5*size",
                            "0", "0.5*size",
                            "0.5*size", "-0.5*size"],
                        "color": "#20ff3000"
                    }
                },
                "n_xleft_ydown_xright_yup": ["n", "n", "n", "n"],
                "delta_xy": ["offset", "offset"]
            }

        }
    }
}
```

