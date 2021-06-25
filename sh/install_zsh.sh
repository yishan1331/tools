#!/bin/sh
echo "\033[44;37m --------------------------------安裝Zsh-------------------------------- \033[0m"
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install zsh
sudo apt-get install powerline
sudo apt-get -y install fonts-powerline
echo "\033[44;37m --------------------------------安裝oh-my-zsh-------------------------------- \033[0m"
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
echo "\033[44;37m --------------------------------下載bullet-train.zsh-theme與配置-------------------------------- \033[0m"
wget https://raw.githubusercontent.com/caiogondim/bullet-train-oh-my-zsh-theme/master/bullet-train.zsh-theme
mv bullet-train.zsh-theme .oh-my-zsh/themes
sudo sed -i '11s/robbyrussell/bullet-train/' ~/.zshrc
sudo sed -i '11a\\n#Yishan add for theam setting -> bullet-train\nBULLETTRAIN_PROMPT_ORDER=(\n#time\nstatus\ncustom\ncontext\ndir\nscreen\nperl\nruby\nvirtualenv\n#nvm\naws\ngo\nrust\nelixir\ngit\nhg\ncmd_exec_time\n)' ~/.zshrc
sudo sed -i '48s/# DISABLE_AUTO_UPDATE/DISABLE_AUTO_UPDATE/' ~/.zshrc
echo "\033[44;37m --------------------------------下載zsh-syntax-highlighting&zsh-autosuggestions與配置-------------------------------- \033[0m"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
sudo sed -i '92s/plugins=(git)/plugins=(\ngit\nzsh-syntax-highlighting\nzsh-autosuggestions\n)/' ~/.zshrc
echo "export TERM=xterm-256color" >> ~/.zshrc
echo "ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=10'" >> ~/.zshrc
echo '
# Yishan add for Fix numeric keypad 預設一進入小鍵盤就能使用
bindkey -s "^[Op" "0"
bindkey -s "^[On" "."
bindkey -s "^[OM" "^M"
bindkey -s "^[Oq" "1"
bindkey -s "^[Or" "2"
bindkey -s "^[Os" "3"
bindkey -s "^[Ot" "4"
bindkey -s "^[Ou" "5"
bindkey -s "^[Ov" "6"
bindkey -s "^[Ow" "7"
bindkey -s "^[Ox" "8"
bindkey -s "^[Oy" "9"
bindkey -s "^[Ol" "+"
bindkey -s "^[Om" "-"
bindkey -s "^[Oj" "*"
bindkey -s "^[Oo" "/"
' >> ~/.zshrc
source ~/.zshrc
echo "\033[44;37m --------------------------------完成-------------------------------- \033[0m"