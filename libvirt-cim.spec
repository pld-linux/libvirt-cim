Summary:	CIM provider for libvirt
Summary(pl.UTF-8):	Dostarczyciel CIM dla libvirt
Name:		libvirt-cim
Version:	0.6.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://libvirt.org/libvirt-cim/%{name}-%{version}.tar.bz2
# Source0-md5:	168ce53e26e2ac4b9eb261a82adc2e34
Patch0:		%{name}-make.patch
URL:		http://libvirt.org/CIM/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no devel files
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libxkutil.{so,la}
# plugins
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/*.la

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
%dir %{_datadir}/libvirt-cim
%{_datadir}/libvirt-cim/*.mof
%{_datadir}/libvirt-cim/*.registration
%{_datadir}/libvirt-cim/cim_schema_2.21.0Experimental-MOFs.zip
%{_datadir}/libvirt-cim/cimv2.21.0-*_mof
%attr(755,root,root) %{_datadir}/libvirt-cim/install_base_schema.sh
%attr(755,root,root) %{_datadir}/libvirt-cim/provider-register.sh
