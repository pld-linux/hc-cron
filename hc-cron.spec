Summary:     Home computer cron daemon
Summary(de): Home computer cron daemon 
Summary(fr): Démon Home computer cron
Summary(pl): Demon cron dla domowego komputera
Summary(tr): Home computer cron süreci, periyodik program çalýþtýrma yeteneði
Name:        hc-cron
Version:     0.11
Release:     2
Copyright:   GPL
Group:       Daemons
Source0:     ftp://sunsite.unc.edu/pub/Linux/system/daemons/cron/%{name}-%{version}.tar.gz
Source1:     hc-cron.init
Source2:     cron.log
Source3:     run-parts
Source4:     hc-cron.crontab
Patch:       hc-cron-syscrondir.patch
Prereq:      /sbin/chkconfig
Provides:    crontabs
Buildroot:   /tmp/%{name}-%{version}-root
Obsoletes:   vixie-cron crontabs

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
%patch -p1 -b .syscrondir

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
echo ".so cron.8" >$RPM_BUILD_ROOT/usr/man/man8/crond.8

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
%defattr(600, root, root, 700)
%attr(755, root, root) %config /etc/rc.d/init.d/crond
%config /etc/logrotate.d/cron
/etc/crontab.d
%dir /etc/cron.*
%attr(700, root, root) /usr/sbin/crond
%attr(4755,root, root) /usr/bin/crontab
%attr(755, root, root) /usr/bin/run-parts
%attr(644, root,  man) /usr/man/man*/*
/var/spool/cron

%changelog
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
  simplifying automatic adding of cron jobs by packages

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Jeff Johnson <jbj@redhat.com>
- reset SIGCHLD before grandchild execle (problem #732)

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscript

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Dec 11 1997 Cristian Gafton <gafton@redhat.com>
- added a patch to get rid of the dangerous sprintf() calls
- added BuildRoot and Prereq: /sbin/chkconfig

* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- fixed cron/crond dichotomy in init file.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- fixed bad init symlinks

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- force it to use SIGCHLD instead of defunct SIGCLD

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- updated for chkconfig
- added status, restart options to init script

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Wed Feb 19 1997 Erik Troan <ewt@redhat.com>
- Switch conditional from "axp" to "alpha"
