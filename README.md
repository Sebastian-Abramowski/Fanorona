
# Fanorona game
A simple program that allows you to play
[fanorona](https://en.wikipedia.org/wiki/Fanorona) game written in pygame, Python.





## Features

- Generating board depending on the size of the window and number of rows and columns
- Playing with two people together
- Playing against computer that makes random allowed moves
- Playing against computer that makes moves that captures the most pawns
- Starting, moving and winning sounds
- Hints that indicate what pawns can you pick from when some capture is possible
- Hints that indicate where can you move a selected pawn
- Showing whose turn is it and a number of round



## Meanings of colours

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Default white pawn | ![colour_of_pawn_white](https://user-images.githubusercontent.com/113067612/210139405-cd630105-763c-43dd-b6e7-00f8e1ed4b0b.png) |
| Default black pawn | ![colour_of_pawn_black](https://user-images.githubusercontent.com/113067612/210139441-5787cb2e-3a13-43d8-90fb-46d5cd338da4.png) |
| Picking what pawn to capture (black) | ![colour_of_pawn_when_picking2 (1)](https://user-images.githubusercontent.com/113067612/210139736-335214fb-0622-47a9-aea0-f1b7b8fb12ca.png) |
| Picking what pawn to capture (white) | ![colour_of_pawn_when_picking_2](https://user-images.githubusercontent.com/113067612/210139493-1449c52d-acf1-4b23-863d-297bef8430c5.png)
| Highlight of picked pawn  | ![highlight_selected](https://user-images.githubusercontent.com/113067612/210139512-cddfe640-c2e0-4828-b2b6-91c695dcfabb.png) |
| Highlight of pawn that is able to capture | ![highlight_able_to_capture2](https://user-images.githubusercontent.com/113067612/210139538-9e7d60dd-1d44-4343-b790-3fcfdd9fa55f.png) |
| Indicates move that captures by approach| ![approach_cap_ind](https://user-images.githubusercontent.com/113067612/210139569-6653d892-bdba-425a-b092-80dd9bee46de.png) |
| Indicates move that captures by withdrawal | ![withdrawal_cap_ind](https://user-images.githubusercontent.com/113067612/210139579-f7d7a05f-0d6d-4e90-8424-46a15a1ef968.png) |
| Indicates move that captures either by approach or withdrawal | ![problematic_capture_ind](https://user-images.githubusercontent.com/113067612/210139576-5e8c13d4-c9c2-4aa2-9d7c-7be44a058184.png) |
| Indicates paika move (no captures) | ![paika_ind](https://user-images.githubusercontent.com/113067612/210139574-265e9d70-bdba-4ca0-9704-4dda05f0041d.png) |



## How it looks

![screen2](https://user-images.githubusercontent.com/113067612/210140032-de53a811-7de3-4f9b-98de-44e9ab1bc58b.png)
![screen4](https://user-images.githubusercontent.com/113067612/210140066-50ee9ff7-2903-4017-9ecc-cb33ef5021c2.png)
![screen3](https://user-images.githubusercontent.com/113067612/210140058-0dc389aa-310c-4e41-80bd-12028861d1e2.png)

## Gifs

![ezgif com-gif-maker](https://user-images.githubusercontent.com/113067612/210140771-265570c6-76bb-482f-87b1-62a0d5650b9d.gif)
![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/113067612/210140777-941329e0-7a08-4ba9-a2a3-c2d63ddab8f1.gif)


## Usage

##### Running from the command line
#### pip install pygame <br />
#### python main.py <br />
###### Change constants.py if you want to change a number of rows and columns of the board
