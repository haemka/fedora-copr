%global debug_package %{nil}
%global __requires_exclude_from plugins/.*/(.*-aarch64/.*\.so|.*/bin/.*\.js)$

Name:           pycharm-professional
Version:        2022.2.1
Release:        1%{?dist}
Summary:        The Python IDE for Professional Developers
License:        custom
URL:            https://www.jetbrains.com/pycharm/
Source0:        https://download.jetbrains.com/python/pycharm-professional-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/haemka/fedora-copr/main/pycharm-professional/pycharm-professional.desktop

BuildRequires: pkg-config desktop-file-utils

%description
The Python IDE for Professional Developers.

%prep
%autosetup -n pycharm-%{version} -p1

# Replace python shebangs to make them compatible with fedora
find -type f -name "*.py" -exec sed -e 's|/usr/bin/env python|%{__python3}|g' \
                                    -i "{}" \;

find -type f -name "*.sh" -exec sed -e 's|/bin/sh|/usr/bin/sh|g' \
                                    -i "{}" \;

# Remove files for other CPU architectures
%{__rm} -rf lib/pty4j-native/linux/aarch64
%{__rm} -rf lib/pty4j-native/linux/arm
%{__rm} -rf lib/pty4j-native/linux/mips64el
%{__rm} -rf lib/pty4j-native/linux/ppc64le

# remove bundled jre
%{__rm} -rf jbr

%build

%install
%{__mkdir} -p %{buildroot}/opt/%{name}
cp -a * %{buildroot}/opt/%{name}

%{__install} -pDm644 bin/pycharm.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{__install} -pDm644 bin/pycharm.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%{__install} -pDm644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
ln -s -f /opt/%{name}/bin/pycharm.sh %{_bindir}/pycharm

%postun
%{__rm} -f %{_bindir}/pycharm

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%dir /opt/%{name}
/opt/%{name}/*

%changelog
