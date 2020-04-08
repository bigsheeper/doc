###1. 设置下次重启后的模式（关掉图形界面）
`sudo systemctl set-default multi-user.target`

###2.重启电脑

###3.Ctrl + Alt + F1进入命令行界面

###4.卸载NVIDIA driver
- 如果原先的驱动是通过apt安装
`sudo apt-get remove --purge nvidia*`
- 如果原先的驱动是run file安装
`sudo sh old.driver.filename.run --uninstall`

###5.安装NVIDA driver
` sudo sh new.driver.filename.run`

###6.nvidia-smi检验是否安装成功

###7.设置下次重启后的模式（打开图形界面）
`sudo systemctl set-default graphical.target`

###8.重启电脑