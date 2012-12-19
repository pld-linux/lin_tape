#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		rel	12
%define		pname	lin_tape
Summary:	IBM Tape SCSI Device Driver for Linux
Name:		%{pname}%{_alt_kernel}
Version:	1.74.0
Release:	%{rel}
License:	GPL v2/LGPL
Group:		Base/Kernel
Source0:	%{pname}-%{version}.tgz
# Source0-md5:	675822326c2b12390b5164a4e2b14aec
Patch0:		use-module-dir.patch
# System Storage, Tape systems, Tape drivers and software, Tape device drivers (Linux)
URL:		http://www.ibm.com/support/fixcentral/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The IBM Tape Device Driver, lin_tape, product is a device driver that
provides attachment for the IBM TotalStorage and System Storage tape
devices to Linux compatible platforms.

%package -n kernel%{_alt_kernel}-scsi-lin_tape
Summary:	IBM Tape SCSI Device Driver for Linux
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-scsi-lin_tape
The IBM Tape Device Driver, lin_tape, product is a device driver that
provides attachment for the IBM TotalStorage and System Storage tape
devices to Linux compatible platforms.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%ifarch %ix86 ia64
proc="Intel"
%endif
%ifarch %x8664
proc="AMD"
%endif
%ifarch ppc ppc64 powerpc powerpc64
proc="pSeries"
%endif
%ifarch s390 s390x
proc="zSeries"
%endif

%{__cp} -af lin_tape_359X_${proc}.ReadMe lin_tape_359X.ReadMe
%{__cp} -af lin_tape_Ultrium_${proc}.ReadMe lin_tape_Ultrium.ReadMe

%{__mv} Makefile Makefile.IBM
%{__cp} -af Makefile.GPL Makefile

%build
%build_kernel_modules -m lin_tape

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m lin_tape -d kernel/drivers/scsi

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-scsi-lin_tape
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-scsi-lin_tape
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-scsi-lin_tape
%defattr(644,root,root,755)
%doc lin_tape.fixlist lin_tape_Ultrium.ReadMe lin_tape_359X.ReadMe
/lib/modules/%{_kernel_ver}/kernel/drivers/scsi/lin_tape.ko*
