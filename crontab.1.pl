.\" {PTM/LK/0.1/30-09-1998/"zarz±dzanie plikami crontab u¿ytkowników"}
.\" T³umaczenie: 30-09-1998 £ukasz Kowalczyk (lukow@tempac.okwf.fuw.edu.pl)
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
crontab \- zarz±dzanie plikami crontab nale¿±cymi do u¿ytkowników (V3)
.SH SK£ADNIA
crontab [ -u nazwa_u¿ytkownika ] plik
.br
crontab [ -u nazwa_u¿ytkownika ] { -l | -r | -e }
.SH OPIS
.I crontab 
jest programem s³u¿±cym do instalacji, deinstalacji lub
ogl±dania zawarto¶ci tabel u¿ywanych przez demon cron z pakietu Vixie Cron.
Ka¿dy u¿ytkownik mo¿e posiadaæ w³asn± tabelê. Tabele cron s± plikami
przechowywanymi w katalogu /var lecz nie powinny byæ bezpo¶rednio
modyfikowane.
.PP
Je¿eli istnieje plik
.IR allow ,
u¿ytkownik musi byæ w nim wymieniony, by mieæ mo¿liwo¶æ u¿ywania polecenia
.IR crontab .
Je¿eli nie istnieje plik
.I allow
lecz istnieje plik
.IR deny ,
u¿ytkownik \fBnie\fR mo¿e byæ w nim wymieniony, by u¿ywaæ tego polecenia.
Je¿eli nie istnieje ¿aden z tych plików, wówczas dostêpno¶æ polecenia zale¿y
od ustawieñ konkretnego systemu. Mo¿liwa jest zarówno sytuacja, kiedy ka¿dy
u¿ytkownik ma dostêp do tego polecenia, jak i sytuacja, kiedy dostêp do niego
ma tylko administrator.
.PP
Je¿eli podana zostanie opcja
.IR -u ,
okre¶la ona u¿ytkownika, którego tabele cron maj± byæ modyfikowane. Je¿eli
ta opcja nie jest podana, modyfikowane bêd± tabele nale¿±ce do u¿ytkownika
uruchamiaj±cego program. Zauwa¿, ¿e polecenie 
.IR su (8)
mo¿e zdezorientowaæ program
.IR crontab .
Je¿eli uruchamiasz
.I crontab
po wydaniu polecenia 
.IR su ,
powiniene¶ zawsze u¿ywaæ opcji 
.I \-u
ze wzglêdów bezpieczeñstwa.
.PP
Pierwsza forma wywo³ywania programu
.I crontab
s³u¿y do utworzenia nowej tabeli na podstawie podanego pliku lub danych
pobranych ze standardowego wej¶cia, je¿eli podana zostanie pseudo-nazwa pliku
``-''.
.PP
Opcja 
.I -l
powoduje wypisanie bie¿±cej tabeli na standardowym wyj¶ciu.
.PP
Opcja 
.I -r
usuwa bie¿±c± tabelê.
.PP
Opcja
.I -e
s³u¿y do modyfikacji bie¿±cej tabeli przy pomocy edytora, którego nazwa
znajduje siê w jednej ze zmiennych ¶rodowiskowych
\s-1VISUAL\s+1 lub \s-1EDITOR\s+1. Po opuszczeniu edytora zmodyfikowana
tabela zostanie automatycznie zainstalowana.
.SH "ZOBACZ TAK¯E"
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
Nowa sk³adnia polecenia ró¿ni siê od sk³adni u¿ywanej przez poprzednie
wersje Vixie Cron, jak równie¿ od klasycznej sk³adni V3.
.SH DIAGNOSTYKA
Po uruchomieniu programu z b³êdn± opcj± pojawi siê zrozumia³y opis
pope³nionego b³êdu.
.SH AUTOR
.nf
Paul Vixie <paul@vix.com>
