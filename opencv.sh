#!/usr/bin/env bash
# see
# http://docs.opencv.org/master/dd/dd5/tutorial_py_setup_in_fedora.html
#


set -x

clean="clean"
clean="no"

dnf="dnf"
dnf="no"

git="git"
git="no"

cd ~

if [ "$clean" = "clean" ]; then
    sudo rm -rf opencv-install
    mkdir opencv-install
fi

if [ "$dnf" = "dnf" ]; then
    sudo dnf -y install cmake
    sudo dnf -y install python3
    sudo dnf -y install python3-devel
    sudo dnf -y install python3-numpy
    sudo dnf -y install gcc
    sudo dnf -y install gcc-c++
    sudo dnf -y install libpng-devel
    sudo dnf -y install libjpeg-turbo-devel
    sudo dnf -y install jasper-devel
    sudo dnf -y install openexr-devel
    sudo dnf -y install libtiff-devel
    sudo dnf -y install libwebp-devel
    sudo dnf -y install gtk2-devel
    sudo dnf -y install libdc1394-devel
    sudo dnf -y install libv4l-devel
    sudo dnf -y install ffmpeg-devel
    sudo dnf -y install gstreamer-plugins-base-devel
    sudo dnf -y install tbb-devel
    sudo dnf -y install eigen3-devel
    sudo dnf -y install python-sphinx
    sudo dnf -y install texlive
    sudo dnf -y install git
fi


cd opencv-install

if [ "$git" = "git" ]; then
    git clone --progress https://github.com/Itseez/opencv.git
fi

cd opencv
sudo rm -rf build
mkdir build
cd build

python3-config --config --prefix --exec-prefix --includes --libs --cflags --ldflags --extension-suffix --help --abiflags --configdir--
uname -a

#-D CMAKE_INSTALL_PREFIX=/usr/local/myopencv BUILD_DOCS=ON -D BUILD_TESTS=ON -D BUILD_PERF_TESTS=ON -D BUILD_EXAMPLES=ON ..
cmake -D CMAKE_BUILD_TYPE=RELEASE -D BUILD_opencv_python2=OFF -D BUILD_opencv_java=OFF -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") -D PYTHON_EXECUTABLE=$(which python3) ..

make -j3
sudo make install
#make docs
#make html_docs