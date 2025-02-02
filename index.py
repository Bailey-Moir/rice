import os
import math
from termcolor import colored

def bool_input(name: str, default = True) -> bool:
    raw = input(f'{name} ({'Y/n' if default else 'y/N'}): ')
    if default:
        return False if len(raw) != 0 and raw.strip()[0].lower() == 'n' else True
    else:
        return True if len(raw) != 0 and raw.strip()[0].lower() == 'y' else False

def float_input(name: str, default = 0.5) -> float:
    raw = input(f'{name} ({default:.1f}f): ')
    try:
        # return math.ceil(10*float(raw))/10
        return float(raw)
    except ValueError:
        return default

def int_input(name: str, default = 0) -> int:
    raw = input(f'{name} ({default:.0f}): ')
    try:
        return int(raw)
    except ValueError:
        return default


GAP = 10

defaults = []
with open(os.path.join(os.path.dirname(__file__),"data"), 'r') as source:
    content = source.read()

    defaults = content.split('\n')

is_catpuccin = bool_input('catpuccin', default=(defaults[0] == 'True'))
background_number = int(defaults[1])
if is_catpuccin:
    background_number = int_input('background number', default=background_number)
inner_gap = bool_input('inner gap', default=(defaults[2] == 'True')) # False
waybar_gap = bool_input('waybar gap', default=(defaults[3] == 'True'))
top = bool_input('top', default=(defaults[4] == 'True'))
corner = int_input('corner radius', default=int(defaults[5]))
bar_opactiy = float_input('waybar opacity', default=float(defaults[6]))
foot_opacity = float_input('foot opacity', default=float(defaults[7]))


# saving config
with open(os.path.join(os.path.dirname(__file__),"data"), 'w') as destination:
    content = ''

    content += str(is_catpuccin)+'\n'
    content += str(background_number)+'\n'
    content += str(inner_gap)+'\n'
    content += str(waybar_gap)+'\n'
    content += str(top)+'\n'
    content += str(corner)+'\n'
    content += str(bar_opactiy)+'\n'
    content += str(foot_opacity)+'\n'

    destination.write(content)


# sway
with open(os.path.expanduser('~/.config/rice/public/config.sway'), 'r') as source, open(os.path.expanduser('~/.config/sway/config'), 'w') as destination:
    content = source.read()

    backgrounds = os.listdir(os.path.expanduser("~/.config/backgrounds/catpuccin"))

    content += f'\ngaps inner {GAP if inner_gap else 0}'
    content += f'\ncorner_radius {corner}'
    content += f'\noutput * bg ~/.config/backgrounds/{("catpuccin/"+backgrounds[background_number%len(backgrounds)]) if is_catpuccin else "tile.png"} {"fill" if is_catpuccin else "tile"}'

    destination.write(content)

# waybar
with open(os.path.expanduser('~/.config/rice/public/config.waybar'), 'r') as source, open(os.path.expanduser('~/.config/waybar/config'), 'w') as destination:
    content = source.read()
    
    lines = content.split("\n")
    lines.insert(-2, f"  \"position\": \"{'top' if top else 'bottom'}\",")

    content = '\n'.join(lines)
    destination.write(content)

# waybar css
with open(os.path.expanduser('~/.config/rice/public/style.waybar.css'), 'r') as source, open(os.path.expanduser('~/.config/waybar/style.css'), 'w') as destination:
    content = source.read()

    if waybar_gap:
        marginCSS = f"""
            .modules-left {{ margin-left: {GAP}px; }}
            .modules-right {{ margin-right: {GAP}px; }}
            .modules-left, .modules-center, .modules-right {{ margin-{'top' if top else 'bottom'}: {GAP}px; }}
        """
        content += marginCSS

    content += f'window#waybar {{ background: {'transparent' if waybar_gap else '@base'}; }}'

    rounded = 10*math.ceil(10*bar_opactiy)
    content = content.replace("@base;", f'@base{f'{rounded:.0f}' if rounded != 100 else ""};')

    destination.write(content)

# foot
with open(os.path.expanduser('~/.config/rice/public/config.foot'), 'r') as source, open(os.path.expanduser('~/.config/foot/foot.ini'), 'w') as destination:
    content = source.read()

    content = content.replace('[colors]\n', f'[colors]\nalpha={foot_opacity}\nbackground={"1E1D2D" if is_catpuccin else "161616"}\n')

    destination.write(content)

# theme.css
with open(os.path.expanduser('~/.config/theme.css'), 'w') as destination:
    content = ''

    for alpha in range(10,110,10):
        content += f'@define-color base{alpha if alpha != 100 else ""} rgba({"30, 29, 45" if is_catpuccin else "22, 22, 22"}, {alpha/100});\n'
        content += f'@define-color white{alpha if alpha != 100 else ""} rgba({"191, 198, 212" if is_catpuccin else "242, 244, 248"}, {alpha/100});\n'

    destination.write(content)

os.system("swaymsg reload")
