Summary:	CIM provider for libvirt
Summary(pl.UTF-8):	Dostarczyciel CIM dla libvirt
Name:		libvirt-cim
Version:	0.6.3
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://libvirt.org/libvirt-cim/%{name}-%{version}.tar.bz2
# Source0-md5:	6e5bea3a8bf9d3fca70b67498126f2e4
Patch0:		%{name}-inline.patch
Patch1:		%{name}-scanf.patch
Patch2:		%{name}-strcpy.patch
URL:		http://libvirt.org/CIM/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
# scanf 'm' modifier for %s-like formats
BuildRequires:	glibc-devel >= 6:2.7
BuildRequires:	libcmpiutil-devel >= 0.1
BuildRequires:	libconfig-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel >= 1.41.2
BuildRequires:	libvirt-devel >= 0.9.0
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	sblim-cmpi-devel
Requires:	libcmpiutil >= 0.1
Requires:	libuuid >= 1.41.2
Requires:	libvirt >= 0.9.0
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libvirt-cim is a CMPI CIM provider that implements the DMTF SVPC
virtualization model. The goal is to support most of the features
exported by libvirt itself, enabling management of multiple platforms
with a single provider.

%description -l pl.UTF-8
Libvirt-cim to dostarczyciel CMPI CIM implementujący model
wirtualizacji DMTF SVPC. Celem jest obsługa większości funkcji
eksportowanych przez libvirt, a tym samym umożliwienie zarządzania
wieloma platformamy poprzez pojedynczego dostarczyciela.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-migrate_check_dir=%{_libdir}/libvirt-cim/extchecks \
	--with-xen_emulator=%{_libdir}/xen/bin/qemu-dm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/libvirt-cim/extchecks

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no devel files
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libxkutil.{so,la}
# plugins
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README doc/*.html
%attr(755,root,root) %{_libdir}/libxkutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxkutil.so.0
%{_libdir}/cmpi/libVirt_*.so*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libvirt-cim.conf
%dir %{_libdir}/libvirt-cim
%dir %{_libdir}/libvirt-cim/extchecks
%dir %{_datadir}/libvirt-cim
%{_datadir}/libvirt-cim/*.mof
%{_datadir}/libvirt-cim/*.registration
%{_datadir}/libvirt-cim/cim_schema_2.21.0Experimental-MOFs.zip
%{_datadir}/libvirt-cim/cimv2.21.0-*_mof
%attr(755,root,root) %{_datadir}/libvirt-cim/install_base_schema.sh
%attr(755,root,root) %{_datadir}/libvirt-cim/provider-register.sh
