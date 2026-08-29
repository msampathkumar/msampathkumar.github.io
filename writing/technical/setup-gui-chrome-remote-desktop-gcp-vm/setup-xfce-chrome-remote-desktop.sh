#!/bin/bash
# ==============================================================================
# Setup GUI (XFCE4) & Chrome Remote Desktop on Google Cloud Compute Engine
# Repository: https://github.com/msampathkumar/msampathkumar.github.io
# Documentation: https://msampathkumar.github.io/writing/technical/setup-gui-chrome-remote-desktop-gcp-vm/
#
# NOTE: Please review this script before running. It installs desktop packages,
# disables local display managers for headless operation, and configures Chrome
# Remote Desktop. Must be executed with root/sudo privileges.
# ==============================================================================

set -euo pipefail

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "[-] Error: This script must be run as root or with sudo privileges." >&2
    echo "    Usage: sudo bash setup-xfce-chrome-remote-desktop.sh" >&2
    exit 1
fi

FLAG_FILE="/var/log/workstation_setup_complete.flag"

# 1. Check if the setup has already been completed
if [ -f "$FLAG_FILE" ]; then
    echo "[+] Setup was already completed previously (/var/log/workstation_setup_complete.flag exists)."
    echo "[+] Booting normally."
    exit 0
fi

echo "[*] Starting Google Cloud VM GUI & Chrome Remote Desktop setup..."

# 2. Update system packages
echo "[*] Updating apt package repositories..."
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

# 3. Install XFCE4 desktop environment (lightweight for cloud VMs)
echo "[*] Installing XFCE4 and desktop base..."
DEBIAN_FRONTEND=noninteractive apt-get install -y xfce4 desktop-base

# 4. Configure Chrome Remote Desktop to use XFCE session
echo "[*] Configuring Chrome Remote Desktop session for XFCE..."
bash -c 'echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session'

# 5. Download and install Chrome Remote Desktop host package
echo "[*] Downloading and installing Chrome Remote Desktop host..."
wget -q https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
apt-get install -y --fix-broken ./chrome-remote-desktop_current_amd64.deb
rm -f ./chrome-remote-desktop_current_amd64.deb

# 6. Download and install Google Chrome browser
echo "[*] Downloading and installing Google Chrome browser..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y --fix-broken ./google-chrome-stable_current_amd64.deb
rm -f ./google-chrome-stable_current_amd64.deb

# 7. Disable the local display manager since the VM runs headless in the cloud
echo "[*] Disabling lightdm (headless cloud VM)..."
systemctl disable lightdm.service 2>/dev/null || true

# 8. Install essential developer utilities
echo "[*] Installing basic developer utilities (git, vim, gedit, tree)..."
apt-get install -y --fix-broken git vim gedit tree

# 9. Mark setup as complete so startup scripts won't re-run this
touch "$FLAG_FILE"

echo "[✓] GUI & Chrome Remote Desktop installation complete!"
echo "[*] Next step: Generate your auth code at https://remotedesktop.google.com/headless and run it on this VM."
