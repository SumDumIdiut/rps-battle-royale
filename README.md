# Rock Paper Scissors Battle Royale

A `pygame` "particle battle" simulator, similar to the popular Rock/Paper/Scissors bouncing-ball simulations: dozens of rock/paper/scissors sprites bounce around a fullscreen arena and convert or eliminate each other on contact according to RPS rules, until only one type remains. It's a simulation to watch, not something you actively play.

## Running it

```
pip install pygame
python RPSBR.py
```

Only dependency is `pygame` (plus stdlib `random`, `math`). The window always opens **fullscreen** at your desktop's native resolution (`pygame.display.Info()` + `pygame.FULLSCREEN`).

## Controls

- Menu / Settings screens: mouse to click buttons and drag sliders, `Esc` to go back/quit
- During a simulation: `Esc` or `Q` to return to the main menu

## How it works

`main()` runs a simple menu loop: **Start** launches `run_simulation`, **Settings** opens `show_settings_menu`, and `Q`/`Esc` return to the main menu from either. All three screens (`show_main_menu`, `show_settings_menu`, `run_simulation`) are themselves blocking `while` loops with their own event handling and `clock.tick(FPS)`.

- **Sprites** are generated procedurally at startup (`create_rock_sprite`, `create_paper_sprite`, `create_scissors_sprite`) by painting a small ASCII-art pattern of block characters onto a `pygame.Surface`, pixel by pixel — no external image files for the RPS pieces themselves.
- **Entity** is the rock/paper/scissors particle: it moves at a constant random velocity, bounces off the arena edges, and is bucketed into a spatial hash grid (`GRID_SIZE = 64`) each frame so collision checks only compare entities in nearby cells instead of every pair (an O(n²) avoidance optimization).
- **Combat**: `check_winner()` encodes standard RPS rules. On collision between different types, the loser either dies immediately, or — if **Takeover Mode** is on (default) — gets converted to the winner's type, tracking a per-entity `conversion_count` that removes it once it's been converted `conversions_to_death` times (configurable in Settings, default 3).
- The **Settings** screen exposes sliders/toggles for starting counts of each type (10–1000), takeover mode, conversions-to-death, and the two extras below.
- Simulation speed is adjustable live via an on-screen `Slider` (0.1×–5.0×), which runs the update step multiple times per rendered frame (with a probabilistic extra step for fractional speeds) rather than changing the frame rate.
- When one type is the only one left, `draw_victory_animation` plays a podium animation (1st/2nd/3rd place based on who was eliminated in which order) with an eased rise animation.

### Extras — what the asset files are for

- **`DVD-Logo.jpg`** — used by the `DVDLogo` class when "DVD Logo Killer" is enabled in Settings. It's a classic bouncing DVD-logo screensaver sprite that roams the screen and has a 1-in-4 chance to kill any entity it touches.
- **`Thanos.png`** — used by the `Thanos` class when "Thanos Mode" is enabled. It sits in the bottom-right corner and, once per second, has a 1-in-25 chance to "snap," instantly removing half of all remaining entities (`random.sample`).

## Caveats

- **Asset filename case mismatch on Linux/macOS:** the code loads `pygame.image.load('DVD-logo.jpg')` (lowercase `l`), but the file on disk is `DVD-Logo.jpg` (capital `L`). On a case-sensitive filesystem this load will fail and silently fall through to the `except:` fallback — a plain white rectangle with "DVD" text — instead of the real logo. Rename the file to `DVD-logo.jpg` (or fix the string in code) to see the actual image. `Thanos.png` matches its load path exactly and works as-is.
- Both image loads also assume the working directory is the script's own folder (relative paths `'DVD-logo.jpg'` / `'Thanos.png'`), so running the script from elsewhere will always hit the fallback.
- Always launches fullscreen with no windowed-mode option in the UI.
- With very high entity counts (near the 1000-per-type slider max) the collision/grid logic can visibly slow the framerate since it's still Python-level per-pair checking within each grid cell.
