Name:    xdg-desktop-portal
Version: 1.0.2
Release: 1%{?dist}
Summary: Portal frontend service to flatpak

License: LGPLv2+
URL:     https://github.com/flatpak/xdg-desktop-portal/
Source0: https://github.com/flatpak/xdg-desktop-portal/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: pkgconfig(flatpak)
BuildRequires: pkgconfig(fuse)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: /usr/bin/xmlto
BuildRequires: gcc
%{?systemd_requires}
BuildRequires: systemd
Requires:      dbus
# Required version due to the move of the document portal.
Requires:      flatpak >= 0.11.1
# Required for the document portal.
Requires:      /usr/bin/fusermount

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
%configure --enable-docbook-docs --disable-pipewire --docdir=%{_pkgdocdir}
%make_build


%install
%make_install
install -dm 755 %{buildroot}/%{_pkgdocdir}
install -pm 644 README.md %{buildroot}/%{_pkgdocdir}
# This directory is used by implementations such as xdg-desktop-portal-gtk.
install -dm 755 %{buildroot}/%{_datadir}/%{name}/portals

%find_lang %{name}


%post
%systemd_user_post %{name}.service
%systemd_user_post xdg-document-portal.service
%systemd_user_post xdg-permission-store.service


%preun
%systemd_user_preun %{name}.service
%systemd_user_preun xdg-document-portal.service
%systemd_user_preun xdg-permission-store.service


%files -f %{name}.lang
%doc %{_pkgdocdir}
%license COPYING
%{_datadir}/dbus-1/interfaces/org.freedesktop.portal.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.impl.portal.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.portal.Desktop.service
%{_datadir}/dbus-1/services/org.freedesktop.portal.Documents.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.PermissionStore.service
%{_datadir}/%{name}
%{_libexecdir}/xdg-desktop-portal
%{_libexecdir}/xdg-document-portal
%{_libexecdir}/xdg-permission-store
%{_userunitdir}/%{name}.service
%{_userunitdir}/xdg-document-portal.service
%{_userunitdir}/xdg-permission-store.service

%files devel
%{_datadir}/pkgconfig/xdg-desktop-portal.pc


%changelog
* Wed Sep 12 2018 David King <dking@redhat.com> - 1.0.2-1
- Rebase to 1.0.2 (#1570030)

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
