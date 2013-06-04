# molly-guard.spec - SPEC file to build RPM packages
#
# Copyright © Lazarus Long <lazarus.long@bigfoot.com>
# Released under the terms of the Artistic Licence 2.0
#
%define rev		.1
%define ver		0.4.5
%define debrelease	1
%define home		http://ftp.debian.org/debian/pool/main/m

%define _arch		noarch
%define _mandir		%{_datadir}/man 
%define _rpmfilename	%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}%{?dist}.%{ARCH}.rpm
%define _sysconfdir	/etc

Name: molly-guard
Version: %{ver}
Release: %{debrelease}%{?rev}
BuildArch: noarch
BuildRequires: docbook-style-xsl, libxslt
Requires: procps
Vendor: Martin F. Krafft <madduck@madduck.net>
Packager: Lazarus Long <lazarus.long@bigfoot.com> 
License: Artistic Licence 2.0
Distribution: Debian
Group: Applications/Internet
URL: %{home}/%{name}
Source0: %{url}/%{name}_%{version}.orig.tar.gz
Source1: %{url}/%{name}_%{version}-%{debrelease}.diff.gz
Source2: %{url}/%{name}_%{version}-%{debrelease}.dsc
Source3: Makefile
Patch0: %{name}-%{version}-run-parts.patch
Patch1: %{name}-%{version}-Makefile-docbook.patch
Patch2: %{name}-%{version}-Makefile-doubleslashes.patch
Patch3: %{name}-%{version}-Makefile-installfix.patch
Patch4: %{name}-%{version}-profile.d.patch
Patch5: %{name}-%{version}-shutdown-el5.patch
Summary: protects machines from accidental shutdowns/reboots

%description
The package installs a shell script that overrides the existing
shutdown/reboot/halt/poweroff commands and first runs a set of scripts, which
all have to exit successfully, before molly-guard invokes the real command.

One of the scripts checks for existing SSH sessions. If any of the four
commands are called interactively over an SSH session, the shell script
prompts you to enter the name of the host you wish to shut down. This should
adequately prevent you from accidental shutdowns and reboots.

This shell script passes through the commands to the respective binaries in
/sbin and should thus not get in the way if called non-interactively, or
locally.

%changelog
* Fri Oct 26 2012 Lazarus Long <lazarus.long@bigfoot.com> 0.4.5-1.1
- fixed incorrect permissions for /etc/profile.d
- patched /usr/share/molly-guard/shutdown to run on EL version 5
- modified source to create packages for both EL versions 5 and 6

* Sat Jun 3 2012 Lazarus Long <lazarus.long@bigfoot.com> 0.4.5-1
- build from Debian repository
- included /etc/profile.d/molly-guard.sh and /etc/profile.d/molly-guard.csh
  to reorder the $PATH environment. RedHat’s $PATH ordering differs from 
  Debian’s, RedHat has /sbin before /usr/sbin.

%prep
%setup
zcat ${RPM_SOURCE_DIR}/%{name}_%{version}-%{debrelease}.diff.gz |patch -p1 -E -s
%patch -P 0 -p1 -E
%patch -P 1 -p1 -E
%patch -P 2 -p1 -E
%patch -P 3 -p1 -E
%patch -P 4 -p1 -E
%{?el5:%patch -P 5 -p1 -E}

%build
make all prefix=%{_prefix} etc_prefix=/

%install
mkdir -p ${RPM_BUILD_ROOT}
make install DEST=${RPM_BUILD_ROOT} prefix=%{_prefix} etc_prefix=/
install -m755 -oroot -groot -d ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
install -m644 -oroot -groot profile.d/* ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
install -m755 -oroot -groot -d ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}-%{version}-%{release}
install -m644 -oroot -groot ChangeLog debian/copyright ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}-%{version}-%{release}

%clean
rm -fr ${RPM_BUILD_ROOT}

%files
%docdir "%{_datadir}/doc/%{name}-%{version}-%{release}"
%attr(775, root, root) %dir "%{_datadir}/%{name}"
%attr(755, root, root) "%{_datadir}/%{name}/shutdown"
%attr(644, root, root) %doc "%{_mandir}/man8/%{name}.8.gz"
%attr(755, root, root) %config "%{_sysconfdir}/profile.d"
%attr(755, root, root) %dir "%{_sysconfdir}/%{name}"
%attr(755, root, root) %dir "%{_sysconfdir}/%{name}/run.d"
%attr(755, root, root) %config "%{_sysconfdir}/%{name}/run.d"
%attr(755, root, root) %dir "%{_sysconfdir}/%{name}/messages.d"
%attr(644, root, root) %config "%{_sysconfdir}/%{name}/rc"
%attr(644, root, root) %doc "%{_datadir}/doc/%{name}-%{version}-%{release}"
%attr(-, root, root) "%{_sbindir}"
