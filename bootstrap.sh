#!/bin/bash

set -euo pipefail

export PACMAN_USER="pacman"

USER_NAMES=(
  "ansible"
  "adrien"
)

PACKAGE_NAMES=(
  #"ansible"
  "avahi"
  "openssh"
)

AUR_SNAPSHOT_URLS=(
  #"https://aur.archlinux.org/cgit/aur.git/snapshot/cloud-init.tar.gz"
)

SERVICES_NAMES=(
  "avahi-daemon"
  "sshd"
)

set_user_as_sudoer_with_no_password()
{
  declare user_name="${1}"
  cat <<EOCAT >"/etc/sudoers.d/${user_name}"
Defaults:${user_name} !requiretty
Defaults:${user_name} env_keep += "PATH"
${user_name} ALL=(ALL) NOPASSWD:ALL
EOCAT
}

add_users()
{
  if [[ "${#USER_NAMES[@]}" -gt 0 ]]; then
    declare user_name=
    for user_name in "${USER_NAMES[@]}"; do
      useradd --shell "/bin/bash" "${user_name}"
      set_user_as_sudoer_with_no_password "${user_name}"
    done
  fi
}

setup_ansible()
{
  :
}

is_package_installed()
{
  declare package_name="${1}"
  pacman -Q | cut -d" " -f1 | grep -qE "^${package_name}$"
}

setup_pacman()
{
  pacman-key --init
  pacman-key --populate "archlinuxarm"
  #pacman -Syu --noconfirm

  useradd --system --shell "/usr/bin/nologin" "${PACMAN_USER}"
  pacman --sync "base-devel" "git" "sudo" "wget" --noconfirm --needed
  set_user_as_sudoer_with_no_password "${PACMAN_USER}"
}

install_official_packages()
{
  declare package_name=
  for package_name in "${PACKAGE_NAMES[@]}"; do
    if ! is_package_installed "${package_name}"; then
      pacman --sync "${package_name}" --noconfirm --needed
    fi
  done
}

install_aur_packages()
{
  declare aur_snapshot_url=
  declare package_name=
  if [[ "${AUR_SNAPSHOT_URLS[*]}" -gt 0 ]]; then
    for aur_snapshot_url in "${AUR_SNAPSHOT_URLS}"; do
      package_name="$( basename "${aur_snapshot_url}" ".tar.gz" )"
      if ! is_package_installed "${package_name}"; then
        sudo -u "${PACMAN_USER}" mkdir -p "/tmp/${package_name}"
        cd "/tmp/${package_name}"
          sudo -u "${PACMAN_USER}" -- \
            "wget '${aur_snapshot_url}' -O './${temp_folder_name}.tar.gz' && \
             tar -xvf './${package_name}.tar.gz' --strip 1 && \
             makepkg --syncdeps --install --noconfirm"
        cd -
      fi
    done
  fi
}

enable_services()
{
  declare service_name=
  for service_name in "${SERVICES_NAMES[@]}"; do
    systemctl enable "${service_name}.service"
  done
}

setup_sshd()
{
  sed -ie 's,#\?PermitRootLogin .*$,PermitRootLogin yes,g' "/etc/ssh/sshd_config"
}

install_packages()
{
  install_official_packages
  install_aur_packages
}

main()
{
  setup_pacman
  install_packages
  add_users
  enable_services
  setup_ansible
  setup_sshd
}

main "${@}"
