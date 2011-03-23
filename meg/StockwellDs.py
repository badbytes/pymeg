#! /usr/bin/env python

import sys, os, popen2, tempfile
from pylab import *
from math import floor
import ctf
from smt import *
from util import *
from markers import markers

usage("""[options] [dataset]

This program produces time-frequency plots using the Stockwell transform.
The default behavior is to average all trials and compute the Stockwell
transform of the average. Each channel is averaged separately and the
resulting Stockwells are averaged together.

For the -m, -c, and -T options, you can specify multiple arguments in
quotes, or use multiple options, or both. In other words,
	-m 'mark1 mark2 mark3'
and
	-m mark1 -m mark2 -m mark3
are equivalent.

Options are:

	-d dataset      You can either specify a dataset using -d or as
			the last argument.

	-m marker       Define trials relative to the specified marker,
			rather than the dataset's trial structure. You can
			use more than one marker.

	-t "t0 t1"      The time window (in seconds), relative to the markers,
			if any. Default: whole trial.

	-b "lo hi"      Frequencies to use. Default: "0 80".

	-a              Compute the average of the Stockwells, rather than
			the Stockwell of the average.

	-k K            Multitaper smoothing parameter. Default: 0. This is
			the number of tapers to use. This program uses sine
			tapers, resulting in a smoothing bandwidth that
			depends on the length of the time window as well as
			the number of tapers.

	-c channel      The channel list can be a set of individually
			specified channels or a prefix such as MLO or ML.
			There is no default, you need to specify at least
			one channel.

	-T trial        Only process the specified trial(s). You can
			specify more than one trial.

	-n              Don't apply the viewing filter parameters.

	-l              Plot the log of the power.

	-B "t0 t1"      Normalize by the average across the specified baseline
			time window.

	-r channel      Add a reference channel in a subplot.

	-o prefix       Name of an AFNI output BRIK. Default: display a graph.
			The BRIK stores the log of the Stockwell, so that
			subtracting one BRIK (or an average of several
			BRIKs) from another results in the log of the power
			ratio of the two conditions.

This is StockwellDs.py version 1.4""")

optlist, args = parseargs("m:t:b:ak:c:no:lr:T:d:B:")

dsname = None
mlist = []
clist = []
trlist = []
start = None
baset0 = None
lo = 0
hi = 80
K = 0
nflag = False
aflag = False
prefix = None
lflag = False
ref = None

for opt, arg in optlist:
	if opt == '-d':
		dsname = arg
	elif opt == '-m':
		mlist.extend(arg.split())
	elif opt == '-t':
		s = arg.split()
		if len(s) != 2:
			printerror("-t needs two times in quotes")
			printusage()
			sys.exit(1)
		start = float(s[0])
		end = float(s[1])
	elif opt == '-B':
		s = arg.split()
		if len(s) != 2:
			printerror("-B needs two times in quotes")
			printusage()
			sys.exit(1)
		baset0 = float(s[0])
		baset1 = float(s[1])
	elif opt == '-b':
		s = arg.split()
		if len(s) != 2:
			printerror("-b needs two frequencies in quotes")
			printusage()
			sys.exit(1)
		lo = float(s[0])
		hi = float(s[1])
	elif opt == '-k':
		K = int(arg)
		if K < 0:
			printerror("K must be >= 0")
			printusage()
			sys.exit(1)
	elif opt == '-c':
		clist.extend(arg.split())
	elif opt == '-T':
		trlist.extend(arg.split())
	elif opt == '-n':
		nflag = True
	elif opt == '-a':
		aflag = True
	elif opt == '-l':
		lflag = True
	elif opt == '-o':
		prefix = arg
	elif opt == '-r':
		ref = arg

if (dsname == None and len(args) != 1) or len(clist) == 0:
	printusage()
	sys.exit(1)

if dsname == None:
	dsname = args[0]
ds = ctf.PhysicalSet(dsname)

if nflag:
	ds.removeProcessing()

