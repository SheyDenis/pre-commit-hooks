# Colors for pretty printing stuff.
NC='\033[0m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
WHITE='\033[1;37m'
YELLOW='\033[1;33m'

function __echo_color() {
  color="${1}"
  shift
  echo -e "${color}${@}\033[0m"
}

function echo_error() {
  __echo_color ${RED} ${@}
}

function echo_warning() {
  __echo_color ${YELLOW} ${@}
}

function echo_info() {
  __echo_color ${NC} ${@}
}

function echo_debug() {
  __echo_color ${BLUE}"[DEBUG]" ${NC} ${@}
}
