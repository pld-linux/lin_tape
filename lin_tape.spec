#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel	8
%define		pname	lin_tape
Summary:	IBM Tape SCSI Device Driver for Linux
Name:		%{pname}%{_alt_kernel}
Version:	2.1.0
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL v2/LGPL
Group:		Base/Kernel
Source0:	%{pname}-%{version}.tgz
# Source0-md5:	a46993ee41fb438ae3b35249fe2c376f
Patch0:		use-module-dir.patch
Patch1:		linux-3.10.patch
# System Storage, Tape systems, Tape drivers and software, Tape device drivers (Linux)
URL:		http://www.ibm.com/support/fixcentral/
BuildRequires:	rpmbuild(macros) >= 1.678
%{?with_dist_kernel:%{expand:%kbrs}}
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
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%endif\
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
%doc lin_tape.fixlist lin_tape_Ultrium.ReadMe lin_tape_359X.ReadMe\
/lib/modules/%{_kernel_ver}/kernel/drivers/scsi/lin_tape.ko*\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -m lin_tape\
%install_kernel_modules -D installed -m lin_tape -d kernel/drivers/scsi\
%{nil}

%{expand:%kpkg}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
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
%{expand:%bkpkg}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
