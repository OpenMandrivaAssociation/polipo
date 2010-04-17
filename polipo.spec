
Name:			polipo
Summary:		Lightweight caching web proxy
Group:			System/Servers
Version:		1.0.4.1
Release:		%mkrel 1
License:		MIT
URL:			http://www.pps.jussieu.fr/~jch/software/%{name}/
Source0:		http://freehaven.net/~chrisd/%{name}/%{name}-%{version}.tar.gz
Source1:		%{name}.init
Source2:		%{name}.conf
Source3:		%{name}.forbidden
Source4:		%{name}.logrotate
Source5:		%{name}.nm
Patch0:			polipo-1.0.4.1-fix-Makefile-to-access-install-info.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:		info-install
Buildrequires:      texinfo
Requires(pre):		rpm-helper
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Requires:		chkconfig
Requires:		info-install
Requires:		logrotate

%description
Polipo is a lightweight caching web proxy that was designed as a personal
cache. It is able to cache incomplete objects and will complete them using
range requests. It will use HTTP/1.1 pipelining if supported by the remote
server.

%files
%defattr(-,root,root,-)
%doc README CHANGES COPYING config.sample
%attr(0750,%{name},%{name}) %dir %{_var}/cache/%{name}
%attr(0750,%{name},%{name}) %dir %{_var}/run/%{name}
%attr(0750,%{name},%{name}) %{_logdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_infodir}/%{name}.info.lzma
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/forbidden
%attr(0755,root,%name) %{_initddir}/%{name}
%attr(0755,root,%name) %{_sysconfdir}/NetworkManager/dispatcher.d
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}


#--------------------------------------------------------------------
%prep
%setup -q
%patch0 -p0 -b .fix_makefile

%build
%make CDEBUGFLAGS="%{optflags}"

%install
rm -rf %{buildroot}

%makeinstall \
	TARGET=%{buildroot} \
	PREFIX=%{_prefix} \
	BINDIR=%{_bindir} \
	MANDIR=%{_mandir} \
	INFODIR=%{_infodir}

install -m 0755 -d %{buildroot}%{_sysconfdir}/%{name}
install -m 0750 -d %{buildroot}%{_var}/run/%{name}
install -m 0750 -d %{buildroot}%{_var}/cache/%{name}
install -m 0750 -d %{buildroot}%{_logdir}
touch %{buildroot}%{_logdir}/%{name}

install -D -pm 0755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}
install -D -pm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/config
install -D -pm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/forbidden
install -D -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -D -pm 0755 %{SOURCE5} %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/25-%{name}

rm -f %{buildroot}%{_infodir}/dir

%pre
%_pre_useradd %{name} %{_var}/cache/%{name} /bin/false

%post
%_post_service %{name}
/sbin/install-info --quiet --info-dir=%{_infodir} %{_infodir}/%{name}.info.lzma || : 

%preun
%_preun_service %{name}
%_install_info

%postun
%_postun_userdel %{name}


%clean
rm -rf %{buildroot}


