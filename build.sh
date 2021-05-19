#!/bin/bash

rm -rf build
mkdir -p build
pushd build > /dev/null
~/soft/android-studio/jre/bin/javac\
	-classpath ~/Android/Sdk/platforms/android-26/android.jar\
	-d .\
	../src/main/java/com/makepad/hello_quest/*.java
~/Android/Sdk/build-tools/31.0.0-rc3/dx --dex --output classes.dex .
mkdir -p lib/arm64-v8a
pushd lib/arm64-v8a > /dev/null
/home/mirmik/Android/Sdk/ndk/22.1.7171670/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android26-clang\
    -march=armv8-a\
    -shared\
    -I ~/Android/Sdk/ndk/22.1.7171670/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/\
    -I ~/src/ovr_sdk_mobile_1.45.0/VrApi/Include\
    -L ~/Android/Sdk/ndk/22.1.7171670/platforms/android-26/arch-arm64/usr/lib\
    -L ~/src/ovr_sdk_mobile_1.45.0/VrApi/Libs/Android/arm64-v8a/Debug\
    -landroid\
    -llog\
    -lvrapi\
    -o libmain.so\
   ../../../src/main/cpp/*.c
cp ~/src/ovr_sdk_mobile_1.45.0/VrApi/Libs/Android/arm64-v8a/Debug/libvrapi.so .
popd > /dev/null
aapt\
	package\
	-F hello_quest.apk\
	-I ~/Android/Sdk/platforms/android-26/android.jar\
	-M ../src/main/AndroidManifest.xml\
	-f
aapt add hello_quest.apk classes.dex
aapt add hello_quest.apk lib/arm64-v8a/libmain.so
aapt add hello_quest.apk lib/arm64-v8a/libvrapi.so
apksigner\
	sign\
	-ks ~/.android/debug.keystore\
	--ks-key-alias androiddebugkey\
	--ks-pass pass:android\
	hello_quest.apk
popd > /dev/null
