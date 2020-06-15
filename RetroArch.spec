%global appstream_id org.libretro.%{name}
%global optflags %{optflags} -flto
%global build_ldflags %{build_ldflags} -flto

Name:           RetroArch
Version:        1.8.8
Release:        1%{?dist}
Summary:        Cross-platform, sophisticated frontend for the libretro API
License:        GPLv3+ and GPLv2 and CC-BY and CC0 and BSD and ASL 2.0 and MIT
URL:            https://www.libretro.com/

Source0:        https://github.com/libretro/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# https://github.com/flathub/org.libretro.RetroArch/blob/master/org.libretro.RetroArch.appdata.xml
# Repository does not have all tags/releases, master contains the last released version:
Source1:        https://raw.githubusercontent.com/flathub/org.libretro.%{name}/master/org.libretro.%{name}.appdata.xml

BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  libv4l-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  mbedtls-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  pkgconfig(caca)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(miniupnpc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(Qt5Concurrent) >= 5.2
BuildRequires:  pkgconfig(Qt5Core) >= 5.2
BuildRequires:  pkgconfig(Qt5Gui) >= 5.2
BuildRequires:  pkgconfig(Qt5Network) >= 5.2
BuildRequires:  pkgconfig(Qt5Widgets) >= 5.2
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  systemd-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

# Required at runtime:
Requires:       perl(Net::DBus)
Requires:       perl(X11::Protocol)

Provides:       bundled(7zip) = 9.20
Provides:       bundled(discord-rpc)
Provides:       bundled(dr)
Provides:       bundled(ibxm)
# https://github.com/libretro/RetroArch/issues/8153
# https://github.com/RetroAchievements/rcheevos/issues/15
Provides:       bundled(lua) = 5.3.5
Provides:       bundled(rcheevos) = 7.0.2
Provides:       bundled(SPIRV-Cross)
Provides:       bundled(stb)

# Lowercase provide
Provides:       retroarch

%description
libretro is an API that exposes generic audio/video/input callbacks. A frontend
for libretro (such as %{name}) handles video output, audio output, input and
application lifecycle. A libretro core written in portable C or C++ can run
seamlessly on many platforms with very little to no porting effort.

While %{name} is the reference frontend for libretro, several other projects
have used the libretro interface to include support for emulators and/or game
engines. libretro is completely open and free for anyone to use.

%prep
%autosetup -p1

# Remove bundles
pushd deps
rm -rf \
    glslang \
    libfat \
    libFLAC \
    libiosuhax \
    libvita2d \
    libz \
    miniupnpc \
    peglib \
    pthreads \
    wayland-protocols
popd

%build
%set_build_flags
# Not an autotools configure script:
./configure \
    --disable-builtinflac \
    --disable-builtinglslang \
    --disable-builtinmbedtls \
    --disable-builtinminiupnpc \
    --disable-builtinzlib \
    --prefix=%{_prefix}

%make_build

%install
%make_install
install -p -m 0644 -D %{SOURCE1} %{buildroot}%{_metainfodir}/%{appstream_id}.appdata.xml

# Let RPM pick up docs in the files section
rm -fr %{buildroot}%{_docdir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/retroarch.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.appdata.xml

%files
%license COPYING
%doc CHANGES.md CONTRIBUTING.md README-exynos.md README-mali_fbdev_r4p0.md README.md README-OMAP.md
%{_bindir}/retroarch
%{_bindir}/retroarch-cg2glsl
%{_datadir}/applications/retroarch.desktop
%{_datadir}/pixmaps/retroarch.svg
%{_mandir}/man6/retroarch.6*
%{_mandir}/man6/retroarch-cg2glsl.6*
%{_metainfodir}/%{appstream_id}.appdata.xml
%config %{_sysconfdir}/retroarch.cfg

%changelog
* Mon Jun 15 2020 Simone Caronni <negativo17@gmail.com> - 1.8.8-1
- Update to 1.8.8.

* Sun Mar 29 2020 Simone Caronni <negativo17@gmail.com> - 1.8.5-1
- First build, pick some stuff from RPMFusion.
