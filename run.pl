#!/usr/bin/perl

use Net::Telnet::Cisco;

my $host = $ARGV[0];
my $cmd = $ARGV[1];


my $SCRIPT='/opt/collector';


my $user, $pass;

open(my $USER, '<', "$SCRIPT/config/cred.conf");
while(<$USER>) {
        ($user, $pass) = $_ =~ /(\S+)\s+(\S+)/i;
}

close($USER);

my $prompt='/(?m:^\\s?(?:[\\w.\/]+\:)?(?:[\\w.-]+\@)?[\\w.-]+\\s?(?:\(config[^\)]*\))?\\s?[\$#>]\\s?(?:\(enable\))?\\s*$)/';

print "\n\n========Telnet to: $host=======\n";
$session = Net::Telnet::Cisco->new(Host => $host, Prompt => $prompt, Errmode => "return", Input_Log => "debug.txt",max_buffer_length=>100048576, Timeout => 10000000);

if(!$session) {
        print "Failed to connect: $host\n";
        next;
}

$session->login($user,$pass);
$session->enable($pass);
$session->cmd('term len 0');
$session->cmd('term wid 0');

print $session->cmd($cmd);


$session->close;


