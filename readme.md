# uglier

> Make your python code a (working) repulsive mess!

## Features
* Make all the variables names in every function look the same 🤸‍♀️
* Turn your python built-in calls into an unreadable tangle of characters  💁‍♀️
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


draw_mandelbrot(-2.0, 1, 36, 78)
```

After:
```python
def DRAWMANDELBROT(XХXX, ХХХХ, XХХХ, XXXХ, XХХX='.,-:;i+hHM$*#@ '):

    ХXXХ = XXXХ / XХХХ
    ХXХX = (XХXX - ХХХХ) * (ﬂᵒ𝒶𝑡(XХХХ) / XXXХ) * ХXXХ

    for ХXХХ in 𝓇𝒶𝕟𝓰𝔢(XХХХ):


        XXХХ = ''


        for ХXXX in 𝓇𝕒𝕟𝓰𝔢(XXXХ):


            XXХX = 𝓬ᵒ𝓂𝓅𝕝𝔢𝕩(ХХХХ + ХXXX * (XХXX - ХХХХ) / XXXХ, ХXХХ * ХXХX / XХХХ - ХXХX / 2)
            ХХXX = XXХX
            for XХXХ in XХХX:

                if 𝕒𝒷𝖘(ХХXX) > 2:

                    break

                ХХXX = ХХXX * ХХXX + XXХX


            XXХХ += XХXХ

        𝓅𝓇𝒾𝕟𝑡(XXХХ)
𝔇𝕽𝕬𝔚𝕸𝕬𝕹𝔇𝕰𝔏ℬ𝕽𝔒𝔗(-2.0, 1, 36, 78)
```

(It *still* works!)

## How??

This takes advantage of python's [unicode normalization](https://www.python.org/dev/peps/pep-3131/). To make all the identifiers look the same, it uses a mix of latin and cryllic characters.

## Acknowledgements

Thanks to [lancer](https://github.com/LeviBorodenko/lancer) for the (hideous) idea.
