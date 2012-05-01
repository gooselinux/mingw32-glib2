%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}
%global _use_internal_dependency_generator 0
%global __find_requires %{_mingw32_findrequires}
%global __find_provides %{_mingw32_findprovides}
%define __debug_install_post %{_mingw32_debug_install_post}

Name:           mingw32-glib2
Version:        2.22.0
Release:        2%{?dist}
Summary:        MinGW Windows GLib2 library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gtk.org
Source0:        http://download.gnome.org/sources/glib/2.22/glib-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 52
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-gettext

BuildRequires:  pkgconfig
# Native version required for msgfmt use in build
BuildRequires:  gettext
# Native version required for glib-genmarshal
BuildRequires:  glib2-devel

Requires:       pkgconfig


%description
MinGW Windows Glib2 library.

%package static
Summary:        Static version of the MinGW Windows GLib2 library
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description static
Static version of the MinGW Windows GLib2 library.


%{_mingw32_debug_package}


%prep
%setup -q -n glib-%{version}


%build
# GLib can't build static and shared libraries in one go, so we
# build GLib twice here
mkdir build_static
pushd build_static
        %{_mingw32_configure} --disable-shared --enable-static
        make %{?_smp_mflags}
popd

mkdir build_shared
pushd build_shared
        %{_mingw32_configure} --disable-static
        make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

# First install all the files belonging to the shared build
make -C build_shared DESTDIR=$RPM_BUILD_ROOT install

