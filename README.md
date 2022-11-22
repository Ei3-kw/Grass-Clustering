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

Update:

1.0
- Plant has different stages, only spread after mature
- Multi season VS single season plant, single season plant dies after reaching max stage whereas multi season ones continue living
- Multiple plants are allowed on the same tile with higher dying rate due to competition
- Each tile is represented by the most mature (max(current stage/ max stage)) plant on it
- If two or more plants are equally mature, multi season > single season

1.1
- code runs faster now that deepcopy of the plant list is replaced
- cProfile is added to check the performance

TODOs
- more than two species 
- more than one seperating categories
- use np matrix to keep track of tiles (can't do plants as each tile contains a list of plants)

Possible applications:
- Find seperating lines between relality and one's discription (in this case spread will not be plant reproduce but rather event progressing)
- example: TODO