srate = ds.getSampleRate()
ntrials = ds.getNumberOfTrials()
nsamples = ds.getNumberOfSamples()

if ds.isAverage():
	ntrials = 1
	trlist = []

if start is None and len(mlist) == 0 and ntrials == 1 and not ds.isAverage():
	# This case is meant to prevent people from trying to Stockwell
	# an entire run. However, we'll allow a single trial, if it's
	# short enough.
	if nsamples > 10 * srate:
		printerror("Trial too long.")
		printerror("You must specify a marker and time window.")
		sys.exit(1)
	else:
		printerror("Note: defaulting to one trial of %d samples." %
			   nsamples)

# Convert times to number of samples.

if start is None:
	start = 0
	end = nsamples - 1
else:
	start = int(floor(start * srate + .5))
	end = int(floor(end * srate + .5))

if baset0 is not None:
	baset0 = int(floor(baset0 * srate + .5)) - start
	baset1 = int(floor(baset1 * srate + .5)) - start

# Make it an even number of samples.

if (end - start) % 2 == 1:
	end -= 1
if baset0 is not None:
	if (baset1 - baset0) % 2 == 1:
		baset1 -= 1

# Check the channel list.

def sensorlist(ds, cls = 'MEG-SENS'):
	"""Return a list of the channel names in ds, of class cls."""

	nchan = ds.getNumberOfChannels()
	l = []
	for i in range(nchan):
		c = ds.getChannel(i)
		t = c.getSensorClassName()
		if t == cls:
			l.append(c.getName())
	return l

slist = sensorlist(ds)
slist.extend(sensorlist(ds, cls = 'SAM-SENS'))
slist.extend(sensorlist(ds, cls = 'ADC-VOLTREF'))
slist.extend(sensorlist(ds, cls = 'EEG-SENS'))

clist1 = []
for c in clist:
	if c in slist:
		clist1.append(c)
	else:
		# Allow constructs such as 'MLO' which are prefixes
		# of names in the list.

		l = []
		n = len(c)
		for s in slist:
			if c == s[0:n]:
				l.append(s)
		if len(l) > 0:
			clist1.extend(l)
		else:
			printerror("channel %s not found" % c)
			sys.exit(1)

cnames = ', '.join(clist)
clist = clist1

# Look at the markers and construct the list of trials.

marks = markers(dsname)

for marker in mlist:
	if not marks.has_key(marker):
		printerror("unknown marker '%s'" % marker)
		sys.exit(1)

if len(mlist) == 0:
	# if no marks, use the start of each trial
	tlist = zip(range(ntrials), [0]*ntrials)
else:
	tlist = []
	for marker in mlist:
		tlist.extend(marks[marker])

# Filter out unwanted trials.

if len(trlist) > 0:
	trlist = map(int, trlist)
	def intr(t, tr = trlist):
		return t[0] in tr
	tlist = filter(intr, tlist)

seglen = end - start

# Convert frequencies in Hz into rows of the ST, given sampling rate and length.

def freq(f):
	return int(f * seglen / srate + .5)

if K > 0:
	tapers = calc_tapers(K, seglen)
s = 0.
if not aflag:
	s = [0.] * len(clist)
r = 0.
n = 0
maxm = len(tlist)
m = 1
for (tr, t) in tlist:
	samp = int(t * srate + .5)
	if samp + start < 0 or samp + end > nsamples:
		printerror("warning: segment exceeds trial boundaries for trial %d, time %g" % \
			(tr, t))
		continue
	print 'trial %d, %d samples at %d, %d of %d' % (tr, seglen, samp + start, m, maxm)
	m += 1
	for i, c in enumerate(clist):
		ch = ds.getChannel(c)
		d = ch.getCopyData(tr, samp + start, end - start)
		d *= 1e15 # convert from tesla to femtotesla
		d -= add.reduce(d) / len(d) # remove the mean
		if aflag:
			print c,
			sys.stdout.flush()
			if K == 0:
				s += abs(st(d, freq(lo), freq(hi)))**2
			else:
				s += mtst(K, tapers, d, freq(lo), freq(hi))
		else:
			s[i] += d

		n += 1
	if ref:
		ch = ds.getChannel(ref)
		d = ch.getCopyData(tr, samp + start, end - start)
		r += d
	if aflag:
		print