# Install all the files from the static build in a seperate folder
# and move the static libraries to the right location
make -C build_static DESTDIR=$RPM_BUILD_ROOT/build_static install
mv $RPM_BUILD_ROOT/build_static%{_mingw32_libdir}/*.a $RPM_BUILD_ROOT%{_mingw32_libdir}

# Manually merge the libtool files
sed -i s/"old_library=''"/"old_library='libgio-2.0.a'"/ $RPM_BUILD_ROOT%{_mingw32_libdir}/libgio-2.0.la
sed -i s/"old_library=''"/"old_library='libglib-2.0.a'"/ $RPM_BUILD_ROOT%{_mingw32_libdir}/libglib-2.0.la
sed -i s/"old_library=''"/"old_library='libgobject-2.0.a'"/ $RPM_BUILD_ROOT%{_mingw32_libdir}/libgobject-2.0.la
sed -i s/"old_library=''"/"old_library='libgmodule-2.0.a'"/ $RPM_BUILD_ROOT%{_mingw32_libdir}/libgmodule-2.0.la
sed -i s/"old_library=''"/"old_library='libgthread-2.0.a'"/ $RPM_BUILD_ROOT%{_mingw32_libdir}/libgthread-2.0.la

# There's also a small difference in the file glibconfig.h between the
# shared and the static build:
#
#diff -ur shared/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h static/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h
#--- shared/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h	2009-02-20 17:34:35.735677022 +0100
#+++ static/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h	2009-02-20 17:33:35.498932269 +0100
#@@ -92,7 +92,8 @@
# 
# #define G_OS_WIN32
# #define G_PLATFORM_WIN32
#-
#+#define GLIB_STATIC_COMPILATION 1
#+#define GOBJECT_STATIC_COMPILATION 1
# 
# #define G_VA_COPY	va_copy
#
# However, we can't merge this change as it is situation-dependent...
#
# Developers using the static build of GLib need to add -DGLIB_STATIC_COMPILATION
# and -DGOBJECT_STATIC_COMPILATION to their CFLAGS to avoid compile failures

# Drop the folder which was temporary used for installing the static bits
rm -rf $RPM_BUILD_ROOT/build_static

rm -f $RPM_BUILD_ROOT/%{_mingw32_libdir}/charset.alias

# Drop the GDB helper files as we can't use the native Fedora GDB to debug Win32 programs
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/gdb

# Remove the gtk-doc documentation and manpages which duplicate Fedora native
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/gtk-doc

%find_lang glib20


%clean
rm -rf $RPM_BUILD_ROOT


%files -f glib20.lang
%defattr(-,root,root,-)
%{_mingw32_bindir}/glib-genmarshal.exe
%{_mingw32_bindir}/glib-gettextize
%{_mingw32_bindir}/glib-mkenums
%{_mingw32_bindir}/gobject-query.exe
%{_mingw32_bindir}/gspawn-win32-helper-console.exe
%{_mingw32_bindir}/gspawn-win32-helper.exe
%{_mingw32_bindir}/libgio-2.0-0.dll
%{_mingw32_bindir}/libglib-2.0-0.dll
%{_mingw32_bindir}/libgmodule-2.0-0.dll
%{_mingw32_bindir}/libgobject-2.0-0.dll
%{_mingw32_bindir}/libgthread-2.0-0.dll
%{_mingw32_includedir}/glib-2.0/
%{_mingw32_libdir}/gio-2.0.def
%{_mingw32_libdir}/glib-2.0.def
%{_mingw32_libdir}/glib-2.0/
%{_mingw32_libdir}/gmodule-2.0.def
%{_mingw32_libdir}/gobject-2.0.def
%{_mingw32_libdir}/gthread-2.0.def
%{_mingw32_libdir}/libgio-2.0.dll.a
%{_mingw32_libdir}/libgio-2.0.la
%{_mingw32_libdir}/libglib-2.0.dll.a
%{_mingw32_libdir}/libglib-2.0.la
%{_mingw32_libdir}/libgmodule-2.0.dll.a
%{_mingw32_libdir}/libgmodule-2.0.la
%{_mingw32_libdir}/libgobject-2.0.dll.a
%{_mingw32_libdir}/libgobject-2.0.la
%{_mingw32_libdir}/libgthread-2.0.dll.a
%{_mingw32_libdir}/libgthread-2.0.la
%{_mingw32_libdir}/pkgconfig/gio-2.0.pc
%{_mingw32_libdir}/pkgconfig/gio-unix-2.0.pc
%{_mingw32_libdir}/pkgconfig/glib-2.0.pc
%{_mingw32_libdir}/pkgconfig/gmodule-2.0.pc
%{_mingw32_libdir}/pkgconfig/gmodule-export-2.0.pc
%{_mingw32_libdir}/pkgconfig/gmodule-no-export-2.0.pc
%{_mingw32_libdir}/pkgconfig/gobject-2.0.pc
%{_mingw32_libdir}/pkgconfig/gthread-2.0.pc
%{_mingw32_datadir}/aclocal/glib-2.0.m4
%{_mingw32_datadir}/aclocal/glib-gettext.m4
%{_mingw32_datadir}/glib-2.0/

%files static
%defattr(-,root,root,-)
%{_mingw32_libdir}/libgio-2.0.a
%{_mingw32_libdir}/libglib-2.0.a
%{_mingw32_libdir}/libgmodule-2.0.a
%{_mingw32_libdir}/libgobject-2.0.a
%{_mingw32_libdir}/libgthread-2.0.a


%changelog
* Fri Feb  4 2011 Andrew Beekhof <abeekhof@redhat.com> - 2.22.0-2
- Import 2.20.0 from Fedora so native packages dont trail mingw ones
  Related: rhbz#658833

* Wed Sep 23 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.0-1
- Update to 2.22.0

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.6-2
- Rebuild because of broken mingw32-gcc/mingw32-binutils

* Sat Sep  5 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.6-1
- Update to 2.21.6

* Mon Aug 24 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.5-1
- Update to 2.21.5

* Thu Aug 13 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.4-1
- Update to 2.21.4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.3-1
- Update to 2.21.3
- Drop upstreamed patch

* Mon Jun 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.2-2
- The wrong RPM variable was overriden for -debuginfo support. Should be okay now

* Mon Jun 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.2-1
- Update to 2.21.2
- Split out debug symbols to a -debuginfo subpackage

* Wed Jun 10 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.1-1
- Update to 2.21.1
- Use %%global instead of %%define
- Dropped the glib-i386-atomic.patch as it doesn't have any effect (the mingw32
  toolchain is called i686-pc-mingw32, not i386-pc-mingw32)

* Thu Apr 16 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.20.1-1
- Update to 2.20.1

* Thu Mar 5 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.19.10-1
- Update to 2.19.10
- Dropped the gtk-doc documentation as it's identical to the base glib2 package

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Erik van Pienbroek <info@nntpgrab.nl> - 2.19.5-4
- Added -static subpackage
- Developers using the static build of GLib need to add
  -DGLIB_STATIC_COMPILATION and -DGOBJECT_STATIC_COMPILATION to
  their CFLAGS to avoid compile failures
- Fixed the %%defattr line
- Rebuild for mingw32-gcc 4.4 (RWMJ)

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.5-3
- Requires pkgconfig.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.5-2
- Rebase to native Fedora version 2.19.5.
- Use _smp_mflags.
- Use find_lang.
- Don't build static libraries.
- +BR dlfcn.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.1-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.1-1
- Update to 2.18.1 release

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.0-3
- Remove manpages which duplicate Fedora native.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-2
- Add BR on pkgconfig, gettext and glib2 (native)

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-1
- Initial RPM release
