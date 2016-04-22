#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Scores SemEval-2014 task 9, subtask B
#
#  Last modified: April 7, 2014
#
#

use warnings;
use strict;
use utf8;
binmode (STDIN,  ":utf8");
binmode (STDOUT, ":utf8");


my $GOLD_FILE 	       =  $ARGV[0];
my $INPUT_FILE         =  $ARGV[1];


########################
###   MAIN PROGRAM   ###
########################

my %stats = ();

### 1. Read the files and get the statsitics
open INPUT, '<:encoding(UTF-8)', $INPUT_FILE or die;
open GOLD,  '<:encoding(UTF-8)', $GOLD_FILE or die;

my $lineNo = 1;
for (; <INPUT>; $lineNo++) {
	s/^[ \t]+//;
	s/[ \t\n\r]+$//;

	### 1.1. Check the input file format
	#NA	1	positive	i'm done writing code for the week! Looks like we've developed a good a** game for the show Revenge on ABC Sunday, Premeres 09/30/12 9pm
	die "Wrong file format!" if (!/^([0-9]+)\t([0-9]+)\t(positive|negative|neutral)/);
	my $proposedLabel = $3;

	### 1.2	. Check the gold file format
	#NA	T14114531	positive
	$_ = <GOLD>;
	die "Wrong file format!" if (!/^([0-9]+)\t([0-9]+)\t(positive|negative|neutral)/);
	my $trueLabel = $3;

	### 1.3. Update the statistics
	$stats{$proposedLabel}{$trueLabel}++;
}

close(INPUT) or die;
close(GOLD) or die;

#$lineNo--;
#die "Too few lines: $lineNo" if (934 != $lineNo);

### 2. Initialize zero counts
foreach my $class1 ('positive', 'negative', 'neutral') {
	foreach my $class2 ('positive', 'negative', 'neutral') {
		$stats{$class1}{$class2} = 0 if (!defined($stats{$class1}{$class2}))
	}
}

### 3. Calculate the F1 for each dataset
print "$INPUT_FILE\n";

my $overall = 0.0;
foreach my $class ('positive', 'negative', 'neutral') {
	my $denomP = ($stats{'positive'}{$class} + $stats{'negative'}{$class} + $stats{'neutral'}{$class}) > 0 ? ($stats{'positive'}{$class} + $stats{'negative'}{$class} + $stats{'neutral'}{$class}) : 1;
	my $P = 100.0 * $stats{$class}{$class} / $denomP;

	my $denomR = (($stats{$class}{'positive'} + $stats{$class}{'negative'} + $stats{$class}{'neutral'}) > 0) ? ($stats{$class}{'positive'} + $stats{$class}{'negative'} + $stats{$class}{'neutral'}) : 1;
	my $R = 100.0 * $stats{$class}{$class} / $denomR;
	
	my $denom = ($P+$R > 0) ? ($P+$R) : 1;
	my $F1 = 2*$P*$R / $denom;
	$overall += $F1 if ($class ne 'neutral');
	printf "\t%8s: P=%0.2f, R=%0.2f, F1=%0.2f\n", $class, $P, $R, $F1;
}
$overall /= 2.0;
printf "\tOVERALL SCORE : %0.2f\n", $overall;

