Summary:	Home computer cron daemon
Summary(de):	Home computer cron daemon 
Summary(fr):	Démon Home computer cron
Summary(pl):	Demon cron dla domowego komputera
Summary(tr):	Home computer cron süreci, periyodik program çalýþtýrma yeteneði
Name:		hc-cron
Version:	0.13
Release:	1
Copyright:	GPL
Group:		Daemons
Group(pl):	Serwery
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/daemons/cron/%{name}-%{version}.tar.gz
Source1:	hc-cron.init
Source2:	cron.logrotate
Source3:	run-parts
Source4:	hc-cron.crontab
Source5:	crontab.1.pl
Source6:	cron.8.pl
Source7:	cron.sysconfig
Patch0:		hc-cron-syscrondir.patch
Patch1:		hc-cron-paths.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
Provides:	crontabs
Provides:	crondaemon
Obsoletes:	crondaemon
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
%setup  -q
%patch0 -p1
%patch1 -p1 -b .wiget 

%build
make OPTIM="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{cron.{hourly,daily,weekly,monthly},cron} \
	$RPM_BUILD_ROOT/etc/{cron.d,rc.d/init.d,logrotate.d,sysconfig} \
	$RPM_BUILD_ROOT%{_mandir}/{man{1,5,8},pl/man{1,8}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_bindir}} \
	$RPM_BUILD_ROOT/var/{spool/cron,log} 

make install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/pl/man1/crontab.1
install %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/pl/man8/cron.8

echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/man8/crond.8
echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/pl/man8/crond.8

echo "# Simple define users for cron" > $RPM_BUILD_ROOT/etc/cron/cron.allow
:> $RPM_BUILD_ROOT/var/log/cron

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/crond
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/cron
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE4} $RPM_BUILD_ROOT/etc/cron.d/system
install %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/cron

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/{man*/*,pl/man*/*}

%clean
rm -rf $RPM_BUILD_ROOT

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
	/sbin/chkconfig --del crond
	/etc/rc.d/init.d/crond stop >&2
fi

%triggerpostun -- vixie-cron
/sbin/chkconfig --add crond

%files
%defattr(644,root,root,755)

%attr(754,root,root) /etc/rc.d/init.d/crond

%attr(640,root,root) %config /etc/logrotate.d/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*

%attr(750,root,root) %dir /etc/cron.*
%attr(640,root,root) %config /etc/cron/*
%attr(640,root,root) /etc/cron.d/*

%attr(0755,root,root) %{_sbindir}/crond
%attr(4711,root,root) %{_bindir}/crontab
%attr(0755,root,root) %{_bindir}/run-parts

%{_mandir}/man*/*
%lang(pl) %{_mandir}/pl/man*/*

%attr(750,root,root) %dir /var/spool/cron
%attr(640,root,root) %ghost /var/log/*
