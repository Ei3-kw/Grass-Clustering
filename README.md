# Grass-Clustering

Source of inspiration:

There are four holes in the garden, dad digged them for the poles to extend the patio. After a pouring rain, two were filled with water but the other two are empty. It was then observed that the species of weeds around the filled and unfilled holes are different, which infers the existence of environmental difference between two spots only three meters apart. It would be interesting to find out the approx seperating line based on the distribution of grass after certain amount of time. 

Assumptions:
- there are only two habitats.
- each species can live and only live in one of the habitats.
- all species want to maximise their occupied area (i.e. there is no waste land at the end?)

Case study:
The Qin Great Wall sits on the 400ml annual rainfall line in China. As agricultural civilization requires >=400 annual rainfall to maintain, this is the border line formed by the millennia of running-in between farming agricultural and nomadic civilization.

Algorithms:
To find a seperate line between two areas, we can spread out individuals and group em into two groups. These two groups are filtered according to the parameters given. The living conditions are different btwn groups and the same within one group. If an individual is exposed to non-suitable condition, it will stop repreducing and die off after a while. Since both groups are trying to maximise their area, the line btwn the two groups will be approx the seperate line after it converges.

