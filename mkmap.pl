#!/usr/bin/perl

# generated from http://openstreetmap.gryph.de/bigmap.cgi/
# permalink for this map: http://openstreetmap.gryph.de/bigmap.cgi?xmin=1100&xmax=1107&ymin=692&ymax=699&zoom=11&scale=256&baseurl=http%3A%2F%2Ftile.openstreetmap.org%2F%21z%2F%21x%2F%21y.png
#
use strict;
use LWP;
use GD;
use Math::Trig;

sub lon_to_x{
    my($lon, $zoom)=@_;
    return (($lon + 180.) / 360) * (2** $zoom);
}

sub lat_to_y{
     my $pi=3.1415926;
     my($lat, $zoom)=@_;
     return (1 - log(tan($lat * $pi / 180) + 1 / cos($lat * $pi / 180)) / $pi) / 2 * (2** $zoom);
}
sub round{
    my $float=shift;
    my $rounded = int($float + $float/abs($float*2));
    return $rounded;
}
my ($zoom,$startx,$starty,$nx,$ny);
my $REMO=0;
if ($#ARGV==5){
    print STDERR ("five args\n");
    if ($ARGV[0]=="rm"){
	shift( @ARGV);
	$REMO=1;
	print STDERR ("NEWLY @ARGV\n");
    }
}
if ($#ARGV!=4){
    print("./mkmap.pl zoom  xtile ytile nx  ny > a.png \n");
    print("./mkmap.pl 15    17682 11090    28  28 > prague_full.png\n");
    print("./mkmap.pl 15    16563 11245    65 66  > paris_full.png\n");
    print("./mkmap.pl 15    16246 11303    1 1   >le_mont_saint_michel.png\n");
    print("./mkmap.pl 15    16340 11206    14 6 > courselles.png\n");
    print("./mkmap.pl 15    16342 11222    16 12  >caen.png\n");
    print("./mkmap.pl 15    17678 11130    6  4  >mnisek.png\n");
    exit;
}else{
    ($zoom,$startx,$starty,$nx,$ny)=@ARGV;
    $startx=round(lon_to_x($startx, $zoom));
    $starty=round(lat_to_y($starty,$zoom));
    print STDERR "tiles: $startx  $starty\n";
#    if (($zoom!=11)&&($zoom!=15)){
#	print("zoom only 11 or 15\n");
#	exit;
#    }
	
    #print("$zoom,$startx,$starty,$nx,$ny\n");
}

my $img = GD::Image->new(256*$nx, 256*$ny, 1);
my $white = $img->colorAllocate(248,248,248);
$img->filledRectangle(0,0,256*$nx, 256*$ny,$white);
my $ua = LWP::UserAgent->new();
$ua->env_proxy;
my $total=0;
for (my $x=0;$x<$nx;$x++)
{
    for (my $y=0;$y<$ny;$y++)
    {
        my $xx = $x + $startx;
        my $yy = $y + $starty;   # 692 dole tabor[700]  688 dole mnisek[696]
	#        foreach my $base(split(/\|/, "http://tile.openstreetmap.org/11/!x/!y.png"))
        foreach my $base(split(/\|/, "http://localhost:8900/".$zoom."/!x/!y.png"))
	{
		my $url = $base;
                $url =~ s/!x/$xx/g;
                $url =~ s/!y/$yy/g;
if ($REMO==0){		print STDERR "$url... ";}
		my $resp = $ua->get($url);
if ($REMO==0){		print STDERR $resp->status_line;}
		$total=$total+1;
if ($REMO==0){		print STDERR "   ",$total,"/",$nx*$ny," \n";}
if ($REMO==1){		print STDERR "rm $zoom/$xx/$yy.png\n";}
		next unless $resp->is_success;
		my $tile = GD::Image->new($resp->content);
		next if ($tile->width == 1);
		if ($base =~ /seamark/) {
		my $black=$tile->colorClosest(0,0,0);
		$tile->transparent($black);
		}
		$img->copy($tile, $x*256,$y*256,0,0,256,256);
	}
    }
}
binmode STDOUT;
print $img->png();

##########################
exit;

my $startx=1092; #CZ
my $starty=686;  #CZ

 $startx=1011; #Bretagne
 $starty=696; #Bretagne

 $startx=1011; #Bretagne  5x+paris
 $starty=696; #Bretagne  2x+paris

 $startx=1011; #Bretagne  5x+paris
 $starty=692; #Bretagne also Amiens 2x+paris

 $startx=1049; #saarbruck
 $starty=696; #saarbruck

 $startx=1089; #nurnberg
 $starty=696; # nurnberg

 $startx=1089; # lago di bolsena
$starty=750; #


 $startx=1094; # Roma ?
 $starty=756; # 
 $startx=1098; #  Napoli?
 $starty=760; # 

 $startx=1109; # vallo della lucania
 $starty=770; # 

 $startx=1104; #  Catania
 $starty=789; # 

my $nx=1;
my $ny=1;
