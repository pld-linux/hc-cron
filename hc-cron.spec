Summary:	Home computer cron daemon
Summary(fr):	Démon Home computer cron
Summary(pl):	Demon cron dla domowego komputera
Summary(tr):	Home computer cron süreci, periyodik program çalýþtýrma yeteneði
Name:		hc-cron
Version:	0.14
Release:	11.9
License:	GPL
Group:		Daemons
Source0:	ftp://ftp.berlios.de/pub/hc-cron/stable/%{name}-%{version}.tar.gz
# Source0-md5: 19140ce4ceb7d800d2aae6be8b9361cb
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
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	/bin/run-parts
Requires:	psmisc >= 20.1
Provides:	crontabs
Provides:	crondaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	crondaemon
Obsoletes:	vixie-cron
Obsoletes:	crontabs

%description
hc-cron is a cron daemon for home computers. It runs specified jobs at
periodic intervals and will remember the time when it was shut down and
catch up jobs that have occurred during down time when it is started
again. Hc-cron is based on the widely used vixie-cron and uses the same
crontab format so that it can be used as a drop-in replacement for that
program.

%description -l de
cron ist ein Standard-UNIX-Programm, das zu vorgegebenen Zeiten vom
Benutzer angegebene Programme ausführt. hc-cron weist mehr Funktionen
auf als cron aus UNIX, u.a. bessere Sicherheit und leistungsfähigere
Konfigurationsoptionen.

%description -l fr
cron est un des programmes UNIX standard qui permet à un utilisateur
donné de lancer des périodiquement des programmes selon un ordre
planifié. hc-cron ajoute de nombreuses fonctionnalités au cron UNIX de
base, dont une plus grande sécurité et des options de configuration
plus puissantes.

%description -l pl
hc-cron jest demonem cron dla domowych komputerów. Uruchamia zadania
w okre¶lonych odstêpach czasu oraz pamiêta kiedy zosta³ wy³±czony, by
móc wykonaæ pominiête zadania gdy zostanie ponownie uruchomiony.
Hc-cron jest oparty na szeroko u¿ywanyn vixie cronie i u¿ywa tego
samego formatu pliku crontab, wiêc mo¿na stosowaæ zamiennie te programy.

%description -l tr
cron UNIX'de standart olarak belirli zamanlarda bir programý
çalýþtýrmak için kullanýlan daemon'dur. hc-cron, standart cron'dan
daha güvenlidir ve daha geliþmiþ yapýlandýrma seçenekleri içerir.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/pl/man1/crontab.1
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/pl/man8/cron.8

echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/man8/crond.8
echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/pl/man8/crond.8

echo "# Simple define users for cron" > $RPM_BUILD_ROOT%{_sysconfdir}/cron/cron.allow
echo "root" > $RPM_BUILD_ROOT%{_sysconfdir}/cron/cron.allow
:> $RPM_BUILD_ROOT/var/log/cron

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/crond
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/cron
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/system
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/cron

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid crontab`" ]; then
        if [ "`/usr/bin/getgid crontab`" != "117" ]; then
                echo "Error: group crontab doesn't have gid=117. Correct this before installing cron." 1>&2
                exit 1
        fi
else
        echo "Adding group crontab GID=117."
        /usr/sbin/groupadd -g 117 -r -f crontab
fi


%post
/sbin/chkconfig --add crond
if [ -f /var/lock/subsys/crond ]; then
	/etc/rc.d/init.d/crond restart >&2
else
	echo "Run \"/etc/rc.d/init.d/crond start\" to start cron daemon."
fi
touch /var/log/cron
chmod 640 /var/log/cron

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/crond ]; then
		/etc/rc.d/init.d/crond stop >&2
	fi
	/sbin/chkconfig --del crond
fi

%postun
if [ "$1" = "0" ]; then
        echo "Removing group crontab."
        /usr/sbin/groupdel crontab
fi


%triggerpostun -- vixie-cron
/sbin/chkconfig --add crond

%triggerpostun -- hc-cron <= 0.14-8
if [ -f /var/lib/cron.lastrun ]; then
	mv -f /var/lib/cron.lastrun /var/lib/misc/cron.lastrun
fi

%triggerpostun  -- vixie-cron <= 0.14-11
cd /var/spool/cron
for i in `ls /var/spool/cron/*`
do
        chown ${i} /var/spool/cron/${i}
done
/bin/chmod 660 /var/log/cron
/bin/chgrp crontab /var/log/cron
/bin/chmod 1770 /var/spool/cron
/bin/chgrp crontab /var/spool/cron
/bin/chmod 660 /etc/cron/cron.*
/bin/chgrp crontab /etc/cron/cron.*

%files
%defattr(644,root,root,755)
%doc README ChangeLog doc/{CONVERSION,FEATURES,MAIL,README.vix,THANKS}

%attr(754,root,root) /etc/rc.d/init.d/crond

%attr(640,root,root) %config(noreplace) /etc/logrotate.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*

%attr(750,root,root) %dir %{_sysconfdir}/cron*
%attr(640,root,crontab) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/cron/*
%attr(640,root,root) /etc/cron.d/*

%attr(0755,root,root) %{_sbindir}/crond
%attr(2755,root,crontab) %{_bindir}/crontab

%{_mandir}/man*/*
%lang(pl) %{_mandir}/pl/man*/*

%attr(770,root,crontab) %dir /var/spool/cron
%attr(660,root,crontab) %ghost /var/log/*
