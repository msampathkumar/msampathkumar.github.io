# Setting Up GUI and Chrome Remote Desktop on Google Cloud VM

In this guide, you will learn how to set up a graphical user interface (GUI) on your Google Cloud VM and configure Google Chrome Remote Desktop to access the VM desktop securely from your personal computer.

To understand how to provision the VM with the required IAM roles and scopes, see:
[google-cloud-vm-for-agentic-coding-harness-experiments.md](google-cloud-vm-for-agentic-coding-harness-experiments.md)

## Prerequisites

1. A local computer (Mac, Linux, or Windows) with Google Chrome installed.
2. A Google Compute Engine VM running Debian or Ubuntu.

## Compute VM Setup

> **Note:** If you are running these commands interactively in an SSH session, omit steps 1 and 9 from the script below. Otherwise, add this script to your Compute VM's startup script metadata.

To set up a GUI on the VM, shut down the instance and add the following script to the VM metadata as a startup script. In this setup, we use `XFCE` as a lightweight GUI for the remote desktop connection. The script creates a flag file to ensure it executes only once.

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

If you configure this as a startup script, it may take 5–10 minutes to complete during the initial boot. Once logged in via SSH, verify completion by checking for the flag file:

```bash
ls -l /var/log/workstation_setup_complete.flag
```

## (Optional) PyEnv Build Dependencies Setup

If you plan to build Python versions using `pyenv`, install the [suggested build dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment):

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev curl git \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
  libffi-dev liblzma-dev libzstd-dev
```

## Remote Desktop Setup

### Step 1: Authorize from Your Local Computer

1. In Chrome on your local computer, navigate to: https://remotedesktop.google.com/headless
2. Locate the section titled **"Set up via SSH"** (or "Set up another computer").
3. Click **Begin**, then **Next**, and then **Authorize** (ensure you are signed into the Google account you intend to use).
4. Copy the generated authorization command for Debian/Linux. It will resemble:

```bash
DISPLAY= /opt/google/chrome-remote-desktop/start-host --code="4/aXo............................" --redirect-url="https://remotedesktop.google.com/_/oauthredirect" --name=$(hostname)
```

### Step 2: Run the Authorization Command on the Compute Engine VM

1. Connect to the VM via SSH.
2. Paste and run the command copied from Step 1.
3. When prompted, enter a 6-digit PIN to secure your Remote Desktop connection.

### Step 3: Connect from Your Local Computer

1. In Chrome on your local computer, navigate to: https://remotedesktop.google.com/access
2. You will see your VM listed under available remote devices.
3. Click on the VM and enter your 6-digit PIN to launch the desktop session.

---

That's it! In this guide, you learned how to configure an XFCE desktop environment and access your Google Cloud VM through Chrome Remote Desktop.

Happy Coding!