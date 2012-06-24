Summary:	Home computer cron daemon
Summary(fr):	D�mon Home computer cron
Summary(pl):	Demon cron dla domowego komputera
Summary(tr):	Home computer cron s�reci, periyodik program �al��t�rma yetene�i
Name:		hc-cron
Version:	0.14
Release:	18
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
PreReq:		rc-scripts
PreReq:		/sbin/chkconfig
BuildRequires:	rpmbuild(macros) >= 1.176
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(postun):	/usr/sbin/groupdel
Requires:	/bin/run-parts
Requires:	psmisc >= 20.1
Provides:	crontabs
Provides:	crondaemon
Provides:	group(crontab)
Obsoletes:	crontabs
Obsoletes:	fcron
Obsoletes:	mcron
Obsoletes:	vixie-cron
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
hc-cron is a cron daemon for home computers. It runs specified jobs at
periodic intervals and will remember the time when it was shut down
and catch up jobs that have occurred during down time when it is
started again. Hc-cron is based on the widely used vixie-cron and uses
the same crontab format so that it can be used as a drop-in
replacement for that program.

%description -l de
cron ist ein Standard-UNIX-Programm, das zu vorgegebenen Zeiten vom
Benutzer angegebene Programme ausf�hrt. hc-cron weist mehr Funktionen
auf als cron aus UNIX, u.a. bessere Sicherheit und leistungsf�higere
Konfigurationsoptionen.

%description -l fr
cron est un des programmes UNIX standard qui permet � un utilisateur
donn� de lancer des p�riodiquement des programmes selon un ordre
planifi�. hc-cron ajoute de nombreuses fonctionnalit�s au cron UNIX de
base, dont une plus grande s�curit� et des options de configuration
plus puissantes.

%description -l pl
hc-cron jest demonem cron dla domowych komputer�w. Uruchamia zadania w
okre�lonych odst�pach czasu oraz pami�ta kiedy zosta� wy��czony, by
m�c wykona� pomini�te zadania gdy zostanie ponownie uruchomiony.
Hc-cron jest oparty na szeroko u�ywanym vixie cronie i u�ywa tego
samego formatu pliku crontab, wi�c mo�na stosowa� zamiennie te
programy.

%description -l tr
cron UNIX'de standart olarak belirli zamanlarda bir program�
�al��t�rmak i�in kullan�lan daemon'dur. hc-cron, standart cron'dan
daha g�venlidir ve daha geli�mi� yap�land�rma se�enekleri i�erir.

%prep
%setup -q
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
	%banner %{name} -e << EOF
Run \"/etc/rc.d/init.d/crond start\" to start cron daemon.
EOF
# "
fi
umask 027
touch /var/log/cron
chgrp crontab /var/log/cron
chmod 660 /var/log/cron

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/crond ]; then
		/etc/rc.d/init.d/crond stop >&2
	fi
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
%attr(0755,root,root) %{_sbindir}/crond
%attr(2755,root,crontab) %{_bindir}/crontab
%attr(1730,root,crontab) %dir /var/spool/cron
%attr(660,root,crontab) %ghost /var/log/*
%lang(pl) %{_mandir}/pl/man*/*
%{_mandir}/man*/*
