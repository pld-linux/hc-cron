Summary:	Home computer cron daemon
Summary(de):	Home computer cron daemon 
Summary(fr):	Démon Home computer cron
Summary(pl):	Demon cron dla domowego komputera
Summary(tr):	Home computer cron süreci, periyodik program çalýþtýrma \
Summary(tr):	yeteneði
Name:		hc-cron
Version:	0.11
Release:	4
Copyright:	GPL
Group:		Daemons
Group(pl):	Serwery
URL:		ftp://sunsite.unc.edu/pub/Linux/system/daemons/cron/
Source0:	%{name}-%{version}.tar.gz
Source1:	hc-cron.init
Source2:	cron.log
Source3:	run-parts
Source4:	hc-cron.crontab
Patch:		hc-cron-syscrondir.patch
Prereq:		/sbin/chkconfig
Provides:	crontabs
Obsoletes:	vixie-cron
Obsoletes:	crontabs
Buildroot:	/tmp/%{name}-%{version}-root


%description
cron is a standard UNIX program that runs user-specified programs at
periodic scheduled times. hc-cron adds a number of features to the
basic UNIX cron, including better security and more powerful configuration
options.

%description -l de
cron ist ein Standard-UNIX-Programm, das zu vorgegebenen Zeiten vom
Benutzer angegebene Programme ausführt. hc-cron weist mehr Funktionen
auf als cron aus UNIX, u.a. bessere Sicherheit und leistungsfähigere
Konfigurationsoptionen.

%description -l fr
cron est un des programmes UNIX standard qui permet à un utilisateur donné
de lancer des périodiquement des programmes selon un ordre planifié.
hc-cron ajoute de nombreuses fonctionnalités au cron UNIX de base, dont
une plus grande sécurité et des options de configuration plus puissantes.

%description -l pl
cron to standardowy uniksowy program, który okresowo uruchamia okre¶lone
przez u¿ytkowników programy. hc-cron dodaje mo¿liwo¶ci podstawowemu
uniksowemu cronowi, w tym lepsze bezpieczeñstwo i bogatsze opcje
konfiguracyjne.

%description -l tr
cron UNIX'de standart olarak belirli zamanlarda bir programý çalýþtýrmak
için kullanýlan daemon'dur. hc-cron, standart cron'dan daha güvenlidir
ve daha geliþmiþ yapýlandýrma seçenekleri içerir.

%prep
%setup -q
%patch -p1 

%build
make OPTIM="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/{sbin,bin,man/man{1,5,8}} \
	$RPM_BUILD_ROOT/var/spool/cron \
	$RPM_BUILD_ROOT/etc/{crontab.d,rc.d/init.d,logrotate.d} \
	$RPM_BUILD_ROOT/etc/cron.{hourly,daily,weekly,monthly}

install cron $RPM_BUILD_ROOT/usr/sbin/crond
install crontab $RPM_BUILD_ROOT/usr/bin
install crontab.1 $RPM_BUILD_ROOT/usr/man/man1
install crontab.5 $RPM_BUILD_ROOT/usr/man/man5
install cron.8 $RPM_BUILD_ROOT/usr/man/man8

echo ".so cron.8" > $RPM_BUILD_ROOT/usr/man/man8/crond.8

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/crond
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/cron
install %{SOURCE3} $RPM_BUILD_ROOT/usr/bin
install %{SOURCE4} $RPM_BUILD_ROOT/etc/crontab.d/system

gzip -9nf $RPM_BUILD_ROOT/usr/man/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add crond
if test -r /var/run/crond.pid; then
	/etc/rc.d/init.d/crond stop >&2
	/etc/rc.d/init.d/crond start >&2
else
	echo "Run \"/etc/rc.d/init.d/crond start\" to start cron daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del crond
	/etc/rc.d/init.d/crond stop >&2
fi

%triggerpostun -- vixie-cron
/sbin/chkconfig --add crond

%files
%defattr(640,root,root,755)
%attr(750,root,root) %config /etc/rc.d/init.d/crond

%config /etc/logrotate.d/cron

%attr(750,root,root) %dir /etc/crontab.d
%attr(750,root,root) %dir /etc/cron.*

%attr(0755,root,root) /usr/sbin/crond
%attr(4711,root,root) /usr/bin/crontab
%attr(0755,root,root) /usr/bin/run-parts

/usr/man/man*/*

%attr(750,root,root) %dir /var/spool/cron

%changelog
* Thu Apr 22 1999 Artur Frysiak <wiget@pld.org.pl>
  [0.11-5]
- compiled on rpm 3
- removed man group from man pages

* Sat Mar 06 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.11-4]
- fixed files permissions,
- cleaning up spec.

* Wed Jan 26 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.11-3d]
- added Gorup(pl).

* Mon Dec  9 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.11-2]
- added gzipping man pages,
- fixed %preun,
- fixed system crontab.

* Mon Nov 16 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.11-1]
- added crontabs to Obsoletes,
- added Provides: crontabs,
- changed %defattr to (600, root, root, 700),
- added restatring service in %post if before insall was started,
- added stop service in %preun on uninstall package,
- added NICE=15 in default crontab (as Qrczak suggest),
- new hc-cron-syscrondir.patch (made by Marcin 'Qrczak' Kowalczyk
  <qrczak@knm.org.pl>),
- added using %{SOURCE#} macros in %install.

* Mon Oct 5 1998 Marcin 'Qrczak' Kowalczyk <qrczak@knm.org.pl>
  [0.10-1]
- package generally reviewed: now properly handles catched-up jobs
  (it generally didn't work at all), added support for NICE variable,
  removed testing load average to execute catched-up jobs at idle time
  only (my system has a permanent low-priority process running), minor
  bugs fixed; everything is in the syscrondir patch

* Wed Sep 30 1998 Marcin 'Qrczak' Kowalczyk <qrczak@knm.org.pl>
- vixie-cron's spec and syscrondir patch adapted to hc-cron;
  other patches removed, as they are already applied in hc-cron's sources

* Mon Sep 28 1998 Marcin 'Qrczak' Kowalczyk <qrczak@knm.org.pl>
- use %{name} and %{version} macros
- simplified /etc/rc.d/rc?.d/???crond stuff
- added %setup -q parameter
- `mkdir -p' replaced with more standard `install -d'
- added full %attr description in %files
- /usr/sbin/crond permissions changed to 700
- replaced symlink in man page with .so include
- added pl translation
- changed install procedure to allow building from non-root account
- added patch that reads /etc/crontab.d/* in addition to /etc/crontab,
  simplifying automatic adding of cron jobs by packages,
- build against GNU libc-2.1
- start at RH spec file.  
