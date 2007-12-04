%define name	ati.2
%define cvs	20030708
%define version	4.3
%define release	 %mkrel 1

%define x11prefix /usr/X11R6
%define x11libdir %{x11prefix}/lib
%define x11moddir %{x11libdir}/modules

Summary:	Gatos enhanced ATI drivers
Name:		%{name}
Version:	%{version}.%{cvs}
Release:	%{release}
License:	GPL
Group:		System/XFree86
URL:		http://gatos.sourceforge.net
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	X11-devel >= 4.3

%description
These are the experimental ATI drivers from gatos.sourceforge.net


%prep
%setup -n %{name}
%build
xmkmf %{_topdir}/BUILD/XFree86-4.3/xc
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
mkdir -p $RPM_BUILD_ROOT/%{x11moddir}/atidri
cd %{_topdir}/BUILD/XFree86-4.3/xc/lib/GL/mesa/src/drv/r200
install -c -m 0444 r200_dri.so $RPM_BUILD_ROOT/%{x11moddir}/atidri
cd %{_topdir}/BUILD/XFree86-4.3/xc/lib/GL/mesa/src/drv/radeon
install -c -m 0444 radeon_dri.so $RPM_BUILD_ROOT/%{x11moddir}/atidri

mkdir -p $RPM_BUILD_ROOT/%x11moddir/atidrivers
mv $RPM_BUILD_ROOT%{x11moddir}/drivers/* $RPM_BUILD_ROOT/%{x11moddir}/atidrivers
rm -rf $RPM_BUILD_ROOT/%{x11moddir}/drivers

%pre
mkdir -p %{x11moddir}/dri_old
mv %{x11moddir}/dri/r200_dri.so %{x11moddir}/dri_old
mv %{x11moddir}/dri/radeon_dri.so %{x11moddir}/dri_old

mkdir -p %{x11moddir}/drivers_old
mv %{x11moddir}/drivers/ati_drv.o %{x11moddir}/drivers_old
mv %{x11moddir}/drivers/atimisc_drv.o %{x11moddir}/drivers_old
mv %{x11moddir}/drivers/r128_drv.o %{x11moddir}/drivers_old
mv %{x11moddir}/drivers/radeon_drv.o %{x11moddir}/drivers_old

%post
mv %{x11moddir}/atidri/* %{x11moddir}/dri
rm -rf %{x11moddir}/atidri
mv %{x11moddir}/atidrivers/* %{x11moddir}/drivers
rm -rf %{x11moddir}/atidrivers

%postun
mv %{x11moddir}/dri_old/* %{x11moddir}/dri
mv -f %{x11moddir}/drivers_old/* %{x11moddir}/drivers
rm -rf %{x11moddir}/drivers_old
rm -rf %{x11moddir}/multimedia

%clean
rm -rf %RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.gatos
%{x11moddir}/atidri
%{x11moddir}/atidrivers
%{x11moddir}/multimedia

