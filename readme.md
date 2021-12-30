# uglier

> Make your python code a (working) repulsive mess!

## Features
* Make all the variables names in every function look the same 🤸‍♀️
* Turn your builtins into an unreadable tangle of characters  💁‍♀️
* Add ugly new lines 💩
* Code *still* runs

## Example

Before:
```python
def draw_mandelbrot(maxX, minX, height, width, chars=" .,-:;i+hHM$*#@ "):
    aspectRatio = width / height
    yScale = (maxX - minX) * (float(height) / width) * aspectRatio

    for y in range(height):
        line = ""
        for x in range(width):
            c = complex(
                minX + x * (maxX - minX) / width, y * yScale / height - yScale / 2
            )
            z = c
            for char in chars:
                if abs(z) > 2:
                    break
                z = z * z + c
            line += char
        print(line)


draw_mandelbrot(-2.0, 1, 78, 36)
```

After:
```python
def DRAWMANDELBROT(ТTТТ, ТTТT, ТТТТ, TТТТ, ТТTT=' .,-:;i+hHM$*#@ '):


    TТTТ = TТТТ / ТТТТ


    TТTT = (ТTТТ - ТTТT) * (ﬂᵒ𝕒𝑡(ТТТТ) / TТТТ) * TТTТ
    for TTTТ in 𝓇𝕒𝕟ᵍ𝔢(ТТТТ):

        ТТTТ = ''
        for ТТТT in 𝓇𝒶𝕟ᵍ𝔢(TТТТ):


            TТТT = 𝓬ᵒ𝓂𝓅𝔩𝔢𝕩(ТTТT + ТТТT * (ТTТТ - ТTТT) / TТТТ, TTTТ * TТTT / ТТТТ - TТTT / 2)


            TTТТ = TТТT

            for ТTTТ in ТТTT:

                if 𝒶𝒷𝕤(TTТТ) > 2:
                    break

                TTТТ = TTТТ * TTТТ + TТТT


            ТТTТ += ТTTТ
        𝓅𝓇𝓲𝕟𝑡(ТТTТ)


𝕯𝕽𝕬𝖂𝕸𝕬𝕹𝕯𝔈𝔏𝕭𝕽𝔒𝔗(-2.0, 1, 78, 36)
```

(It *still* works!)

## Acknowledgements

Thanks to [lancer](https://github.com/LeviBorodenko/lancer) for the (hideous) idea.
