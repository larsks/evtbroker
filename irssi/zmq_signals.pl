#!/usr/bin/perl
#
use strict;
use Irssi;
use vars qw($VERSION %IRSSI);
use vars qw($CTX $SOCK);
use ZeroMQ qw(:all);
use Data::Dumper;
use Data::Structure::Util qw(unbless);

$VERSION = '1';
%IRSSI = (
	authors	=> 'Lars Kellogg-Stedman',
	contact	=> 'lars@oddbit.com',
);

$CTX = new ZeroMQ::Context;
$SOCK = $CTX->socket(ZMQ_PUB);
$SOCK->connect('tcp://localhost:13902');

sub remove_scalar_refs {
	my $data = shift @_;

	if (ref($data) eq "HASH") {
		my @todelete;
		while ( my ($key, $value) = each %{$data} )
		{
			if (ref($value) eq "SCALAR") {
				push @todelete, $key;
			} elsif (ref($value) eq "HASH") {
				remove_scalar_refs($value);
			}
		}

		foreach (@todelete) {
			delete $data->{$_};
		}
	}
}

sub sanitize {
	my $data = shift @_;

	# Recursively remove blessings.
	unbless $data;

	# Remove scalar references.
	remove_scalar_refs $data;
};

sub send_event {
	my $tag = shift @_;
	my $data = shift @_;

	sanitize($data);
	$data->{tag} = $tag;

	$SOCK->send($tag, ZMQ_SNDMORE);
	$SOCK->send_as(json => $data);
}

sub event_query_created {
	my $query = shift @_;

	delete $query->{server}->{rawlog};

	send_event('irssi.query.created', {
			query => $query,
		});
}

sub event_query_destroyed {
	my $query = shift @_;

	delete $query->{server}->{rawlog};

	send_event('irssi.query.destroyed', {
			query => $query,
		});
}

sub event_message_private {
	my $server  = shift @_;
	my $msg     = shift @_;
	my $nick    = shift @_;
	my $address = shift @_;

	delete $server->{rawlog};

	send_event('irssi.message.private', {
			server => $server,
			msg => $msg,
			nick => $nick,
			address => $address,
		});
}

sub event_message_own_private {
	my $server      = shift @_;
	my $msg         = shift @_;
	my $target      = shift @_;
	my $orig_target = shift @_;

	delete $server->{rawlog};

	send_event('irssi.message.own_private', {
			server => $server,
			msg => $msg,
			target => $target,
			orig_target => $orig_target,
		});
}

Irssi::signal_add('query created'       , 'event_query_created');
Irssi::signal_add('query destroyed'     , 'event_query_destroyed');
Irssi::signal_add('message private'     , 'event_message_private');
Irssi::signal_add('message own_private' , 'event_message_own_private');

send_event('irssi.script.load', {
		script => 'zmq_signals',
	})

