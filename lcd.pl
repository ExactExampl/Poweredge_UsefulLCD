#!/usr/bin/perl -w
#
# Jesper Nyerup <nyerup@one.com>

my $ipmitool = '/usr/bin/ipmitool';

my @chararray = split(//, join(' ', @ARGV));
usage() if (@chararray == 0 or @chararray > 14);

system("$ipmitool raw 0x6 0x58 193 0x0 0x0 ".
    sprintf('0x%x ', scalar(@chararray)).
    join(' ', map { sprintf('0x%x', ord($_)) } @chararray));
system("$ipmitool raw 0x6 0x58 0xc2 0x0 0x0 ".
    "0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0");

sub usage {
    print <<EOF;

  Usage: $0 <string>
         Max. 14 characters

EOF
    exit 1
}
