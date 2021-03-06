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
cimport kenbot.configuration_manager as configuration_manager
cimport kenbot.kenbot_channel_consumer as kenbot_channel_consumer
cimport kenbot.initializer as initializer
cimport kenbot.kenbot_api as kenbot_api
cimport kenbot.producers as producers
cimport kenbot.task_manager as task_manager


cdef class kenbot:
    cdef object logger

    cdef public double start_time

    cdef public bint reset_trading_history
    cdef public bint initialized
    cdef public bint ignore_config

    cdef public dict tools
    cdef public dict config
    cdef public str bot_id

    cdef object _aiohttp_session
    cdef public object community_handler
    cdef public object community_auth
    cdef public object async_loop
    cdef public object tentacles_setup_config

    cdef public initializer.Initializer initializer
    cdef public task_manager.TaskManager task_manager
    cdef public producers.ExchangeProducer exchange_producer
    cdef public producers.EvaluatorProducer evaluator_producer
    cdef public producers.InterfaceProducer interface_producer
    cdef public producers.ServiceFeedProducer service_feed_producer
    cdef public kenbot_api.kenbotAPI kenbot_api
    cdef public kenbot_channel_consumer.kenbotChannelGlobalConsumer global_consumer
    cdef public configuration_manager.ConfigurationManager configuration_manager

    cpdef object run_in_main_asyncio_loop(self, object coroutine)
    cpdef void set_watcher(self, object watcher)
    cpdef object get_aiohttp_session(self)
    cpdef object get_edited_config(self, str config_key, bint dict_only=*)
    cpdef void set_edited_config(self, str config_key, object config)
    cpdef object get_startup_config(self, str config_key, bint dict_only=*)
    cpdef object get_trading_mode(self)
