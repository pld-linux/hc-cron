.\" {PTM/PB/0.1/01-06-1998/"daemon do wywo�ywania od�o�onych komend"}
.\" Translation (c) 1999 Przemek Borys <pborys@dione.ids.pl>
.\"/* Copyright 1988,1990,1993 by Paul Vixie
.\" * All rights reserved
.\" *
.\" * Distribute freely, except: don't remove my name from the source or
.\" * documentation (don't take credit for my work), mark your changes (don't
.\" * get me blamed for your possible bugs), don't alter or remove this
.\" * notice.  May be sold if buildable source is provided to buyer.  No
.\" * warrantee of any kind, express or implied, is included with this
.\" * software; use at your own risk, responsibility for damages (if any) to
.\" * anyone resulting from the use of this software rests entirely with the
.\" * user.
.\" *
.\" * Send bug reports, bug fixes, enhancements, requests, flames, etc., and
.\" * I'll try to keep a version up to date.  I can be reached as follows:
.\" * Paul Vixie          <paul@vix.com>          uunet!decwrl!vixie!paul
.\" */
.\" 
.\" $Id$
.\" 
.TH CRON 8 "20 Grudzie� 1993"
.UC 4
.SH NAZWA
cron \- daemon do wywo�ywania od�o�onych komend
.SH SK�ADNIA
cron
.SH OPIS
.I Cron
powinien by� uruchamiany z /etc/rc lub /etc/rc.local.
Wyjdzie on natychmiast, wi�c nie musisz uruchamia� go z '&'.
.PP
.I Cron
przegl�da /var/spool/cron/crontabs w poszukiwaniu plik�w cronatab, kt�re s�
nazwane wed�ug kont w /etc/passwd; znalezione crontaby �aduje do pami�ci.
.I Cron
szuka r�wnie� /etc/crontab, kt�re jest w innym formacie (zobacz
.IR crontab(5)).
Nast�pnie
.I Cron
budzi si� co minut�, sprawdzaj�c wszystkie zapisane crontaby, czy
przypadkiem jaka� komenda w tej minucie nie powinna by� wywo�ana. Podczas
wywo�ywania komend, wszelkie ich wyj�cie jest przesy�ane poczt� do
w�a�ciciela crontaba (lub do u�ytkownika podanego w zmiennej �rodowiskowej
MAILTO w crontabie, je�li taki istnieje).
.PP
Dodatkowo,
.I cron
co minut� sprawdza czy czas modyfikacji (modtime) jego katalogu spoolowego
(lub czas modyfikacji
.IR /etc/crontab)
by� zmieniony, a je�li tak, to
.I cron
sprawdzi czasy modyfikacji crontab�w i prze�aduje wszystkie te, kt�re by�y
ostatnio zmienione.  Dlateg nie trzeba restartowa�
.I crona
za ka�dym razem gdy zmodyfikuje si� plik crontab. Zauwa�, �e komenda
.IR Crontab (1)
od�wie�a czas modyfikacji za ka�dym razem gdy zmieni crontab.
.SH "ZOBACZ TAK�E"
crontab(1), crontab(5)
.SH AUTOR
.nf
Paul Vixie <paul@vix.com>
