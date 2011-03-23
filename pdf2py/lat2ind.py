# Copyright 2008 Dan Collins
#
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA




from pdf2py import header
from numpy import round

class calc():
    def __init__(self, datapdf, epoch, starttime, endtime):
        '''
        give epoch number and start and end times and returns sample indexes.
        starttime and endtime in seconds.
        '''
        h=header.read(datapdf)
        h.header_data.total_epochs[0]
        self.epochlength=h.epoch_data[0].pts_in_epoch[0]
        self.startind=round(starttime/h.header_data.sample_period[0]+(h.epoch_data[0].pts_in_epoch[0]*(epoch-1)))
        self.endind=round(endtime/h.header_data.sample_period[0]+(h.epoch_data[0].pts_in_epoch[0]*(epoch-1)))
        