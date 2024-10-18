import os
from termcolor import colored

def bool_input(name: str, default = True) -> bool:
    raw = input(f'{name} ({'Y/n' if default else 'y/N'}): ')
    if default:
        return False if len(raw) != 0 and raw.strip()[0].lower() == 'n' else True
    else:
        return True if len(raw) != 0 and raw.strip()[0].lower() == 'y' else False

GAP = 10

inner_gap = bool_input('inner gap')
waybar_gap = bool_input('waybar gap')
top = bool_input('top', default=False)

# output_path = os.path.expanduser('~/.config/sway/config')

with open(os.path.expanduser('~/.config/rice/public/config.sway'), 'r') as source, open(os.path.expanduser('~/.config/sway/config'), 'w') as destination:
    content = source.read()

    content += f'\ngaps inner {GAP if inner_gap else 0}'

    destination.write(content)

# waybar
with open(os.path.expanduser('~/.config/rice/public/config.waybar'), 'r') as source, open(os.path.expanduser('~/.config/waybar/config'), 'w') as destination:
    content = source.read()
    
    lines = content.split("\n")
    lines.insert(-2, f"  \"position\": \"{'top' if top else 'bottom'}\",")

    content = '\n'.join(lines)
    destination.write(content)

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

    destination.write(content)
#

os.system("swaymsg reload")
