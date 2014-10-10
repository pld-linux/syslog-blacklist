# TODO
# etc/default/syslog-blacklist
# etc/init.d/syslog-blacklist
# etc/logrotate.d/syslog-blacklist
# etc/rsyslog.d/01-syslog-blacklist.conf
%include	/usr/lib/rpm/macros.perl
Summary:	Intrusion Blocking with Perl and Ipset
Name:		syslog-blacklist
# from debian/changelog
Version:	1.5
Release:	0.3
License:	GPL v2+
Group:		Applications/Networking
# git clone http://bogeskov.dk/git/syslog-blacklist.git
# tar --exclude-vcs -czf syslog-blacklist.tar.gz syslog-blacklist
Source0:	%{name}.tar.gz
# Source0-md5:	51258b2c1225333feb181e2ee4117716
Patch0:		geoip.patch
URL:		http://bogeskov.dk/Ipset.html
BuildRequires:	dpkg
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	ipset
Suggests:	perl-Geo-IP
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a Perl daemon, that runs a syslog like daemon
which pattermatches against loglines and then tracks ip using ipset.

%prep
%setup -q -n %{name}
%patch0 -p1
mv root/* .
mv debian/copyright .

%build
ver=$(dpkg-parsechangelog --show-field Version)
test "$ver" = "%{version}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_sysconfdir},%{_mandir}}
cp -a usr/share/man/* $RPM_BUILD_ROOT%{_mandir}
install -p usr/bin/syslog-inject $RPM_BUILD_ROOT%{_bindir}
install -p usr/sbin/syslog-blacklist $RPM_BUILD_ROOT%{_sbindir}
cp -p etc/syslog-blacklist.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc copyright
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/syslog-blacklist.conf
%attr(755,root,root) %{_bindir}/syslog-inject
%attr(755,root,root) %{_sbindir}/syslog-blacklist
%{_mandir}/man1/syslog-blacklist.1*
%{_mandir}/man1/syslog-inject.1*
