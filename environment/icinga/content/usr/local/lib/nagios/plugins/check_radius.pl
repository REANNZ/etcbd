#!/usr/bin/perl -w

use strict;
use Getopt::Long;
use File::Basename;
use Time::HiRes qw(gettimeofday tv_interval);;

# Fetched from Nagios Exchange, modified by Jamie, 2013-11-06

# my $version =	"20100116";
my $version =	"20131106";
my $host =	"localhost";
my $port =	1812;
my $debug =	0;
my $w =		3;
my $c =		5;
my $t =		10;
my $filename;
my $secret;
my $status;

my $radclient =	"/usr/bin/radclient";

my %ERRORS =	('OK'=>0,'WARNING'=>1,'CRITICAL'=>2,'UNKNOWN'=>3,'DEPENDENT'=>4);



sub usage() {
	my $basename = basename($0);

print <<DATA;

	Version: $version
	$basename [-h] [-d] [-H hostname] [-P port] [-w warning] [-c critical] [-t timeout] -s secret

	-h|--help	This help screen
	-d|--debug	Activate debug mode
	-H|--hostname	Hostname to send query [Default: $host]
	-P|--port	Port where status server is listening [Default: $port]
	-w|--warning	Warning threshold in seconds [Default: $w]
	-c|--critical	Critical threshold in seconds [Default: $c]
	-t|--timeout	Timeout [Default: $t]
	-s|--secret	Secret

	Plugin to check radius status. It use the radclient program from FreeRADIUS project
	(http://www.freeradius.org) and use the Status-Server packet to perform tests. See
	http://wiki.freeradius.org/Status on how to configure it.

	The plugin output performance data about elapsed time executing the query.

DATA

	exit $ERRORS{'UNKNOWN'};
}

sub check_options () {
	my $o_help;
	my $o_debug;

	Getopt::Long::Configure ("bundling");
	GetOptions(
		'h|help'	=> \$o_help,
		'd|debug'	=> \$o_debug,
		'H|hostname:s'	=> \$host,
		'P|port:i'	=> \$port,
		'w|warning:i'	=> \$w,
		'c|critical:i'	=> \$c,
		't|timeout:s'	=> \$t,
		's|secret:s'	=> \$secret,

	);

	usage() if (defined($o_help));
	$debug = 1 if (defined($o_debug));
	if ( $port !~ /^\d+$/ or ($port <= 0 or $port > 65535)) {
		print "\nPlease insert an integer value between 1 and 65535\n";
		usage();
	}
	if ( $w !~ /^\d+$/ or $w <= 0) {
		print "\nPlease insert an integer value as warning threshold\n";
		usage();
	}
	if ( $c !~ /^\d+$/ or $c <= 0) {
		print "\nPlease insert an integer value as critical threshold\n";
		usage();
	}
	if ( $t !~ /^\d+$/ or $t < $c) {
		print "\nPlease insert an integer value greater than $c\n";
		usage();
	}
	if ( !defined($secret) ) {
		print "\nPlease supply the secret for $host\n";
		usage();
	}
}

sub shell_escape_single_quote {
  my ($str) = @_;
  $str =~ s/'/'"'"'/g;

  return $str;
}

#
# Main
#
check_options();

my $cmd = "echo \"Message-Authenticator = 0x00\" | $radclient -q -c 1 -r 1 " .
    "-t '" . shell_escape_single_quote($t) . "' '" . shell_escape_single_quote($host . ":" . $port) . "' " .
    "status '" . shell_escape_single_quote($secret) . "' 2>/dev/null";
print "DEBUG: radclient command: $cmd\n" if $debug;

my $t0 = [gettimeofday];
system($cmd);
my $elapsed = tv_interval($t0);

$status = $ERRORS{'OK'} if ( $elapsed < $w );
$status = $ERRORS{'WARNING'} if ( $elapsed >= $w );
$status = $ERRORS{'CRITICAL'} if ( $elapsed >= $c or $? !=0 );

print "DEBUG: Elapsed time: $elapsed seconds\n" if $debug;
print "DEBUG: radclient exit status: $?\n" if $debug;
print "DEBUG: plugin exit status: $status\n" if $debug;

print "Radius response time $elapsed seconds";
print " | ";
print "'Response Time'=$elapsed;$w;$c;0;$t\n";

exit $status;