if n == 0:
	printerror("no valid trials!")
	sys.exit(1)

r /= n
if aflag:
	s /= n
else:
	d = 0.
	for i, c in enumerate(clist):
		print c,
		sys.stdout.flush()
		if K == 0:
			d += abs(st(s[i] / n, freq(lo), freq(hi)))**2
		else:
			d += mtst(K, tapers, s[i] / n, freq(lo), freq(hi))
	print
	s = d / len(clist)

print 'bw =', calcbw(K, seglen, srate)

def writebrik(s, prefix):
	"Write 2D TF data as an AFNI BRIK."

	# dump the array into a file
	fd, tmpfile = tempfile.mkstemp()
	f = os.fdopen(fd, 'w')
	asarray(s, dtype = Float32).tofile(f)
	f.close()

	# use to3d to create the BRIK file
	sess = os.path.dirname(prefix)
	prefix = os.path.basename(prefix)
	pathname = os.path.join(sess, prefix)
	run("rm -f %s+orig.*" % pathname)
	if sess:
		arg = "-session %s -prefix %s" % (sess, prefix)
	else:
		arg = "-prefix %s" % prefix
	cmd = "to3d -fim %s -xSLAB 0P-%dP -ySLAB 0S-%dS -zFOV 0L-1R 3Df:0:0:%d:%d:1:%s" % \
		(arg, s.shape[1], s.shape[0], s.shape[1], s.shape[0], tmpfile)
	run(cmd + " 2> /dev/null")

	# clean up, and set some fields in the AFNI header.
	os.unlink(tmpfile)
	note = "tfdim: %d %d %g %g %g" % (start, end, srate, lo, hi)
	cmd = "3dNotes -h '%s' %s+orig" % (note, pathname)
	run(cmd)
	note = "tftitle: %s %s" % (caption, cnames)
	cmd = "3dNotes -h '%s' %s+orig" % (note, pathname)
	run(cmd)

from tics import scale1

def plotst(y, titlestr):
	n = min(minimum.reduce(y))
	m = max(maximum.reduce(y))
	nlevels = 40
	clevel = linspace(n, m, nlevels)
	ticks, mticks = scale1(clevel[0], clevel[-1])
	time = linspace(start / srate, end / srate, y.shape[1])
	fr = linspace(lo, hi, y.shape[0])
	if ref:
		subplot(211)
	c = contourf(time, fr, y, clevel, cmap = cm.jet)
	cax = gca()
	title(titlestr, fontsize = 15)
	colorbar(format = '%.2g', ticks = ticks)
	newright = cax.get_position()[2]
	if ref:
		from matplotlib.colorbar import make_axes
		subplot(212)
		plot(time, r)
		# ensure the x axis takes up the same amount of space
		ax = gca()
		p = ax.get_position()
		p[2] = newright
		ax.set_position(p)
		# ensure the x axis has the same range
		a = list(ax.axis())
		a[0:2] = cax.axis()[0:2]
		ax.axis(a)

if len(mlist) == 0:
	caption = "%d trial%s" % (ntrials, 's'[0:ntrials > 1])
else:
	caption = ', '.join(mlist)

if baset0 is not None:
	# Average across the baseline, and set all time points to that
	# average. (dimensions are frequency and time)

	x = add.reduce(s[:, baset0:baset1], 1) / (baset1 - baset0)
	x.shape = (x.shape[0], 1)
	x = repeat(x, s.shape[1], 1)

	# Normalize s by the baseline time average.

	s /= x

if prefix:
	writebrik(log(s), prefix)
	sys.exit(0)

if lflag:
	s = log(s)

figure()
plotst(s, "%s; %s" % (caption, cnames))
show()
