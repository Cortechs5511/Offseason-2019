set -e
PACKAGES=()
DO_INSTALL=0
if ! opkg list-installed | grep -F 'python37 - 3.7.2-r0'; then
    PACKAGES+=("opkg_cache/python37_3.7.2-r0_cortexa9-vfpv3.ipk")
    DO_INSTALL=1
else
    echo "python37 already installed"
fi
if ! opkg list-installed | grep -F 'python37-robotpy-ctre - 2019.3.0'; then
    PACKAGES+=("opkg_cache/python37-robotpy-ctre_2019.3.0_cortexa9-vfpv3.ipk")
    DO_INSTALL=1
else
    echo "python37-robotpy-ctre already installed"
fi
if [ "${DO_INSTALL}" == "0" ]; then
    echo "No packages to install."
else
    opkg install  ${PACKAGES[@]}
fi