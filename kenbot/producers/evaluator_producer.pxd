# cython: language_level=3
#  gotbase kenbot
#  Copyright (c) gotbase, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
cimport kenbot.channels as kenbot_channel 


cdef class EvaluatorProducer(kenbot_channel.kenbotChannelProducer):
    cdef public object kenbot
    cdef public object tentacles_setup_config

    cdef public str matrix_id