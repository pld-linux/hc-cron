.\" {PTM/LK/0.1/30-09-1998/"zarz�dzanie plikami crontab u�ytkownik�w"}
.\" T�umaczenie: 30-09-1998 �ukasz Kowalczyk (lukow@tempac.okwf.fuw.edu.pl)
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
.TH crontab 1 "29 grudnia 1993"
.UC 4
.SH NAZWA
crontab \- zarz�dzanie plikami crontab nale��cymi do u�ytkownik�w (V3)
.SH SK�ADNIA
crontab [ -u nazwa_u�ytkownika ] plik
.br
crontab [ -u nazwa_u�ytkownika ] { -l | -r | -e }
.SH OPIS
.I crontab 
jest programem s�u��cym do instalacji, deinstalacji lub
ogl�dania zawarto�ci tabel u�ywanych przez demon cron z pakietu Vixie Cron.
Ka�dy u�ytkownik mo�e posiada� w�asn� tabel�. Tabele cron s� plikami
przechowywanymi w katalogu /var lecz nie powinny by� bezpo�rednio
modyfikowane.
.PP
Je�eli istnieje plik
.IR allow ,
u�ytkownik musi by� w nim wymieniony, by mie� mo�liwo�� u�ywania polecenia
.IR crontab .
Je�eli nie istnieje plik
.I allow
lecz istnieje plik
.IR deny ,
u�ytkownik \fBnie\fR mo�e by� w nim wymieniony, by u�ywa� tego polecenia.
Je�eli nie istnieje �aden z tych plik�w, w�wczas dost�pno�� polecenia zale�y
od ustawie� konkretnego systemu. Mo�liwa jest zar�wno sytuacja, kiedy ka�dy
u�ytkownik ma dost�p do tego polecenia, jak i sytuacja, kiedy dost�p do niego
ma tylko administrator.
.PP
Je�eli podana zostanie opcja
.IR -u ,
okre�la ona u�ytkownika, kt�rego tabele cron maj� by� modyfikowane. Je�eli
ta opcja nie jest podana, modyfikowane b�d� tabele nale��ce do u�ytkownika
uruchamiaj�cego program. Zauwa�, �e polecenie 
.IR su (8)
mo�e zdezorientowa� program
.IR crontab .
Je�eli uruchamiasz
.I crontab
po wydaniu polecenia 
.IR su ,
powiniene� zawsze u�ywa� opcji 
.I \-u
ze wzgl�d�w bezpiecze�stwa.
.PP
Pierwsza forma wywo�ywania programu
.I crontab
s�u�y do utworzenia nowej tabeli na podstawie podanego pliku lub danych
pobranych ze standardowego wej�cia, je�eli podana zostanie pseudo-nazwa pliku
``-''.
.PP
Opcja 
.I -l
powoduje wypisanie bie��cej tabeli na standardowym wyj�ciu.
.PP
Opcja 
.I -r
usuwa bie��c� tabel�.
.PP
Opcja
.I -e
s�u�y do modyfikacji bie��cej tabeli przy pomocy edytora, kt�rego nazwa
znajduje si� w jednej ze zmiennych �rodowiskowych
\s-1VISUAL\s+1 lub \s-1EDITOR\s+1. Po opuszczeniu edytora zmodyfikowana
tabela zostanie automatycznie zainstalowana.
.SH "ZOBACZ TAK�E"
crontab(5), cron(8)
.SH PLIKI
.nf
/etc/cron.allow
/etc/cron.deny
.fi
.SH STANDARDY
Polecenie
.I crontab
jest zgodne ze standardem IEEE Std1003.2-1992 (``POSIX'').  
Nowa sk�adnia polecenia r�ni si� od sk�adni u�ywanej przez poprzednie
wersje Vixie Cron, jak r�wnie� od klasycznej sk�adni V3.
.SH DIAGNOSTYKA
Po uruchomieniu programu z b��dn� opcj� pojawi si� zrozumia�y opis
pope�nionego b��du.
.SH AUTOR
.nf
Paul Vixie <paul@vix.com>
