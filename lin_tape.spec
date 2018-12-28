#
# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	2
%define		pname	lin_tape
Summary:	IBM Tape SCSI Device Driver for Linux
Name:		%{pname}%{_alt_kernel}
Version:	3.0.33
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL v2/LGPL
Group:		Base/Kernel
Source0:	%{pname}-%{version}.tgz
# Source0-md5:	c22358f485f12baa7254aa25abe20a43
Source1:	%{pname}.fixlist
Patch0:		use-module-dir.patch
Patch1:		clean-ifdefs.patch
Patch2:		linux-4.9.patch
Patch4:		linux-4.11.patch
Patch5:		linux-4.12.patch
Patch6:		linux-4.13.patch
Patch7:		kernel-4.14.patch
Patch8:		kernel-4.15.patch
Patch9:		kernel-4.17.patch
Patch10:	kernel-4.19.patch
Patch11:	linux-4.4.169.patch
# System Storage, Tape systems, Tape drivers and software, Tape device drivers (Linux)
URL:		http://www.ibm.com/support/fixcentral/
BuildRequires:	rpmbuild(macros) >= 1.701
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The IBM Tape Device Driver, lin_tape, product is a device driver that
provides attachment for the IBM TotalStorage and System Storage tape
devices to Linux compatible platforms.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-scsi-lin_tape\
Summary:	IBM Tape SCSI Device Driver for Linux\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-scsi-lin_tape\
The IBM Tape Device Driver is a device driver that provides attachment\
for the IBM TotalStorage and System Storage tape devices to Linux\
compatible platforms.\
\
%post	-n kernel%{_alt_kernel}-scsi-lin_tape\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-scsi-lin_tape\
%depmod %{_kernel_ver}\
\
%files -n kernel%{_alt_kernel}-scsi-lin_tape\
%defattr(644,root,root,755)\
%doc lin_tape.fixlist lin_tape.ReadMe\
/lib/modules/%{_kernel_ver}/kernel/drivers/scsi/lin_tape.ko*\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -m lin_tape\
%install_kernel_modules -D installed -m lin_tape -d kernel/drivers/scsi\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -q -n %{pname}-%{version}
%undos Makefile
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

install -p %{SOURCE1} .

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
