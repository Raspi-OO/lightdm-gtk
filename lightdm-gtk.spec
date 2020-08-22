Name:           lightdm-gtk
Version:        2.0.7
Summary:        LightDM GTK Greeter
Release:        1
License:        GPLv3+
URL:            https://launchpad.net/lightdm-gtk-greeter
Source0:        %url/2.0/%{version}/+download/lightdm-gtk-greeter-%{version}.tar.gz

Source1:        60-lightdm-gtk-greeter.conf
Patch0:         fix_arm_compile.patch
Patch1:         lightdm-gtk_add-language-button-to-layout.patch

# tweak default config

## upstreamable patches
# https://bugzilla.redhat.com/show_bug.cgi?id=1178498
# (lookaside cache)
Patch2:         lightdm-gtk-greeter-1.8.5-add-cinnamon-badges.patch

BuildRequires:  gettext
BuildRequires:  intltool
# exo-csource
BuildRequires:  exo-devel
BuildRequires:  pkgconfig(liblightdm-gobject-1)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  gobject-introspection-devel

Obsoletes:      lightdm-gtk2 < 1.8.5-15

Obsoletes:      lightdm-gtk-common < 2.0
Obsoletes:      lightdm-gtk-greeter < 1.1.5-4
Provides:       lightdm-gtk-greeter = %{version}-%{release}
Provides:       lightdm-greeter = 1.2

Requires:       lightdm%{?_isa}

# owner of HighContrast gtk/icon themes
Requires:       gnome-themes-standard

# Fix issue with lightdm-autologin-greeter pulled in basic-desktop netinstall.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1481192
Supplements: (lightdm%{?_isa} and lightdm-autologin-greeter)

%description
A LightDM greeter that uses the GTK3 toolkit.


%prep
%autosetup -n lightdm-gtk-greeter-%{version} -p1

%if 0%{?background:1}
sed -i.background -e "s|#background=.*|background=%{background}|" \
  data/lightdm-gtk-greeter.conf
%endif


%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --disable-libindicator \
  --enable-at-spi-command="%{_libexecdir}/at-spi-bus-launcher --launch-immediately" \
  --enable-kill-on-sigterm

%make_build


%install
%make_install

install -m644 -p -D %{SOURCE1} \
  %{buildroot}%{_datadir}/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf

%find_lang lightdm-gtk-greeter

# create/own GREETER_DATA_DIR
mkdir -p %{buildroot}%{_datadir}/lightdm-gtk-greeter/

## unpackaged files
rm -fv %{buildroot}%{_docdir}/lightdm-gtk-greeter/sample-lightdm-gtk-greeter.css


%pre
%{_sbindir}/update-alternatives \
  --remove lightdm-greeter \
  %{_datadir}/xgreeters/lightdm-gtk-greeter.desktop 2> /dev/null ||:


%files -f lightdm-gtk-greeter.lang
%license COPYING
%doc ChangeLog NEWS README
%doc data/sample-lightdm-gtk-greeter.css
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_sbindir}/lightdm-gtk-greeter
%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop
%dir %{_datadir}/lightdm-gtk-greeter/
%{_datadir}/icons/hicolor/scalable/places/*badge-symbolic.svg
%{_datadir}/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf


%changelog
* Fri Sep 25 2020 Luke Yue <lukedyue@gmail.com> - 2.0.7-1
- Initial package
