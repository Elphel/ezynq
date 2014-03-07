#!/bin/bash
#***************************************************************************
# FILE NAME  : install_uboot.sh
# DESCRIPTION: gets xilinx's u-boot and merges with ezynq
# AUTHOR: Oleg Dzhimiev <oleg@elphel.com>
# Copyright (C) 2013 Elphel, Inc
# -----------------------------------------------------------------------------**
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The four essential freedoms with GNU GPL software:
#  * to run the program for any purpose
#  * to study how the program works and change it to make it do what you wish
#  * to redistribute copies so you can help your neighbor
#  * to distribute copies of your modified versions to others
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------**

#get the current script path
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

#constants
UBOOT_TREE="$SCRIPTPATH/u-boot-tree"
CONFIGS="include/configs"
EZYNQ="ezynq"
REPO_DIR_NAME="u-boot-xlnx"
PATCH_NAME="u-boot-xlnx.patch"

SUFFIX=".orig"

INITENV="initenv"
OVERWRITE_INITENV=1
CROSS_COMPILE="arm-poky-linux-gnueabi-"
COMPILE_PATH="/opt/poky/1.4.2/sysroots/x86_64-pokysdk-linux/usr/bin/armv7a-vfp-neon-poky-linux-gnueabi"

echo "Step 1: Cloning Xilinx's u-boot repository (master-next branch)"
if [ ! -d "$REPO_DIR_NAME/.git" ]; then
  git clone -b master-next https://github.com/Xilinx/u-boot-xlnx.git "$REPO_DIR_NAME"
else
  echo "  Already there"
fi

echo "Step 2: Checking out u-boot version with the hash 'bbd91fc9ae290c31dc52fd8322f43f67ddd39247'"
cd "$REPO_DIR_NAME"
git checkout 54fee227ef141214141a226efd17ae0516deaf32

echo "Step 3: Merging ezynq with u-boot"

echo "Step 3a: Creating symbolic link for the root folder"
if [ ! -h $EZYNQ ]; then
  ln -s $SCRIPTPATH $EZYNQ
fi

echo "Step 3b: Creating symbolic link for the 'ezynq' folder"
if [ ! -h "$CONFIGS/$EZYNQ" ]; then
  ln -s "$UBOOT_TREE/$CONFIGS/$EZYNQ" $CONFIGS
fi

echo "Step 3c: Creating symbolic links for separate files (a suffix is added to the originals)"
if [ ! -d "board/elphel" ]; then 
  mkdir "board/elphel"
fi
if [ ! -d "board/elphel/elphel393" ]; then 
  mkdir "board/elphel/elphel393"
fi
for SRC in $(find $UBOOT_TREE -type f -not -path "$UBOOT_TREE/$CONFIGS/$EZYNQ/*")
do
  LINK=$(echo $SRC | sed "s:^$UBOOT_TREE/::")
  #echo "$SRC | $LINK"
  if [ ! -h $LINK ]; then
    ln -s -S $SUFFIX $SRC $LINK
  fi
done

# echo "Step 3b: Creating a patch file"
# cd ..
# if [ ! -f $PATCH_NAME ]; then
#   diff -rubPB "$REPO_DIR_NAME" "$UBOOT_TREE" > "$PATCH_NAME"
# fi
# 
# echo "Step 3c: Applying the patch"
# cd "$REPO_DIR_NAME"
# patch -r - -Np1 < "../$PATCH_NAME"
# chmod +x makeuboot

echo "Step 4: Creating initenv script"
if [ -f $INITENV ]; then
    read -p "Overwrite an already existing initenv? (y/n) " yn
    if [ ! $yn = "y" ]; then
      OVERWRITE_INITENV=0;
    fi
fi

if [ $OVERWRITE_INITENV = 1 ] ; then
  echo "#!/bin/sh
export CROSS_COMPILE=$CROSS_COMPILE
export PATH=$COMPILE_PATH/:\$PATH" > $INITENV
fi

if [ ! -d $COMPILE_PATH ] ; then
  echo "  WARNING: Please update initenv with your cross compiler path"
fi

echo "DONE. 
FURTHER INSTRUCTIONS (TO GENERATE BOOT.BIN):
  cd u-boot-xlnx
  ./makeuboot <target> 

SUPPORTED TARGETS:
  ./makeuboot zynq_microzed_config
  ./makeuboot zynq_zc706_config
  ./makeuboot elphel393_config 
  ./makeuboot zynq_zed_config "
