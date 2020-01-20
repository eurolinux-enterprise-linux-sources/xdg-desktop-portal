Name:    xdg-desktop-portal
Version: 0.5
Release: 2%{?dist}
Summary: Portal frontend service to flatpak

License: LGPLv2+
URL:     https://github.com/flatpak/xdg-desktop-portal/
Source0: https://github.com/flatpak/xdg-desktop-portal/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: pkgconfig(flatpak)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: /usr/bin/xmlto
Requires:      dbus

%description
xdg-desktop-portal works by exposing a series of D-Bus interfaces known as
portals under a well-known name (org.freedesktop.portal.Desktop) and object
path (/org/freedesktop/portal/desktop). The portal interfaces include APIs for
file access, opening URIs, printing and others.

%package  devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The pkg-config file for %{name}.


%prep
%setup -q


%build
# Generate consistent IDs between runs to avoid multilib problems.
export XMLTO_FLAGS="--stringparam generate.consistent.ids=1"
%configure --enable-docbook-docs
%make_build


%install
%make_install
install -dm 755 %{buildroot}/%{_pkgdocdir}
install -pm 644 README.md %{buildroot}/%{_pkgdocdir}
# This directory is used by implementations such as xdg-desktop-portal-gtk.
install -dm 755 %{buildroot}/%{_datadir}/%{name}/portals

if test -d %{buildroot}/%{_docdir}/%{name}; then
    mv %{buildroot}/%{_docdir}/%{name}/* %{buildroot}/%{_pkgdocdir}
    rmdir %{buildroot}/%{_docdir}/%{name}/
fi

%find_lang %{name}


%files -f %{name}.lang
%doc %{_pkgdocdir}
%license COPYING
%{_libexecdir}/xdg-desktop-portal
%{_datadir}/dbus-1/interfaces/org.freedesktop.portal.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.impl.portal.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.portal.Desktop.service
%{_datadir}/%{name}

%files devel
%{_libdir}/pkgconfig/xdg-desktop-portal.pc


%changelog
* Fri Mar 10 2017 David King <dking@redhat.com> - 0.5-2
- Fix multilib issues with XML-based documentation

* Wed Jan 18 2017 David King <amigadave@amigadave.com> - 0.5-1
- Update to 0.5

* Thu Dec 01 2016 David King <amigadave@amigadave.com> - 0.4-1
- Update to 0.4

* Fri Sep 02 2016 David King <amigadave@amigadave.com> - 0.3-1
- Update to 0.3

* Fri Jul 29 2016 David King <amigadave@amigadave.com> - 0.2-1
- Update to 0.2 (#1361575)

* Tue Jul 12 2016 David King <amigadave@amigadave.com> - 0.1-2
- Own the portals directory

* Mon Jul 11 2016 David King <amigadave@amigadave.com> - 0.1-1
- Initial Fedora packaging
