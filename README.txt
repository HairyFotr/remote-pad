Install:
sudo apt install libudev-dev libevdev-dev evtest python3-dev
sudo modprobe uinput
echo 'KERNEL=="uinput", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-uinput.rules
sudo udevadm control --reload-rules
sudo usermod -aG input $USER

Log out and in
Or use this for the current shell:
newgrp input
Or set the permissions to 666


python -m venv env
. env/bin/activate
python -m pip install -r requirements.txt


Receiver should open port 8888/udp on firewall and/or router

Optional:
Testing is possible using qjoypad

