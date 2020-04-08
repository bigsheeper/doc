###安装
```
sudo add-apt-repository ppa:gnome-terminator
sudo apt-get update
sudo apt-get install terminator
```

###卸载
```
sudo apt-get remove terminator
sudo apt-get remove --auto-remove terminator
```
###配置
**文件路径**`filepath=~/.config/terminator/config`

###配置方案
```
[global_config]
  always_on_top = True
  focus = system
  handle_size = 1
  inactive_color_offset = 1.0
  suppress_multiple_term_dialog = True
  title_transmit_bg_color = "#d30102"
[keybindings]
[layouts]
  [[default]]
    [[[child1]]]
      parent = window0
      type = Terminal
    [[[window0]]]
      parent = ""
      type = Window
[plugins]
[profiles]
  [[default]]
    background_color = "#2d2d2d"
    background_darkness = 0.74
    background_image = None
    background_type = transparent
    copy_on_selection = True
    font = Monospace 20
    foreground_color = "#eee9e9"
    palette = "#2d2d2d:#f2777a:#99cc99:#ffcc66:#6699cc:#cc99cc:#66cccc:#d3d0c8:#747369:#f2777a:#99cc99:#ffcc66:#6699cc:#cc99cc:#66cccc:#f2f0ec"
    scrollback_infinite = True
    show_titlebar = False
    use_system_font = False
```