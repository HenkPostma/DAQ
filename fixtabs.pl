#!/usr/bin/perl 

use strict; 

my $file = $ARGV[0]; 

if (not(-e $file)) {
      print "specify file on the command line, $file does not exist\n";
      exit; 
}
print $file; 

system("cp $file $file.old");
open(input, "< $file.old");
open(output, "> $file"); 
while (not(eof(input))) {
   my $line = <input>;
   if ($line =~ /\t/) {
      $line =~ s/\t/\ \ \ \ /g;
      print $line;
   }
   print output $line;
}
close (input); 
close(output); 
