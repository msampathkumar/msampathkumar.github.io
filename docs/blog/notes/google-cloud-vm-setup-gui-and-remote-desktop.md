# google-cloud-vm-setup-gui-and-remote-desktop.md

In this blog post, you will learn how to set up a graphical user interface in your Google Cloud VM and how to set up Google Chrome remote desktop for accessing the VM from your personal laptop. To understand how to set up your Google Cloud VM, check the blog post below.

[google-cloud-vm-for-agentic-coding-harness-experiments.md](google-cloud-vm-for-agentic-coding-harness-experiments.md)

Prequired

1. personal pc - i am using Mac book
2. google compute ubuntu vm

# Compute VM Setup

> **Note:** If you are manually running these commands, comment 1 and 9 from the script below. Otherwise add this script to your Compute VM's startup script.

To setup a GUI in VM, I have shutdown VM and added following script to it's startup script. In this setup I use `XFCE` as the GUI for our remote deskopt connection. I have also setup necessary placeholder to ensure that this script run one time.

You may either do the same or run below command from 2 to 8. Commenting 1 and 9.

```bash
#!/bin/bash

# 1. Check if the setup has already been completed
FLAG_FILE="/var/log/workstation_setup_complete.flag"

if [ -f "$FLAG_FILE" ]; then
    echo "Setup already ran previously. Booting normally."
    exit 0
fi

# ==========================================
# FIRST TIME SETUP RUNS BELOW THIS LINE
# ==========================================

# 2. Update system packages
apt-get update
apt-get upgrade -y

# 3. Install XFCE (a lightweight, fast GUI for cloud servers)
DEBIAN_FRONTEND=noninteractive apt-get install -y xfce4 desktop-base

# 4. Tell Chrome Remote Desktop to use XFCE
bash -c 'echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session'

# 5. Download and install Chrome Remote Desktop
wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
apt-get install -y --fix-broken ./chrome-remote-desktop_current_amd64.deb

# 6. Download and install Google Chrome browser inside the VM
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y --fix-broken ./google-chrome-stable_current_amd64.deb

# 7. Disable the local display manager since we are running headless
systemctl disable lightdm.service

# 8. Install basic user utils
apt-get install -y --fix-broken git vim gedit tree

# ==========================================
# 9. Mark setup as complete so this never runs again
touch "$FLAG_FILE"
```

If you are using this script as os start up script, then it may take some time for these commands to completed. May be take 10-15 min for coffee break. Once you login to VM, you find `/var/log/workstation_setup_complete.flag` to confirm if the setup is done.

# (Optional) PyEnv Build dependencies setup

If you plan to use this VM for long time, you may need [additional packages](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) for pyenv setup.

```bash
sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libzstd-dev
```

# Remote deskopt setup

## step1: Personal PC

In Chrome, go to https://remotedesktop.google.com/headless and look for `SetUp via SSH`.

You have a "Ubuntu Command" shared in page titled "Set up another computer"

Click Begin, then click Next, and finally click Authorize (make sure you are signed into the Google account you want to use for work).

DISPLAY= /opt/google/chrome-remote-desktop/start-host --code="4/aXo............................" --redirect-url="https://remotedesktop.google.com/_/oauthredirect" --name=$(hostname)


## step 2: Compute VM

In SSH Shell, pass your code to it.

It will ask you to setup a 6 digit pin code to be passcode for your Remote Desktop


## setp 3: Personal PC

In Chrome, go to https://remotedesktop.google.com/access
You will find that your `ComputeVM` is already added here.
Click it and provide the 6 digit pin to login to the VM

## step 4: 

This is the most important part of this tutorial. You must do this step within 2 min.

Say `Yay! I did it.` :)


---

That it! In this post, you learned how to setup GUI and remote desktop for your Google Cloud VM.

Happy Coding!