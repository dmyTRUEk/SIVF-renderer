# SIVF-renderer
SIVF - SImple Vector Format

SIVF-renderer - open source program for rendering new open source file format: SIVF



## Example 1: Not smiley face
![alt text](https://raw.githubusercontent.com/dmytruek/sivf-renderer/master/image_example_1.png)

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
![alt text](https://raw.githubusercontent.com/dmytruek/sivf-renderer/master/image_example_2.png)

SIVF file content:
```
{
    "sizes_wh": ["512", "512"],
    "color_scheme": "rgb",

    "image": {
        "layer1": {
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
![alt text](https://raw.githubusercontent.com/dmytruek/sivf-renderer/master/image_example_3.png)

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
