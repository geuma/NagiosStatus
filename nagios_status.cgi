#!/usr/bin/perl -w
#
# nagios_status.cgi
# Copyright (C) 2010-2013 Stefan Heumader <stefan@heumader.at>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

use strict;
use warnings;

use NagiosStatus;

my $foo = NagiosStatus->new("/usr/local/nagios/var/status.dat");
#$foo->debug(1);
$foo->parse_statusfile();
$foo->evaluate();
my @alerts = $foo->get_alerts(["host_name", "service_description", "plugin_output"]);

my $ct = "Content-Type: text/html\n\n";
$ct .= "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">\n";
$ct .= "<html>\n";
$ct .= "\t<head>\n";
$ct .= "\t\t<title>Nagios Status</title>\n";
$ct .= "\t\t<META HTTP-EQUIV=\"Refresh\" CONTENT=\"10\">\n";
$ct .= "\t\t<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
$ct .= "\t\t<META HTTP-EQUIV=\"Expires\" CONTENT=\"0\">\n";
$ct .= "\t\t<link href=\"/style.css\" rel=\"stylesheet\" rev=\"stylesheet\" type=\"text/css\">\n";
$ct .= "\t</head>\n";
$ct .= "\t<body>\n";
$ct .= "\t\t<table width=\"100%\">\n";

if (scalar @alerts == 0)
{
	$ct .= "\t\t\t<tr><td class=\"green\">NO PROBLEM</td></tr>\n";
}
foreach (@alerts)
{
	$ct .= "\t\t\t<tr>\n";

	$ct .= "\t\t\t\t<td ";
	$ct .= "id=\"$_->{'id'}1\" " if defined($_->{'id'});
	$ct .= "class=\"$_->{'type'}\">$_->{'host_name'}</td>\n";

	$ct .= "\t\t\t\t<td ";
	$ct .= "id=\"$_->{'id'}2\" " if defined($_->{'id'});
	$ct .= "class=\"$_->{'type'}\">$_->{'service_description'}</td>\n";

	$ct .= "\t\t\t\t<td ";
	$ct .= "id=\"$_->{'id'}3\" " if defined($_->{'id'});
	$ct .= "class=\"$_->{'type'}\">$_->{'plugin_output'}</td>\n";

	$ct .= "\t\t\t</tr>\n";
}
$ct .= "\t\t</table>\n";
$ct .= "\t</body>\n";
$ct .= "</html>";

print $ct;
