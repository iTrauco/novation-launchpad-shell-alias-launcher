# Launchpad Mini MK3 Grid Mapping Reference

## Grid Coordinates Layout

```
   0 1 2 3 4 5 6 7  (x-coordinates →)
0  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
1  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
2  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
3  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
4  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
5  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
6  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
7  ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️ ⬜️
(y-coordinates ↓)
```

## Coordinate Reference

- Origin (0,0): Top-left corner
- X-axis: Increases left to right (0-7)
- Y-axis: Increases top to bottom (0-7)

## Common Positions

- (0,0): Top-left corner
- (7,0): Top-right corner
- (0,7): Bottom-left corner
- (7,7): Bottom-right corner

## Quadrants

```
   0 1 2 3 4 5 6 7
0  Q1  |  Q2
1      |
2      |
3 -----+-----
4  Q3  |  Q4
5      |
6      |
7      |
```

- Q1: Top-left quadrant (x: 0-3, y: 0-3)
- Q2: Top-right quadrant (x: 4-7, y: 0-3)
- Q3: Bottom-left quadrant (x: 0-3, y: 4-7)
- Q4: Bottom-right quadrant (x: 4-7, y: 4-7)

## Color Constants

```python
class Colors:
    OFF = 0      # No light
    RED = 5      # 🔴
    GREEN = 21   # 💚
    YELLOW = 13  # 💛
    BLUE = 45    # 💙
    PURPLE = 53  # 💜
    CYAN = 37    # 💠
    WHITE = 3    # ⚪
```

## Example Button Mappings

```python
# Corner buttons
top_left = (0, 0)      # Origin point
top_right = (7, 0)     # Right edge
bottom_left = (0, 7)   # Bottom edge
bottom_right = (7, 7)  # Opposite corner

# Center buttons
center_left = (0, 3)
center_right = (7, 3)
center_top = (3, 0)
center_bottom = (3, 7)
```

## MIDI Note Calculation

The MIDI note number for any coordinate can be calculated using:
```python
note = x + (y * 10)
```

For example:
- (0,0) = 0 + (0 * 10) = 0
- (1,0) = 1 + (0 * 10) = 1
- (0,1) = 0 + (1 * 10) = 10
- (7,7) = 7 + (7 * 10) = 77
