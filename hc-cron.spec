Summary:	Home computer cron daemon
Summary(fr.UTF-8):	Démon Home computer cron
Summary(pl.UTF-8):	Demon cron dla domowego komputera
Summary(tr.UTF-8):	Home computer cron süreci, periyodik program çalıştırma yeteneği
Name:		hc-cron
Version:	0.14
Release:	24
License:	GPL
Group:		Daemons
Source0:	ftp://ftp.berlios.de/pub/hc-cron/stable/%{name}-%{version}.tar.gz
# Source0-md5:	19140ce4ceb7d800d2aae6be8b9361cb
Source1:	%{name}.init
Source2:	cron.logrotate
Source3:	%{name}.crontab
Source4:	crontab.1.pl
Source5:	cron.8.pl
Source6:	cron.sysconfig
Patch0:		%{name}-syscrondir.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-time.patch
Patch3:		%{name}-closefile.patch
Patch4:		%{name}-sgid.patch
Patch5:		%{name}-sleep.patch
BuildRequires:	rpmbuild(macros) >= 1.247
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	/bin/run-parts
Requires:	/sbin/chkconfig
Requires:	psmisc >= 20.1
Requires:	rc-scripts
Provides:	crondaemon
Provides:	crontabs = 1.7
Provides:	group(crontab)
Obsoletes:	crondaemon
Obsoletes:	crontabs
Obsoletes:	mcron
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
hc-cron is a cron daemon for home computers. It runs specified jobs at
periodic intervals and will remember the time when it was shut down
and catch up jobs that have occurred during down time when it is
started again. Hc-cron is based on the widely used vixie-cron and uses
the same crontab format so that it can be used as a drop-in
replacement for that program.

%description -l de.UTF-8
cron ist ein Standard-UNIX-Programm, das zu vorgegebenen Zeiten vom
Benutzer angegebene Programme ausführt. hc-cron weist mehr Funktionen
auf als cron aus UNIX, u.a. bessere Sicherheit und leistungsfähigere
Konfigurationsoptionen.

%description -l fr.UTF-8
cron est un des programmes UNIX standard qui permet à un utilisateur
donné de lancer des périodiquement des programmes selon un ordre
planifié. hc-cron ajoute de nombreuses fonctionnalités au cron UNIX de
base, dont une plus grande sécurité et des options de configuration
plus puissantes.

%description -l pl.UTF-8
hc-cron jest demonem cron dla domowych komputerów. Uruchamia zadania w
określonych odstępach czasu oraz pamięta kiedy został wyłączony, by
móc wykonać pominięte zadania gdy zostanie ponownie uruchomiony.
Hc-cron jest oparty na szeroko używanym vixie cronie i używa tego
samego formatu pliku crontab, więc można stosować zamiennie te
programy.

%description -l tr.UTF-8
cron UNIX'de standart olarak belirli zamanlarda bir programı
çalıştırmak için kullanılan daemon'dur. hc-cron, standart cron'dan
daha güvenlidir ve daha gelişmiş yapılandırma seçenekleri içerir.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__make} \
	 OPTIM="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{cron.{hourly,daily,weekly,monthly},cron} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{cron.d,rc.d/init.d,logrotate.d,sysconfig} \
	$RPM_BUILD_ROOT%{_mandir}/{man{1,5,8},pl/man{1,8}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_bindir}} \
	$RPM_BUILD_ROOT/var/{spool/cron,log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

echo "# Simple define users for cron" > $RPM_BUILD_ROOT%{_sysconfdir}/cron/cron.allow
echo "root" > $RPM_BUILD_ROOT%{_sysconfdir}/cron/cron.allow
:> $RPM_BUILD_ROOT/var/log/cron

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/crond
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/cron
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/system
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/pl/man1/crontab.1
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/pl/man8/cron.8
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/cron

echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/man8/crond.8
echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/pl/man8/crond.8

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 117 -r -f crontab

%post
/sbin/chkconfig --add crond
umask 027
touch /var/log/cron
chgrp crontab /var/log/cron
chmod 660 /var/log/cron
%service crond restart "cron daemon"

%preun
if [ "$1" = "0" ]; then
	%service crond stop
	/sbin/chkconfig --del crond
fi

%postun
if [ "$1" = "0" ]; then
	%groupremove crontab
fi

%triggerpostun -- hc-cron <= 0.14-8
if [ -f /var/lib/cron.lastrun ]; then
	mv -f /var/lib/cron.lastrun /var/lib/misc/cron.lastrun
fi

%triggerpostun -- hc-cron <= 0.14-11
for i in `/bin/ls /var/spool/cron 2>/dev/null`
do
	/bin/chown ${i} /var/spool/cron/${i} 2>/dev/null || :
done
/bin/chmod 660 /var/log/cron
/bin/chgrp crontab /var/log/cron
/bin/chmod 640 /etc/cron/cron.*
/bin/chgrp crontab /etc/cron/cron.*

%triggerpostun -- vixie-cron
/sbin/chkconfig --add crond

%triggerpostun -- vixie-cron <= 3.0.1-85
for i in `/bin/ls /var/spool/cron 2>/dev/null`
do
	/bin/chown ${i} /var/spool/cron/${i} 2>/dev/null || :
done
/bin/chmod 660 /var/log/cron
/bin/chgrp crontab /var/log/cron
/bin/chmod 640 /etc/cron/cron.*
/bin/chgrp crontab /etc/cron/cron.*

%files
%defattr(644,root,root,755)
%doc README ChangeLog doc/{CONVERSION,FEATURES,MAIL,README.vix,THANKS}
%attr(754,root,root) /etc/rc.d/init.d/crond
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(750,root,root) %dir %{_sysconfdir}/cron.*
%attr(750,root,crontab) %dir %{_sysconfdir}/cron
%attr(640,root,crontab) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cron/*
%attr(640,root,crontab) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/*
%attr(755,root,root) %{_sbindir}/crond
%attr(2755,root,crontab) %{_bindir}/crontab
%attr(1730,root,crontab) %dir /var/spool/cron
%attr(660,root,crontab) %ghost /var/log/*
%lang(pl) %{_mandir}/pl/man*/*
%{_mandir}/man*/*
