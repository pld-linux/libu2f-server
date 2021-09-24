#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Yubico Universal 2nd Factor (U2F) Server C Library
Summary(pl.UTF-8):	Biblioteka C serwera Universal 2nd Factor (U2F) Yubico
Name:		libu2f-server
Version:	1.1.0
Release:	4
License:	BSD
Group:		Libraries
Source0:	https://developers.yubico.com/libu2f-server/Releases/%{name}-%{version}.tar.xz
# Source0-md5:	7350f22ff60f21133a2f78d050448dae
Patch0:		%{name}-json-c.patch
URL:		https://developers.yubico.com/libu2f-server/
BuildRequires:	gengetopt
BuildRequires:	help2man
BuildRequires:	json-c-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libu2f-server is a C library that implements the server-side of the
U2F protocol. More precisely, it provides an API for generating the
JSON blobs required by U2F devices to perform the U2F Registration and
U2F Authentication operations, and functionality for verifying the
cryptographic operations.

%description -l pl.UTF-8
libu2f-server to biblioteka C implementująca stronę serwera protokołu
U2F. Ściślej mówiąc, udostępnia API do generowania blobów JSON
wymaganych przez urządzenia U2F do wykonywania operacji U2F
Registration i U2F Authentication oraz funkcjonalność weryfikowania
operacji kryptograficznych.

%package devel
Summary:	Header files for libu2f-server library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libu2f-server
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libu2f-server library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libu2f-server.

%package static
Summary:	Static libu2f-server library
Summary(pl.UTF-8):	Statyczna biblioteka libu2f-server
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libu2f-server library.

%description static -l pl.UTF-8
Statyczna biblioteka libu2f-server.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libu2f-server.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/u2f-server
%attr(755,root,root) %{_libdir}/libu2f-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libu2f-server.so.0
%{_mandir}/man1/u2f-server.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libu2f-server.so
%{_includedir}/u2f-server
%{_pkgconfigdir}/u2f-server.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libu2f-server.a
%endif
